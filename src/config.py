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
        env_prefix="db_",
    )

    user: str
    password: SecretStr
    host: str
    port: int
    name: str

    @property
    def dsn(self):
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"
    
    @property
    def sync_dsn(self):
        return f"postgresql+psycopg2://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class Token(BaseSettings):
    model_config = SettingsConfigDict(
        **_common_config,
        env_prefix="vk_"
    )

    token: SecretStr


class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    token: Token = Field(default_factory=Token)


settings = Config()