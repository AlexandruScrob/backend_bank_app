import asyncio
import json
import aiohttp
import uuid
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from core.serializers import RequestModel, TransactionModel, PayTypeEnum
from api import bank_api


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "App is running."}


@app.post(path="/transaction")
async def transaction(req_data: RequestModel):
    # create 2 wallets async

    wallet_id_1, wallet_id_2 = str(uuid.uuid4()), str(uuid.uuid4())

    async with aiohttp.ClientSession() as session_1:
        tasks = [
            bank_api.create_wallet(session=session_1, wallet_id=str(uuid.uuid4()))
            for _ in range(2)
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async with aiohttp.ClientSession() as session_2:
        tasks = [
            # from
            bank_api.transaction(
                session=session_2,
                tr_data=TransactionModel(
                    amount=req_data.amount,
                    wallet_id=wallet_id_1,
                    type=PayTypeEnum.payout.value,
                    iban=req_data.from_iban,
                ),
            ),
            # to
            bank_api.transaction(
                session=session_2,
                tr_data=TransactionModel(
                    amount=req_data.amount,
                    wallet_id=wallet_id_2,
                    type=PayTypeEnum.payin.value,
                    iban=req_data.to_iban,
                ),
            ),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    return JSONResponse(content=results)
