from app.exceptions import AppException


class TravelProjectNotFoundError(AppException):
    pass


class CannotDeleteWithVisitedPlacesError(AppException):
    pass
