"""
    Custom exception handler for empty tables
    [Missing module docstring without this]
"""

class EmptyEntityError(Exception):
    """
        Custom exception handler for empty tables
        [Missing class docstring without this]
    """
    code:str = ''
    description = None

    def __init__(self, description, code:str, *args):
        super().__init__(args)
        self.code = code
        self.description = description
