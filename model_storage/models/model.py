from sqlmodel import Field, SQLModel


class BlendModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    vertices: int = Field()
    edges: int = Field()
    faces: int = Field()
    render_time: float = Field()
    is_ready: bool = Field(default=False)