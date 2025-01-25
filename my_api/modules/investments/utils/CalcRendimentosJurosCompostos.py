from my_api.modules.investments.utils.ConvertTax import (
    ConvertTax,
)


class CalcRendimentosJurosCompostos(ConvertTax):
    def __init__(self, months: int, amount: int, monthly_investment: int, year_tax: float):
        self.meses = months
        self.montante = amount
        self.aporte_mensal = monthly_investment
        self.year_tax = year_tax
        self.month_tax = self.year_tax_to_month_tax(year_tax)

    def execute(self, variated_investments: list = []):
        rendimentos: list = [{
            'mes': 0,
            'montante': self.montante,
            'aporte_mensal': 0,
            'total_aportado': 0,
            'rendimento_mes': round(self.montante * (self.month_tax - 1), 2),
            'rendimento_total': round(self.montante * (self.month_tax - 1), 2),
        }]

        for mes in range(1, self.meses):
            variacao_aporte_mensal: float = 0
            for x in variated_investments:
                if x['mes'] == mes:
                    variacao_aporte_mensal = x['aporte_mensal']

            self.montante = round(self.montante + (self.montante * (self.month_tax - 1)) + (self.aporte_mensal + variacao_aporte_mensal), 2)
            rendimentos.append({
                'mes': mes,
                'montante': self.montante,
                'aporte_mensal': self.aporte_mensal + variacao_aporte_mensal,
                'total_aportado': sum(mes['total_aportado'] for mes in rendimentos[0: mes + 1]) + (self.aporte_mensal + variacao_aporte_mensal),
                'rendimento_mes': round(self.montante * (self.month_tax - 1), 2),
                'rendimento_total': round(sum([mes['rendimento_mes'] for mes in rendimentos[0: mes + 1]], (self.montante * (self.month_tax - 1))), 2),
            })

        return rendimentos

    # def calc_juros_compostos_default(self, montante: float, tax: int, meses: int):
    #     return montante * ((1 + tax / 100) ** meses)


# if __name__ == '__main__':
#     variated_investments = [
#         {'mes': 2, 'aporte_mensal': -100},
#         {'mes': 3, 'aporte_mensal': 400}
#     ]
#     result = CalcRendimentosJurosCompostos(months=4, amount=200, monthly_investment=600, year_tax=0.1215).execute(variated_investments)
#     for x in result:
#         print(x)
