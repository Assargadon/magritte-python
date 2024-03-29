import inspect

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, relationship, Session
from sqlalchemy import create_engine

mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
    )

address_table = Table(
    "address",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("email_address", String(50)),
    )


class User:
    def __init__(self, *, name, fullname, nick, password):
        self.name = name
        self.fullname = fullname
        self.nick = nick
        self.addresses = []
        self.password = password

    @property
    def descriptive_label(self):
        return f"{self.name} ({self.nick})"


class Address:
    def __init__(self, *, email_address):
        self.email_address = email_address


def my_repr(obj):
    res = f"{obj.__class__.__name__}:\n"
    res += f"{repr(obj)}\n"
    for k in dir(obj):
        if k.find("__") != 0:
            res += f"  {k} = {getattr(obj, k)}\n"
    return res


if __name__ == "__main__":

    print(f" ============== Model classes before mapping: ==============")
    print(f"dir(User) = {dir(User)}")
    print(f"dir(Address) = {dir(Address)}")

    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            "addresses": relationship(
                Address,
                back_populates="user",
                ),
            "nick": user_table.c.nickname,
            },
        )

    mapper_registry.map_imperatively(
        Address,
        address_table,
        properties={
            "user": relationship(
                User,
                )
            },
        )

    print(f" ============== Model classes after mapping: ==============")
    print(f"dir(User) = {dir(User)}")
    print(f"dir(Address) = {dir(Address)}")

    print(f" ============== Initializing user, address1 instances: ==============")

    user = User(name="John", fullname="John Doe", nick="jdoe", password="12345")
    address1 = Address(email_address="jdoe@acme.org")

    print(my_repr(address1))
    print(my_repr(user))

    print(f" ============== Appending address1 to user.addresses: ==============")

    user.addresses.append(address1)

    print(my_repr(address1))
    print(my_repr(user))

    print(f" ============== Initializing/appending address2 instance: ==============")


    user.addresses.append(Address(email_address="jdoe@yahoo.com"))

    print(my_repr(user.addresses[-1]))
    print(my_repr(user))

    print(f" ============== Initializing engine, creating tables: ==============")

    engine = create_engine("sqlite://", echo=True)

    mapper_registry.metadata.create_all(engine)
    mapper_registry.metadata

    print(f" ============== Adding user to database: ==============")

    with Session(engine) as session:
        session.add_all([user])
        session.commit()

    print(f" ============== Querying user from database: ==============")

    with Session(engine) as session:
        user = session.query(User).first()
        print(my_repr(user))

        print(" ========== User addresses ==========")
        print(my_repr(user.addresses[0]))
        print(my_repr(user.addresses[1]))

    user2 = User(name="Jane", fullname="Jane Doe", nick="jane", password="12345")
    user.addresses[0].user = user2

    print(" ========== Moving address1 to user2 ==========")

    user2.addresses.append(user.addresses[0])

    print(" ========== User1 & User2  ==========")

    print(my_repr(user))
    print(my_repr(user2))

    print(f" ============== Adding address1 to database: ==============")
    with Session(engine) as session:
        session.add(user.addresses[0])
        session.commit()

    print(f" ============== Querying user from database: ==============")
    with Session(engine) as session:
        user = session.query(User).first()
        print(my_repr(user))
        print(" ========== User1 addresses ==========")
        print(my_repr(user.addresses[0]))
        # print(my_repr(user.addresses[1]))

        user = session.query(User).filter_by(name="Jane").first()
        print(my_repr(user))
        print(" ========== User2 addresses ==========")
        print(my_repr(user.addresses[0]))
        # print(my_repr(user.addresses[1]))