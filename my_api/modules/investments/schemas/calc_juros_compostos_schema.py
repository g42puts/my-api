from pydantic import BaseModel


class JurosCompostosSchema(BaseModel):
    months: int
    amount: int
    monthly_investment: int
    year_tax: float
    variated_investments: list[dict] = []
