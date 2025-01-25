from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str
    PGDATA: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


configs = Configs()
