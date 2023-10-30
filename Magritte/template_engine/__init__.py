
from Cheetah.Template import Template


class MAModelCheetahTemplateAdapter:

    def __init__(self, model, description):
        self.model = model
        self.description = description

    def respondTo(self, sTemplate):
        compiledTemplate = Template(sTemplate)
        compiledTemplate.magritteModel = self
        return compiledTemplate.respond()

    #def __getattr__(self, item):

    def __len__(self):
        return len(self.model)

    def __getitem__(self, item):
        from MAToManyRelationDescription_class import MAToManyRelationDescription
        if isinstance(self.description, MAToManyRelationDescription):
            childModel = self.model[item]
            childDescription = self.description.reference
            adapter = MAModelCheetahTemplateAdapter(childModel, childDescription)
            return adapter
        else:
            from MAModel_class import MAModel
            from MAContainer_class import MAContainer
            from MAReferenceDescription_class import MAReferenceDescription
            if isinstance(self.description, MAContainer):
                children = self.description.children
                childDescription = next(d for d in children if d.name == item)
                if isinstance(childDescription, MAReferenceDescription):
                    childModel = MAModel.readUsingWrapper(self.model, childDescription)
                    adapter = MAModelCheetahTemplateAdapter(childModel, childDescription)
                    return adapter
                else:
                    return MAModel.readUsingWrapper(self.model, childDescription)
            raise AttributeError()



