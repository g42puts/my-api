from pydantic import BaseModel, ConfigDict


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
    model_config = ConfigDict(from_attributes=True)
