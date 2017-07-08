class ScaleData:
    """
    Scale Data model
    """
    def __init__(self, identifier, calculated=False):
        self.id = identifier
        self.calculated = calculated
        self.units = 'Lbs'
        self.weight = 0
        self.percent = 0
        self.widget = None

