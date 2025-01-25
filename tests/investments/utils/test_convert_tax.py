from my_api.modules.investments.utils.ConvertTax import (
    ConvertTax,
)


def test_year_tax_to_month_tax_should_return_month_tax():
    result = ConvertTax().year_tax_to_month_tax(0.12)
    assert result == 1.009489


def test_month_tax_to_year_tax_should_return_year_tax():
    result = ConvertTax().month_tax_to_year_tax(0.01)
    assert result == 1.126825
