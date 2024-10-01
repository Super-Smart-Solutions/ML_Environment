class ModelNotFoundError(Exception):
    """Custom exception class raised when the model is not found."""
    def __init__(self, message="Model Not Found"):
        self.message = message
        super().__init__(self.message)


class ImageProcessingError(Exception):
    """Custom exception class raised when the image is unprocessable."""
    def __init__(self, message="Image processing error"):
        self.message = message
        super().__init__(self.message)

class ModelLoadingError(Exception):
    """Custom exception class raised when the model fails to load."""
    def __init__(self, message="model loading error"):
        self.message = message
        super().__init__(self.message)
