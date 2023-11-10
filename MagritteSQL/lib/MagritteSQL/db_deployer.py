from sqlalchemy import create_engine
from sqlalchemy import Engine
from typing import Any
from typing import Self
from Magritte.MAContainer_class import MAContainer

class DbDeployer:

    def __init__(self, engine: Engine):
        self.engine = engine
        self.models: dict = {}

    @classmethod
    def create_db_deployer(self, connline: str, **kwargs: Any) -> Self:
        engine = create_engine(connline, **kwargs)
        return DbDeployer(engine)

    def register_model(self, magrittedescription: MAContainer) -> None:
        pass

    def deploy_table(self, model_name: str) -> None:
        pass

    def deploy_db(self) -> None:
        pass
