class FolderExistsError(Exception):
    """
    Error when trying to create a folder that already exists.
    """
    pass


class InvalidCredentialsError(Exception):
    """
    Error if user put in invalid credentials for creating Token object.
    """
    pass


class NoChildrenError(Exception):
    """
    Error when trying to get children from a folder that has no children.
    """
    pass


class ItemNotFoundError(Exception):
    """
    Error if item requested was not found.
    There is already a builtin FileNotFoundError, but that refers to local
    files so it's not appropriate to use it if an item was not found in ShareFile.
    """
    pass


class LinkNotAcquiredError(Exception):
    """
    Error for when trying to create share link for item in ShareFile but there was a problem in getting of link.
    """
    pass


class UploadFailedError(Exception):
    """
    Error when an upload of a file fails.
    """
    pass


class ExcelValueError(Exception):
    """
    Error when trying to access or change a value in the excel sheet and it doesn't exist.
    """
    pass
