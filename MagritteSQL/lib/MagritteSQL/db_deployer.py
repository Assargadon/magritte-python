from sqlalchemy import create_engine
from sqlalchemy import Engine
from typing import Any
from Magritte.MAContainer_class import MAContainer

class DbDeployer:

    def __init__(self):
        self.engines = []
        self.tables = []

    """
    Adds new engine to engine list of the DbDeployer. Engine is basically a db connection

    :param self: instance object itself
    :param str connline: connection line to connect db, would be passed directly to SQLAlchemy
    :param Any kwargs: any additional engine options, would be passed directly to SQLAlchemy
    :return: None
    :raises Exception: any exception that SQLAlchemy raise
    """
    def add_engine(self, connline: str, **kwargs: Any) -> None:
        self.engines.append(create_engine(connline, kwargs))

    """
    Adds new table to table list of the DbDeployer. The table is described with Magritte description

    :param self: instance object itself
    :param MAContainer magrittedescription: the table magritte description to be added
    :return: None
    :raises Exception: any exception that MAContainer members raise
    :raises Exception: invalid magritte description
    """
    def add_table(self, magrittedescription: MAContainer) -> None:
        pass

    """
    Deploys table list to all engines of the engine list

    :param self: instance object itself
    :return: None
    :raises Exception: any exception that SQLAlchemy raise
    :raises Exception: no engines were specified
    :raises Exception: no tables were specified
    """
    def deploy_db(self) -> None:
        pass
