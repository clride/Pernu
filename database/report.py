## User friendly way to return information to the frontend

class Report():
    is_error = False
    information = ""

    def __init__(self, is_error: bool = False, information: str = "") -> None:
        self.is_error = is_error
        self.information = information