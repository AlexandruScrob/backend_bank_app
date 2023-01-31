import aiohttp
import backoff
from typing import Any
from string import Template

from core.serializers import TransactionModel
from core.settings import get_settings


settings = get_settings()


@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60)
@backoff.on_predicate(
    backoff.expo,
    predicate=lambda r: r.json() == {"result": "error"},
    max_time=60,
)
async def create_wallet(
    session: aiohttp.ClientSession, wallet_id: str
) -> dict[str, Any]:
    url = Template(settings.bank_settings.create_wallet_url).substitute(
        wallet_id=wallet_id
    )
    response = await session.request("POST", url=url)
    return await response.json()


@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60)
async def transaction(
    session: aiohttp.ClientSession, tr_data: TransactionModel
) -> dict[str, Any]:
    response = await session.request(
        "POST", url=settings.bank_settings.settle_url, json=tr_data.dict()
    )
    return await response.json()
