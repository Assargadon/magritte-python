
class MAModelCheetahTemplateAdapter:

    def __init__(self, model, description):
        self.model = model
        self.description = description

    #def __getattr__(self, item):

    def __len__(self):
        return len(self.model)

    def __getitem__(self, item):
        from descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
        if isinstance(self.description, MAToManyRelationDescription):
            childModel = self.model[item]
            childDescription = self.description.reference
            adapter = MAModelCheetahTemplateAdapter(childModel, childDescription)
            return adapter
        else:
            from MAModel_class import MAModel
            from descriptions.MAElementDescription_class import MAElementDescription
            from descriptions.MAContainer_class import MAContainer
            from descriptions.MAReferenceDescription_class import MAReferenceDescription
            if isinstance(self.description, MAContainer):
                children = self.description.children
                childDescription = next(d for d in children if d.name == item)
                if isinstance(childDescription, MAReferenceDescription):
                    childModel = MAModel.readUsingWrapper(self.model, childDescription)
                    adapter = MAModelCheetahTemplateAdapter(childModel, childDescription)
                    return adapter
                elif isinstance(childDescription, MAElementDescription):
                    return childDescription.writeString(self.model)
                else:
                    return MAModel.readUsingWrapper(self.model, childDescription)
            raise AttributeError()