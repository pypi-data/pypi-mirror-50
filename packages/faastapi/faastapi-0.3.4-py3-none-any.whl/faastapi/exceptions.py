"""

"""


class MissingDependencyError(ImportError):
    def __init__(self, missing_package: str, extra: str, *args, **kwargs):
        super().__init__(
            f"Package '{missing_package}' is not installed. "
            "You can install it with all required dependencies using the following command:\n"
            f"'pip install faastapi[{extra}]'",
            *args,
            **kwargs,
        )
