from app.exceptions import AppException


class ProjectPlaceNotFoundError(AppException):
    pass


class PlaceValidationError(AppException):
    pass
