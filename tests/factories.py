import random

import factory
import factory.fuzzy

from my_api.models import Investments, TibiaHuntAnalyser
from my_api.utils.get_current_datetime import get_current_datetime_formatted


class InvestmentFactory(factory.Factory):
    class Meta:
        model = Investments

    id = factory.fuzzy.FuzzyText(length=10)
    name = factory.fuzzy.FuzzyText(length=10)
    value = factory.fuzzy.FuzzyDecimal(low=0.0, high=100000.0)
    created_at = factory.fuzzy.FuzzyDate(start_date='-30d', end_date='today')


class TibiaHuntAnalyserFactory(factory.Factory):
    class Meta:
        model = TibiaHuntAnalyser

    loot = 10000
    waste = 5000
    id = "1",
    balance = loot - waste,
    created_at = get_current_datetime_formatted(),
    duration = 30000,
    experience = 10000,
    raw_xp_gain = 5000,
    xp_gain = 7500,
    level = 20,
    vocation = 'ELITE_KNIGHT',
    world = factory.LazyAttribute(random.choice(['Honbra', 'Vunira', 'Serdebra'])),
    loot = loot,
    waste = waste,
    start_date = factory.LazyAttribute(get_current_datetime_formatted()),
    end_date = factory.LazyAttribute(get_current_datetime_formatted()),
