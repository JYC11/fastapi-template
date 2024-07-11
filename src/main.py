import uvicorn
from fastapi import FastAPI, HTTPException, Request
from starlette import status
from starlette.responses import JSONResponse

from src.common.settings import settings
from src.entrypoints.v1.router import api_v1_router
from src.service_layer.exceptions import (
    ConcurrencyException,
    DuplicateRecord,
    Forbidden,
    ItemNotFound,
    MethodNotFound,
    Unauthorized,
)

app = FastAPI(
    title="template",
    redoc_url="/redoc",
    docs_url="/docs",
    openapi_url=f"{settings.api_v1_str}/openapi.json",
)


@app.middleware("http")
async def exception_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as http_exception:
        return JSONResponse(
            status_code=http_exception.status_code,
            content={"error": "Client Error", "message": str(http_exception.detail)},
        )
    except ItemNotFound as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Not found", "message": str(e)},
        )
    except MethodNotFound as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Incorrect method call in message bus", "message": str(e)},
        )
    except Unauthorized as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Unauthorized", "message": str(e)},
        )
    except Forbidden as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": "Forbidden", "message": str(e)},
        )
    except DuplicateRecord as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Duplicate record exists", "message": str(e)},
        )
    except ConcurrencyException as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Concurrency exception", "message": str(e)},
        )
    # except Exception as e:
    #     return JSONResponse(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         content={"error": "Internal Server Error", "message": str(e)},
    #     )


app.include_router(api_v1_router)


if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8000, reload=True)
