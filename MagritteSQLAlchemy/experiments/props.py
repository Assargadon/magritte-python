from sqlalchemy import Table, Column, Integer, String, create_engine
from sqlalchemy.orm import registry, Session


class TClass:
    def __init__(self):
        self._prop = None

    @property
    def prop(self):
        return self._prop

    @prop.setter
    def prop(self, value):
        self._prop = value

    '''
    def __getattr__(self, item):
        print(f"Entering {self.__class__}.__getattr__({item})")
        if item == 'prop':
            return self.get_prop()
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
    '''


def my_log(fn):
    def wrapper(*args, **kwargs):
        print(f"Entering {fn.__name__} with args = {args} and kwargs = {kwargs}.")
        res = fn(*args, **kwargs)
        print(f"Exiting {fn.__name__}.")
        return res
    return wrapper


mapper_registry = registry()

t_table = Table(
    "tclass",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("prop", Integer),
    )


if __name__ == "__main__":

    getattr = my_log(getattr)
    TClass.__getattribute__ = my_log(TClass.__getattribute__)

    '''
    obj = TClass()

    print(" =========================== Before mapping: =========================")

    print(" ============== Before prop assignment ==============")
    print(f"obj.__dict__ = {obj.__dict__}")
    obj.prop = 42
    print(" ============== After prop assignment ==============")
    print(f"obj.__dict__ = {obj.__dict__}")

    print(" ============== Retrieving prop ==============")
    print(f"obj.prop = {obj.prop}")
    print(f"obj.prop = {getattr(obj, 'prop')}")
    print(f"obj._prop = {obj._prop}")
    
    '''

    mapper_registry.map_imperatively(
        TClass,
        t_table,
        properties={
            "_prop": t_table.c.prop,
            # "prop": t_table.c.prop,
            },
        )

    obj = TClass()

    print(" =============================== After mapping: ================================")

    print(" ============== Before prop assignment ==============")
    print(f"obj.__dict__ = {obj.__dict__}")
    obj.prop = 42
    print(" ============== After prop assignment ==============")
    print(f"obj.__dict__ = {obj.__dict__}")

    print(" ============== Retrieving prop ==============")
    print(f"obj.prop = {obj.prop}")
    print(f"obj.prop = {getattr(obj, 'prop')}")
    print(f"obj._prop = {obj._prop}")

    print(" =========================== Before creating scheme in Database: =========================")

    engine = create_engine("sqlite://", echo=True)
    mapper_registry.metadata.create_all(engine)

    print(" =========================== Before saving data to Database: =========================")

    with Session(engine) as session:
        session.add(obj)
        session.commit()

    print(" =========================== After saving data to Database: =========================")

    with Session(engine) as session:
        obj = session.query(TClass).first()
        print(f"obj.prop = {obj.prop}")
        print(f"obj._prop = {obj._prop}")
        print(f"obj.__dict__ = {obj.__dict__}")
