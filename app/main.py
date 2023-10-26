import asyncio
from fastapi import FastAPI, Depends
import logging
from uvicorn.config import Config
from uvicorn.server import Server
import config
from config import (
    PAGE_URL,
)
from dependencies import get_pool
from routers.main_route import router as main_router


logger = logging.getLogger('yandex_maps_api')


yandex_maps_kwargs = dict(
    page_url=PAGE_URL,
    headless=True,
)

app = FastAPI(
    openapi_prefix="/coordinates",
    dependencies=[Depends(get_pool)],
)
app.include_router(main_router)


# setup uvicorn logger
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


@app.on_event("startup")
async def startup_event() -> None:
    pass


@app.on_event("shutdown")
async def shutdown_event() -> None:
    pool = get_pool()
    pool.close()
    try:
        await app.state.r.close()
    except:
        pass

async def run_fastapi():
    config = Config(app=app, host="0.0.0.0", port=9000, lifespan="on")
    server = Server(config)
    await server.serve()


async def main() -> None:
    pool = get_pool()
    await asyncio.gather(
        pool.add_model(1, **yandex_maps_kwargs),
        run_fastapi(),
    )

if __name__ == "__main__":
    asyncio.run(main())