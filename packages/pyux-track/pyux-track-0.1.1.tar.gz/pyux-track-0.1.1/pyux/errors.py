
class ColorValueError(ValueError):
    """Exception when color is not available for ColourPen"""
    pass


class StyleValueError(ValueError):
    """Exception when style is not available for ColourPen"""
    pass


class NoDurationsError(ValueError):
    """Exception when durations were not computed in Chronos"""
    pass


class DelayTypeError(TypeError):
    """Exception when no delay was given to Timer"""
    pass
