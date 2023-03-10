from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):

    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    API_URL_PREFIX: str = "/v1"

    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_USER: str = "admin"
    PG_PASSWORD: str = "admin"
    PG_DB: str = "rest"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_migrate_url(self):
        return PostgresDsn.build(
            scheme="postgresql", user=self.PG_USER, password=self.PG_PASSWORD, host=self.PG_HOST, path=self.PG_DB
        )

    def get_pg_url(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.PG_USER,
            password=self.PG_PASSWORD,
            host=self.PG_HOST,
            path=f"/{self.PG_DB}",
        )


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore
