from pydantic_settings import BaseSettings # pyright: ignore[reportMissingImports]


class Settings(BaseSettings):
    app_name: str = "Nshight API"
    environment: str = "development"

    llm_api_key: str = ""
    llm_base_url: str = "https://openrouter.ai/api/v1"
    llm_model: str = "gpt-5-mini"

    class Config:
        env_file = ".env"


settings = Settings()