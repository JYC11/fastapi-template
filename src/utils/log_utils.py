import logging
from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)


def logging_decorator(log_path: str):
    def internal_logger(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger.info(f"{log_path}.{func.__name__} called with : \nArgument:{args}\nKeyword argument:{kwargs}:")

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Exception in: {log_path}.{func.__name__}. exception{str(e)}")
                raise e

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger.info(f"{log_path}.{func.__name__} called with : \nArgument:{args}\nKeyword argument:{kwargs}:")
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Exception in: {log_path}.{func.__name__}. exception{str(e)}")
                raise e

        if iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return internal_logger
