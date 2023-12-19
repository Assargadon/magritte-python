
from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.MAModel_class import MAModel


class MAModelCheetahTemplateAdapterVisitor2(MAVisitor):
    def __init__(self, model):
        self.model = model
        self.result = None

    def visitReferenceDescription(self, description):
        childModel = MAModel.readUsingWrapper(self.model, description)
        self.result = MAModelCheetahTemplateAdapter(childModel, description)

    def visitToOneRelationDescription(self, description):
        childModel = MAModel.readUsingWrapper(self.model, description)
        childDescription = description.reference
        self.result = MAModelCheetahTemplateAdapter(childModel, childDescription)

    def visitElementDescription(self, description):
        self.result = description.writeString(self.model)

    def visitDescription(self, description):
        self.result = MAModel.readUsingWrapper(self.model, description)

class MAModelCheetahTemplateAdapterVisitor1(MAVisitor):
    def __init__(self, model, item):
        self.model = model
        self.item = item
        self.result = None

    def visitToManyRelationDescription(self, description):
        childModel = self.model[self.item]
        childDescription = description.reference
        self.result = MAModelCheetahTemplateAdapter(childModel, childDescription)

    def visitContainer(self, description):
        children = description.children
        childDescription = next(d for d in children if d.name == self.item)
        if childDescription is None:
            raise AttributeError()
        visitor = MAModelCheetahTemplateAdapterVisitor2(self.model)
        childDescription.acceptMagritte(visitor)
        self.result = visitor.result

    def visitToOneRelationDescription(self, description):
        childModel = MAModel.readUsingWrapper(self.model, description)
        childDescription = description.reference
        visitor = MAModelCheetahTemplateAdapterVisitor2(childModel)
        childDescription.acceptMagritte(visitor)
        self.result = visitor.result

    def visitDescription(self, description):
        raise AttributeError()

class MAModelCheetahTemplateAdapter:

    def __init__(self, model, description):
        self.model = model
        self.description = description

    #def __getattr__(self, item):

    def __len__(self):
        return len(self.model)

    def __getitem__(self, item):
        visitor = MAModelCheetahTemplateAdapterVisitor1(self.model, item)
        self.description.acceptMagritte(visitor)
        return visitor.result

    def __str__(self):
        visitor = MAModelCheetahTemplateAdapterVisitor2(self.model)
        self.description.acceptMagritte(visitor)
        return visitor.result