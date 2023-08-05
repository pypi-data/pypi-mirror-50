"""
Core procedures for processing source content.

In order for a submission to be finalized, it must have a valid source package,
and the source must be processed. Source processing involves the transformation
(and possibly validation) of sanitized source content (generally housed in the
file manager service) into a usable preview (generally a PDF) that is housed in
the submission preview service.

The specific steps involved in source processing vary among supported source
formats. The primary objective of this module is to encapsulate in one location
the orchestration involved in processing submission source packages.

The end result of source processing is the generation of a
:class:`.ConfirmSourceProcessed` event. This event signifies that the source
has been processed succesfully, and that a corresponding preview may be found
in the preview service.

Implementing support for a new format
=====================================
Processing support for a new format can be implemented by registering a new
:class:`SourceProcess`, using :func:`._make_process`. Each source process
supports a specific :class:`SubmissionContent.Format`, and should provide a
starter, a checker, and a summarizer. The preferred approach is to extend the
base classes, :class:`.BaseStarter`, :class:`.BaseChecker`, and
:class:`.BaseSummarizer`.

Using a process
===============
The primary API of this module is comprised of the functions :func:`start`,
:func:`check`, and :func:`summarize`. These functions dispatch to the
processes defined/registered in this module.

"""

import io
from typing import IO, Dict, Tuple, NamedTuple, Optional, Any, Callable

from arxiv.integration.api.exceptions import NotFound
from arxiv.submission import InvalidEvent, User, Client, Event, Submission, \
    SaveError
from .. import save
from ..domain import Preview, SubmissionContent, Submission
from ..domain.event import ConfirmSourceProcessed
from ..services import PreviewService, Compiler, Filemanager

Status = str
SUCCEEDED: Status = 'succeeded'
FAILED: Status = 'failed'
IN_PROGRESS: Status = 'in_progress'

Summary = Dict[str, Any]
"""Summary information suitable for generating a response to users/clients."""

IStarter = Callable[[Submission, User, Optional[Client], str], Status]
"""Interface for processing starter functions."""

IChecker = Callable[[Submission, User, Optional[Client], str], Status]
"""Interface for status check functions."""

ISummarizer = Callable[[Submission, User, Optional[Client], str], Summary]
"""Interface for processing summarizer functions."""


class SourceProcess(NamedTuple):
    """Container for source processing routines for a specific format."""

    supports: SubmissionContent.Format
    """The source format supported by this process."""

    start: IStarter
    """A function for starting processing."""

    check: IChecker
    """A function for checking the status of processing."""

    summarize: ISummarizer
    """A function for summarizing the result of processing."""


_PROCESSES: Dict[SubmissionContent.Format, SourceProcess] = {}


class SourceProcessingException(RuntimeError):
    """Base exception for this module."""


class FailedToCheckStatus(SourceProcessingException):
    """Could not check the status of processing."""


class NoProcessToCheck(SourceProcessingException):
    """Attempted to check a process that does not exist."""


class FailedToStart(SourceProcessingException):
    """Could not start processing."""


class FailedToGetResult(SourceProcessingException):
    """Could not get the result of processing."""


class BaseStarter:
    """
    Base class for starting processing.

    To extend this class, override :func:`BaseStarter.start`. That function
    should perform whatever steps are necessary to start processing, and
    return a :const:`.Status` that indicates the disposition of
    processing for that submission.
    """

    def start(self, submission: Submission, token: str) -> Status:
        """Start processing the source. Must be implemented by child class."""
        raise NotImplementedError('Must be implemented by a child class')

    def on_success(self, submission: Submission, token: str) -> None:
        """Callback for successful start. May be overridden by child class."""
        pass

    def on_failure(self, submission: Submission, exc: Exception) -> None:
        """Callback for failed start. May be overridden by child class."""
        pass

    def fail(self, submission: Submission, exc: Exception) -> None:
        """Handle failure to start processing."""
        self.on_failure(submission, exc)
        message = f'Could not start processing {submission.submission_id}'
        raise FailedToStart(message) from exc

    def __call__(self, submission: Submission, user: User,
                 client: Optional[Client], token: str) -> Status:
        """Start processing a submission source package."""
        try:
            status = self.start(submission, token)
            self.on_success(submission, token)
        except SourceProcessingException:   # Propagate.
            raise
        except Exception as e:
            self.fail(submission, e)
        return status


