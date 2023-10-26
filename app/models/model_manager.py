import asyncio
from .yandex_maps import YandexMaps
from typing import List
import logging
from .errors import (
    NoFreeModelFound,
    NotFoundMessageByPrompt,
    BtnNotFound,
    NotFoundMessageById
)


logger = logging.getLogger(__name__)


class Model:
    def __init__(self, **kwargs) -> None:
        self.constructor_kwargs = kwargs
        self.ym: YandexMaps
        self.is_busy = True
        self.lock = asyncio.Lock()
    
    async def init(self) -> None:
        async with self.lock:
            self.is_busy = True
            self.close()

            self.ym = await asyncio.to_thread(YandexMaps, **self.constructor_kwargs)
            self.is_busy = False
    
    async def asend_prompt(self, prompt:str) -> dict:
        async with self.lock:
            res = await asyncio.to_thread(self.ym.send_prompt, prompt)
            return res
    
    def close(self):
            try:
                self.ym.close()
            except:
                pass


class ModelManager:
    def __init__(self, pool: List[Model]) -> None:
        self.pool = pool
        self.model: Model | None = None
        self.model_n = None
        self.lock = asyncio.Lock()

    async def __aenter__(self) -> Model:
        self.model = await self.acquire_model()

        return self.model

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        async with self.lock:
            if self.model is not None:
                self.model.is_busy = False
                logger.debug(f'release model {self.model_n}')

    async def acquire_model(self) -> Model:
        """The function return free model or raise an excaption"""
        async with self.lock:
            for i, model in enumerate(self.pool):
                if not model.is_busy:
                    logger.debug(f'Model {i} is acquired')
                    model.is_busy = True
                    self.model_n = i
                    return model
            logger.warning('No free model found!')
            raise NoFreeModelFound


class ModelsPool:
    def __init__(self) -> None:
        self.pool: List[Model] = []
    
    async def add_model(self, instances: int = 1, **kwargs) -> None:
        tasks = []
        for _ in range(instances):
            model = Model(**kwargs)
            self.pool.append(model)
            tasks.append(asyncio.create_task(model.init()))

        await asyncio.gather(*tasks)
    
    def acquire(self) -> ModelManager:
        return ModelManager(self.pool)
    
    def close(self) -> None:
        for model in self.pool:
            model.close()
