from database.database import get_transaction_db
from fastapi import FastAPI, Request
from fastapi.responses import  RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from functools import lru_cache
from config import Settings
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from routes import (weather)
import time
from apscheduler.schedulers.background import BackgroundScheduler

@lru_cache
def get_settings():
    return Settings()

origins = ["*"]
app = FastAPI(
    description="This is for Power Stream portal api only",
    title="Power Stream Data api's",
    redoc_url="",
    dependencies=[Depends(get_settings)],
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.routes) 

@app.get('/docs')
def docs():
    return RedirectResponse('/')


@app.get('/')
def Index():
    return RedirectResponse('/docs')



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print("URL {0} response time is {1} sec".format(str(request.url), (time.time() - start_time)))
    return response


scheduler = BackgroundScheduler()
def scheduler_task():
    with next(get_transaction_db()) as db:
        weather.fetch_weather_data_crawl(db)


def actual_data_scheduler_task():
    with next(get_transaction_db()) as db:
        weather.fetch_actual_weather_data(data_date=None, db=db)

@app.on_event("startup")
def startup_event():
    scheduler.add_job(scheduler_task, 'interval', hours=6)
    print("Scheduler started for weather data.")
    scheduler.add_job(actual_data_scheduler_task, 'interval', minutes=5)
    print("Scheduler started for actual data insertion in db.")
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    print("Shutting down scheduled tasks.")
