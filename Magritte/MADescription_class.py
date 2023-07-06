
class MADescription:

    @classmethod
    def isAbstract(cls):
        return True

    def defaultDefault(self):
        return None

    def defaultKind(self):
        return object

    def defaultLabel(self):
        return ''

    def kind(self):
        kind_attr = 'kind'
        if hasattr(self, kind_attr):
            return getattr(self, kind_attr)
        else:
            return self.defaultKind()

    def label(self):
        label_attr = 'label'
        if hasattr(self, label_attr):
            return getattr(self, label_attr)
        else:
            return self.defaultLabel()

    def isSortable(self):
        return False
