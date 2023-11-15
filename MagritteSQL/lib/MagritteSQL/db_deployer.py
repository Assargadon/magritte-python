from sqlalchemy import create_engine
from sqlalchemy import Engine
from typing import Any
from typing import Self
from Magritte.MAContainer_class import MAContainer

from MagritteSQL.lib.MagritteSQL.sqlalchemy_model_writer import SQLAlchemyModelWriter

class DbDeployer:

    def __init__(self, engine: Engine):
        self.engine = engine
        self.models: dict = {}

    @classmethod
    def create_db_deployer(self, connline: str, **kwargs: Any) -> Self:
        engine = create_engine(connline, **kwargs)
        return DbDeployer(engine)

    def register_model(self, magrittedescription: MAContainer) -> None:
        model = SQLAlchemyModelWriter.write_model(magrittedescription)
        modelname = model.__tablename__
        self.models[modelname] = model

    def register_models(self, magrittedescriptions: list[MAContainer]) -> None:
        for description in magrittedescriptions:
            self.register_model(description)

    def get_registered_model(self, modelname: str):
        if modelname in self.models:
            return self.models[modelname]
        else:
            raise KeyError("Model '{model}' wasn't registered".format(model=modelname))

    def deploy_table(self, modelname: str) -> None:
        if modelname in self.models:
            self.models[modelname].metadata.create_all(self.engine)
        else:
            raise KeyError("Model '{model}' wasn't registered".format(model=modelname))

    def deploy_db(self) -> None:
        for model in self.models:
            self.deploy_table(model)