class BaseChecker:
    """
    Base class for checking the status of processing.

    To extend this class, override :func:`BaseStarter.check`. That function
    should return a :const:`.Status` that indicates the disposition of
    processing for a given submission.
    """

    def check(self, submission: Submission, token: str) -> Status:
        """Perform the status check."""
        raise NotImplementedError('Must be implemented by a subclass')

    def on_failure(self, submission: Submission, exc: Exception) -> None:
        """Failure callback. May be overridden by child class."""
        pass

    def fail(self, submission: Submission, exc: Exception) -> None:
        """Generate a failure exception."""
        self.on_failure(submission, exc)
        raise FailedToCheckStatus(f'Status check failed: {exc}') from exc

    def finish(self, submission: Submission, user: User,
               client: Optional[Client], token: str) -> None:
        """Emit :class:`.ConfirmSourceProcessed` on successful processing."""
        try:
            save(ConfirmSourceProcessed(creator=user, client=client),  # type: ignore
                 submission_id=submission.submission_id)
        except SaveError as e:
            self.fail(submission, e)

    def __call__(self, submission: Submission, user: User,
                 client: Optional[Client], token: str) -> Status:
        """Check the status of source processing for a submission."""
        if submission.is_source_processed:      # Already succeeded.
            return SUCCEEDED
        try:
            status = self.check(submission, token)
            if status == SUCCEEDED:
                self.finish(submission, user, client, token)
        except SourceProcessingException:   # Propagate.
            raise
        except Exception as e:
            self.fail(submission, e)
        return status


class BaseSummarizer:
    """
    Base class for summarizing the result of processing.

    To extend this class, override :func:`BaseStarter.summarize`. That function
    should return a :const:`.Summary` that can be used to provide feedback to
    a user or API consumer.
    """

    def on_failure(self, submission: Submission, exc: Exception) -> None:
        """Callback for failed summary. May be overridden by child class."""
        pass

    def fail(self, submission: Submission, exc: Exception) -> None:
        """Handle failure to get summary."""
        self.on_failure(submission, exc)
        message = f'Could not summarize processing {submission.submission_id}'
        raise FailedToGetResult(message) from exc

    def summarize(self, submission: Submission, token: str) -> Dict[str, Any]:
        """
        Generate summary information about the processing.

        Must be overridden by a child class.
        """
        raise NotImplementedError('Must be implemented by a child class')
        return {}

    def __call__(self, submission: Submission, user: User,
                 client: Optional[Client], token: str) -> Dict[str, Any]:
        """Summarize source processing."""
        p = PreviewService.current_session()
        try:
            summary = self.summarize(submission, token)
            preview = p.get_metadata(submission.source_content.identifier,
                                     submission.source_content.checksum,
                                     token)
            summary.update({'preview': preview})
        except SourceProcessingException:   # Propagate.
            raise
        except Exception as e:
            self.fail(submission, e)
        return summary


class _PDFStarter(BaseStarter):
    """Start processing a PDF source package."""

    def start(self, submission: Submission, token: str) -> Status:
        """Ship the PDF to the preview service."""
        m = Filemanager.current_session()
        stream, source_checksum, stream_checksum = \
            m.get_single_file(submission.source_content.identifier, token)
        if submission.source_content.checksum != source_checksum:
            raise FailedToStart('Source has changed')
        _ship_to_preview(submission, stream, stream_checksum, token)
        return IN_PROGRESS


class _PDFChecker(BaseChecker):
    """Check the status of a PDF source package."""

    def check(self, submission: Submission, token: str) -> Status:
        """Verify that the preview is present."""
        p = PreviewService.current_session()
        if p.has_preview(submission.source_content.identifier,
                         submission.source_content.checksum,
                         token):
            return SUCCEEDED
        return FAILED


class _PDFSummarizer(BaseSummarizer):
    """Summarize PDF processing."""

    def summarize(self, submission: Submission, token: str) -> Summary:
        """Currently does nothing."""
        return {}


class _CompilationStarter(BaseStarter):
    """Starts compilation via the compiler service."""

    def start(self, submission: Submission, token: str) -> Status:
        """Start compilation."""
        c = Compiler.current_session()
        stamp_label, stamp_link = self._make_stamp(submission)
        stat = c.compile(submission.source_content.identifier,
                         submission.source_content.checksum,
                         token,
                         stamp_label,
                         stamp_link,
                         force=True)
        if stat.is_failed:
            raise FailedToStart(f'Failed to start: {stat.Reason.value}')
        return IN_PROGRESS

    def _make_stamp(self, submission: Submission) -> Tuple[str, str]:   # label, URL
        # Create label and link for PS/PDF stamp/watermark.
        #
        # Stamp format for submission is of form [identifier category date]
        #
        # "arXiv:submit/<submission_id>  [<primary category>] DD MON YYYY
        #
        # Date segment is optional and added automatically by converter.
        #
        stamp_label = f'arXiv:submit/{submission.submission_id}'

        if submission.primary_classification \
                    and submission.primary_classification.category:
            # Create stamp label string - for now we'll let converter
            #                             add date segment to stamp label
            primary_category = submission.primary_classification.category
            stamp_label = f'{stamp_label} [{primary_category}]'

        stamp_link = f'/{submission.submission_id}/preview.pdf'
        return stamp_label, stamp_link


