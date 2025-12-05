from fastapi import FastAPI, Request
from routers.users import router as users_router
from routers.todos import router as todos_router
from core.logger import logger


app = FastAPI()
app.include_router(users_router)
app.include_router(todos_router)



@app.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} {response.status_code}")
    return response
