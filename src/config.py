from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


_common_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)

class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        **_common_config,
        env_prefix="DB_",
    )

    user: str
    password: SecretStr
    host: str
    port: int
    name: str

    @property
    def dsn(self):
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)


settings = Config()