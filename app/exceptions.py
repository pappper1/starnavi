from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal Server Error"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ExpiredTokenException(BaseException):

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Expired token"


class TokenAbsentException(BaseException):

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is absent"


class IncorrectTokenFormatException(BaseException):

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(BaseException):

    status_code = status.HTTP_401_UNAUTHORIZED


class UserAlreadyExistsException(BaseException):

    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectEmailOrPasswordException(BaseException):

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class UserNotFoundException(BaseException):

    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class FileNotAnImageException(BaseException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "File is not an image"


class PostNotFoundException(BaseException):

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Post not found"


class AccessForbiddenException(BaseException):

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Access forbidden"


class CommentNotFoundException(BaseException):

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Comment not found"


class AnalyticsNotFoundException(BaseException):

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Analytics not found"


class FoulLanguageException(BaseException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Foul language is not allowed"
