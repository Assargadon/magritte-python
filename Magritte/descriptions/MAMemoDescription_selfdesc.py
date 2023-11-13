from sys import intern

from descriptions.MANumberDescription_class import MANumberDescription


def magritteDescription(self, parentDescription):
    desc = parentDescription

    desc += MANumberDescription(label='Number of Lines', priority=400, default=self.defaultLineCount(), accessor=intern('lineCount'))

    return desc
