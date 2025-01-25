from pydantic import BaseModel, ConfigDict


class TibiaHuntAnalyserSchema(BaseModel):
    character_name: str
    level: int
    vocation: str
    world: str
    experience: int
    raw_xp_gain: int
    xp_gain: int
    loot: int
    waste: int
    balance: int
    duration: int
    start_date: str
    end_date: str
    monsters_killeds: list[str] = None


class TibiaHuntAnalyserPublic(TibiaHuntAnalyserSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
