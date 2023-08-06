# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Exceptions thrown by AutoML."""
from typing import cast, Optional, Type, TypeVar
from ._error_response_constants import ErrorCodes


ExceptionT = TypeVar('ExceptionT', bound=BaseException)


class ErrorTypes:
    """Possible types of errors."""

    User = 'User'
    Service = 'Service'
    Client = 'Client'
    Resource = 'Resource'
    Unclassified = 'Unclassified'
    All = {User, Service, Client, Resource, Unclassified}


class AutoMLException(Exception):
    """Exception with an additional field specifying what type of error it is."""

    error_type = ErrorTypes.Unclassified

    def __init__(self, message="", error_type=ErrorTypes.Unclassified, target=None):
        """
        Construct a new AutoMLException.

        :param error_type: type of the exception.
        :param message: details on the exception.
        """
        super().__init__(message)
        self.error_type = error_type
        self._target = target

    @classmethod
    def from_exception(cls: 'Type[ExceptionT]', e: BaseException, msg: Optional[str] = None) -> ExceptionT:
        """Convert an arbitrary exception to this exception type."""
        if not msg and isinstance(e, cls):
            return cast(ExceptionT, e)
        return cast(ExceptionT, cls(msg or str(e)).with_traceback(e.__traceback__))

    def get_error_type(self):
        """Get the error code for this exception."""
        return getattr(self, "_error_code", self.error_type)


class DataException(AutoMLException):
    """
    Exception related to data validations.

    :param message: Details on the exception.
    """

    _error_code = ErrorCodes.INVALIDDATA_ERROR

    def __init__(self, message="", target=None):
        """
        Construct a new DataException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.User, target)


class ConfigException(AutoMLException):
    """
    Exception related to invalid user config.

    :param message: Details on the exception.
    """

    _error_code = ErrorCodes.VALIDATION_ERROR

    def __init__(self, message="", target=None):
        """
        Construct a new ConfigException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.User, target)


class ArgumentException(AutoMLException):
    """
    Exception related to invalid user config.

    :param message: Details on the exception.
    """

    _error_code = ErrorCodes.VALIDATION_ERROR

    def __init__(self, message="", target=None):
        """
        Construct a new ConfigException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.User, target)


class ServiceException(AutoMLException):
    """
    Exception related to JOS.

    :param message: Details on the exception.
    """

    _error_code = ErrorCodes.SYSTEM_ERROR

    def __init__(self, message="", target=None):
        """
        Construct a new ServiceException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.Service, target)


class ClientException(AutoMLException):
    """
    Exception related to client.

    :param message: Details on the exception.
    """

    _error_code = ErrorCodes.SYSTEM_ERROR

    def __init__(self, message="", target=None):
        """
        Construct a new ClientException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.Client, target)


class ResourceException(AutoMLException):
    """
    Exception related to resource usage.

    :param message: Details on the exception.
    """

    def __init__(self, message="", target=None):
        """
        Construct a new ResourceException.

        :param message: details on the exception.
        """
        super().__init__(message, ErrorTypes.Resource, target)


class OnnxConvertException(ClientException):
    """Exception related to ONNX convert."""

    # TODO - define a code for this
    # _error_code = ErrorCodes.ONNX_ERROR


class DataprepException(ClientException):
    """Exceptions related to Dataprep."""

    # TODO - define a code for this
    # _error_code = ErrorCodes.DATAPREPVALIDATION_ERROR
