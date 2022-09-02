from pydantic import BaseModel, Field


class CreatePlayerForm(BaseModel):
    name: str = Field(
        ...,
        example="Lebron James",
        description="The name of the player",
        min_length=3,
        max_length=50,
    )


class RegisterThrowsForm(BaseModel):
    id: str
    num_scored: int = Field(ge=0)
    num_missed: int = Field(ge=0)
