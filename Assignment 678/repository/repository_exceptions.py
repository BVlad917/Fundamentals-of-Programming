class RepositoryException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class AddException(RepositoryException):
    def __init__(self, msg):
        super().__init__(msg)


class DeleteException(RepositoryException):
    def __init__(self, msg):
        super().__init__(msg)
