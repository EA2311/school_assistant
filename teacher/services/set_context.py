def set_context(context: dict, **kwargs) -> dict:
    """Gets context data dict with kwargs. Pass kwargs into context and return it."""
    if kwargs:
        for key, value in kwargs.items():
            context[key] = value

    return context
