from sqlmodel import Field, SQLModel


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    price: float = Field()
    deadline: str = Field()