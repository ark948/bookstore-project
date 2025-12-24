class NegativeIntegerConverter:
    regex = '-1|0|1'

    def to_python(self, value):
        return int(value)
    
    def to_url(self, value):
        return str(value)