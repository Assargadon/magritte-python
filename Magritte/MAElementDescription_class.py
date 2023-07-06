
from MADescription_class import MADescription

class MAElementDescription(MADescription):

    def default(self):
        default_attr = 'default'
        if hasattr(self, default_attr):
            return getattr(self, default_attr)
        else:
            return self.defaultDefault()

    def default(self, aDefault):
        default_attr = 'default'
        setattr(self, default_attr, aDefault)
