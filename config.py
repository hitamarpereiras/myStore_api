from pydantic_settings import BaseSettings, SettingsConfigDict

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

# Instância global para uso em toda a aplicação
thi_settings = EnvSettings()