import time

from fastapi import FastAPI, Request

from app.logger import logger
from app.user.router import router as user_router
from app.post.router import router as post_router
from app.post.comment.router import router as comment_router

app = FastAPI(openapi_prefix="/api")

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request processing time: {process_time}", extra={
        "process_time": round(process_time, 4)
    })

    return response
