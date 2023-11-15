from MagritteSQL.lib.MagritteSQL.sqlalchemy_model_visitor import SQLAlchemyModelVisitor

class SQLAlchemyModelWriter:
    @classmethod
    def write_model(self, model):
        visitor = SQLAlchemyModelVisitor()
        visitor.convert(model)
        return visitor.sqlAlchemyTableType
