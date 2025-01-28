from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class TibiaHuntAnalyser:
    __tablename__ = 'tibia_global_analyser'

    id: Mapped[str] = mapped_column(primary_key=True)
    character_name: Mapped[str]
    level: Mapped[int]
    vocation: Mapped[str]
    world: Mapped[str]
    experience: Mapped[int]
    raw_xp_gain: Mapped[int]
    xp_gain: Mapped[int]
    loot: Mapped[int]
    waste: Mapped[int]
    balance: Mapped[int]
    duration: Mapped[int]
    start_date: Mapped[str]
    end_date: Mapped[str]
    created_at: Mapped[str]
    updated_at: Mapped[str] = mapped_column(init=False, nullable=True)
    monsters_killeds: Mapped[str] = mapped_column(default=None, nullable=True)


@table_registry.mapped_as_dataclass
class Investments:
    __tablename__ = 'investments'

    id: Mapped[str] = mapped_column(init=True, primary_key=True)
    category: Mapped[str]
    sub_category: Mapped[str]
    apply_date: Mapped[str]
    end_date: Mapped[str]
    tax: Mapped[float]
    tax_period_type: Mapped[str]
    initial_value: Mapped[int]
    created_at: Mapped[str]
    updated_at: Mapped[str] = mapped_column(default=None, nullable=True)
    deleted_at: Mapped[str] = mapped_column(default=None, nullable=True)


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'user'

    id: Mapped[str] = mapped_column(init=True, primary_key=True)
    username: Mapped[str] = mapped_column(init=True, unique=True)
    email: Mapped[str] = mapped_column(init=True, unique=True)
    password: Mapped[str] = mapped_column(init=True)
    created_at: Mapped[str] = mapped_column(init=True)
    full_name: Mapped[str] = mapped_column(init=False, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, init=False, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, init=False, nullable=True)
    is_staff: Mapped[bool] = mapped_column(default=False, init=False, nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False, init=False, nullable=True)
    updated_at: Mapped[str] = mapped_column(init=False, nullable=True)
