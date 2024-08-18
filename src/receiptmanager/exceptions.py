"""Custom exception names for better code error readability."""
class ConfigNotFoundError(FileNotFoundError):
    """
    Raised when the receiptmanager.config is missing
    """
    def __init__(self, message="receiptmanager.config is missing. Please ensure that the program_data folder and its contents are not being modified or accessed."):
        self.message = message
        super().__init__(self.message)
