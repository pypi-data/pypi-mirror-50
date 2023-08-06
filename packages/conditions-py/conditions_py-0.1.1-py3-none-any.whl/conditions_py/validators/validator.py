class Validator:
    """
    Base validation class.
    """

    def __init__(self, value, argument_name):
        """
        Constructor which initializes the validator with a `value` and `argument_name`
        """
        self.value = value
        self.argument_name = argument_name