class ConvertTax:
    def year_tax_to_month_tax(self, tax: float) -> float:
        return round(((1 + tax) ** (1 / 12)), 6)

    def month_tax_to_year_tax(self, tax: float) -> float:
        return round(((1 + tax) ** 12), 6)


# if __name__ == '__main__':
#     print(ConvertTax().year_tax_to_month_tax(0.12))
#     print(ConvertTax().month_tax_to_year_tax(0.01))
