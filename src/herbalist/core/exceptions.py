"""Custom exceptions for Herbalist AI pipeline."""

class HerbalistError(Exception):
    """Base exception for all Herbalist AI runtime errors."""
    pass


class DataValidationError(HerbalistError):
    """Raised when dataset schema, file formats, or split ratios are invalid."""
    pass


class CorruptImageError(DataValidationError):
    """Raised when an image cannot be read, decoded, or has invalid dimensions."""
    pass


class HardwareError(HerbalistError):
    """Raised when hardware requirements or resource constraints are violated."""
    pass


class ModelNotLoadedError(HerbalistError):
    """Raised when inference or fine-tuning is attempted without a compiled model."""
    pass


class CheckpointError(HerbalistError):
    """Raised when loading or saving model weights/checkpoints fails."""
    pass


class ConfigurationError(HerbalistError):
    """Raised when configuration YAML files are malformed or missing required keys."""
    pass
