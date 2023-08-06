import time
from fastapi import FastAPI
from starlette.requests import Request


def set_process_time_headers(app: FastAPI) -> None:
    """
    Set middleware that inject X-Process-Time header into request
    """

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
