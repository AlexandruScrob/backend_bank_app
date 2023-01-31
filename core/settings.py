from functools import lru_cache
from pydantic import BaseSettings


class DotEnvSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class BankSettings(DotEnvSettings):
    host_base_url: str
    create_wallet_endpoint: str = "/wallet/$wallet_id"
    settle_endpoint: str = "/settle"

    @property
    def create_wallet_url(self) -> str:
        return f"{self.host_base_url}{self.create_wallet_endpoint}"

    @property
    def settle_url(self) -> str:
        return f"{self.host_base_url}{self.settle_endpoint}"


class Settings(DotEnvSettings):
    bank_settings: BankSettings = BankSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
