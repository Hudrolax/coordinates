from fastapi import APIRouter, HTTPException, Depends
import traceback
import logging
from config import TOKEN
from models.model_manager import NoFreeModelFound
from fastapi_models import Answer
from dependencies import get_pool


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def send_prompt(
    address: str,
    token: str | None = None,
    pool=Depends(get_pool),
) -> Answer:
    if token != TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        async with pool.acquire() as ym:
            coords = await ym.asend_prompt(address)
            return Answer(**coords)

    except NoFreeModelFound:
        raise HTTPException(
            status_code=500, detail='Server is not ready yet! Try again in 3 minutes...')

    except Exception as ex:
        error_message = f"Exception occurred: {type(ex).__name__}, {ex.args}\n"
        error_message += traceback.format_exc()
        logger.critical(error_message)
        raise HTTPException(status_code=500)