class _CompilationChecker(BaseChecker):
    def _get_preview(self, submission: Submission, token: str) \
            -> Tuple[IO[bytes], str]:
        c = Compiler.current_session()
        product = c.get_product(submission.source_content.identifier,
                                submission.source_content.checksum,
                                token)
        return product.stream, product.checksum

    def check(self, submission: Submission, token: str) -> Status:
        c = Compiler.current_session()
        try:
            compilation = c.get_status(submission.source_content.identifier,
                                       submission.source_content.checksum,
                                       token)
        except NotFound as e:     # Nothing to do.
            raise NoProcessToCheck('No compilation process found') from e
        if compilation.is_succeeded:
            stream, stream_checksum = self._get_preview(submission, token)
            _ship_to_preview(submission, stream, stream_checksum, token)
            return SUCCEEDED
        elif compilation.is_failed:
            return FAILED
        return IN_PROGRESS


class _CompilationSummarizer(BaseSummarizer):
    def summarize(self, submission: Submission, token: str) -> Summary:
        c = Compiler.current_session()
        log = c.get_log(submission.source_content.identifier,
                        submission.source_content.checksum,
                        token)
        return {'log_output': log.stream.read().decode('utf-8')}


def _ship_to_preview(submission: Submission, stream: IO[bytes],
                     preview_checksum: str, token: str) -> None:
    p = PreviewService.current_session()
    p.deposit(submission.source_content.identifier,
              submission.source_content.checksum,
              stream, token, overwrite=True)


def _make_process(supports: SubmissionContent.Format,
                  starter: BaseStarter,
                  checker: BaseChecker,
                  summarizer: BaseSummarizer) -> SourceProcess:

    proc = SourceProcess(supports, starter, checker, summarizer)
    _PROCESSES[supports] = proc
    return proc


def _get_process(source_format: SubmissionContent.Format) -> SourceProcess:
    proc = _PROCESSES.get(source_format, None)
    if proc is None:
        raise NotImplementedError(f'No process found for {source_format}')
    return proc


def start(submission: Submission, user: User, client: Optional[Client],
          token: str) -> Status:
    """
    Start processing the source package for a submission.

    Parameters
    ----------
    submission : :class:`.Submission`
        The submission to process.
    user : :class:`.User`
        arXiv user who originated the request.
    client : :class:`.Client` or None
        API client that handled the request, if any.
    token : str
        Authn/z token for the request.

    Returns
    -------
    str
        Status indicating the disposition of the process. See :const:`.Status`.

    Raises
    ------
    :class:`NotImplementedError`
        Raised if the submission source format is not supported by this module.

    """
    proc = _get_process(submission.source_content.source_format)
    return proc.start(submission, user, client, token)


def check(submission: Submission, user: User, client: Optional[Client],
          token: str) -> Status:
    """
    Check the status of source processing for a submission.

    Parameters
    ----------
    submission : :class:`.Submission`
        The submission to process.
    user : :class:`.User`
        arXiv user who originated the request.
    client : :class:`.Client` or None
        API client that handled the request, if any.
    token : str
        Authn/z token for the request.

    Returns
    -------
    str
        Status indicating the disposition of the process. See :const:`.Status`.

    Raises
    ------
    :class:`NotImplementedError`
        Raised if the submission source format is not supported by this module.

    """
    proc = _get_process(submission.source_content.source_format)
    return proc.check(submission, user, client, token)


def summarize(submission: Submission, user: User, client: Optional[Client],
              token: str) -> Summary:
    """
    Summarize the results of source processing for a submission.

    Parameters
    ----------
    submission : :class:`.Submission`
        The submission to process.
    user : :class:`.User`
        arXiv user who originated the request.
    client : :class:`.Client` or None
        API client that handled the request, if any.
    token : str
        Authn/z token for the request.

    Returns
    -------
    dict
        Keys are strings. Summary information suitable for generating feedback
        to an end user or API consumer. E.g. to be injected in a template
        rendering context.

    Raises
    ------
    :class:`NotImplementedError`
        Raised if the submission source format is not supported by this module.

    """
    proc = _get_process(submission.source_content.source_format)
    return proc.summarize(submission, user, client, token)


TeXProcess = _make_process(
    SubmissionContent.Format.TEX,
    _CompilationStarter(),
    _CompilationChecker(),
    _CompilationSummarizer()
)
"""Support for processing TeX submissions."""


PostscriptProcess = _make_process(
    SubmissionContent.Format.POSTSCRIPT,
    _CompilationStarter(),
    _CompilationChecker(),
    _CompilationSummarizer()
)
"""Support for processing Postscript submissions."""


PDFProcess = _make_process(
    SubmissionContent.Format.PDF,
    _PDFStarter(),
    _PDFChecker(),
    _PDFSummarizer()
)
"""Support for processing PDF submissions."""
