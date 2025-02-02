from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    full_name: str | None
    is_active: bool
    is_superuser: bool
    is_staff: bool
    is_verified: bool
    created_at: str
    updated_at: str | None
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class InvestmentsSchema(BaseModel):
    category: str
    sub_category: str
    apply_date: str
    end_date: str
    tax: float
    tax_period_type: str
    initial_value: int


class InvestmentsPublic(BaseModel):
    id: int
    category: str
    sub_category: str
    apply_date: str
    end_date: str
    tax: float
    tax_period_type: str
    initial_value: int
    model_config = ConfigDict(from_attributes=True)


class InvestmentsList(BaseModel):
    investments: list[InvestmentsPublic]


class JurosCompostosSchema(BaseModel):
    months: int
    amount: int
    monthly_investment: int
    year_tax: float
    variated_investments: list[dict] = []


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
    monsters_killeds: str


class UpdateTibiaHuntAnalyser(BaseModel):
    character_name: str | None = None
    level: int | None = None
    vocation: str | None = None
    world: str | None = None
    experience: int | None = None
    raw_xp_gain: int | None = None
    xp_gain: int | None = None
    loot: int | None = None
    waste: int | None = None
    balance: int | None = None
    duration: int | None = None
    start_date: str | None = None
    end_date: str | None = None
    monsters_killeds: str | None = None


class TibiaHuntAnalyserPublic(BaseModel):
    id: str
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
    created_at: str
    updated_at: str | None
    monsters_killeds: str
    model_config = ConfigDict(from_attributes=True)


class TibiaHuntAnalyserList(BaseModel):
    analysers: list[TibiaHuntAnalyserPublic]
