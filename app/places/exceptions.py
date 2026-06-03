from app.exceptions import AppException


class ProjectPlaceNotFoundError(AppException):
    pass


class PlaceValidationError(AppException):
    pass


class MaxPlacesExceededError(AppException):
    pass


class DuplicatePlaceInProjectError(AppException):
    pass
