import re

class RegexHelper:
    """
    Defines regex helper methods.
    """

    @staticmethod
    def is_match(pattern: str, string: str, flag: int = 0) -> bool:
        """
        Returns `True` or `False` if a regex match has been found in the string.
        """
        if re.match(pattern, string, flag) is not None:
            return True
        else:
            return False