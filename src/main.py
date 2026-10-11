from fastapi import FastAPI

from src.routes.tickets import router as tickets_router

app = FastAPI()


app.include_router(tickets_router)
