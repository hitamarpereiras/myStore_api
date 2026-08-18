from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


    # Cofiguracoes gerais
    APP_NAME: str = "my store"
    DEBUG: bool = False
    DATABASE_URL: str

    SUPABASE_URL: str
    SUPABASE_KEY: str

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str) and value.lower() in {"release", "production", "prod"}:
            return False
        return value

# Instância global para uso em toda a aplicação
thi_settings = EnvSettings()
