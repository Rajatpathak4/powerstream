import json, socket
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI, Depends
from functools import lru_cache
from config import Settings
from starlette.middleware.sessions import SessionMiddleware
import sys
import time
from fastapi.staticfiles import StaticFiles
import os
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from routes import (weather)


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

app.include_router(weather.routes)  # Assuming 'routes' is defined in the imported weather module

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


def seconds_to_next_slot():
    now = datetime.now()
    minutes = now.minute
    next_minutes = ((minutes // 15) + 1) * 15  # Get next multiple of 15
    
    if next_minutes == 60:  # Handle the hour change
        next_time = now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0)
    else:
        next_time = now.replace(minute=next_minutes, second=0, microsecond=0)
    
    return int((next_time - now).total_seconds())

# scheduler = BackgroundScheduler()
# def scheduled_task():
#     with next(get_transaction_db()) as db:
#         last_two_min_flag = seconds_to_next_slot() < 120
#         dsmreport.dsm_current_block_data(last_two_min_flag)
#         todays_date = datetime.today().date()
#         curr_date = datetime.now()
#         curr_month = curr_date.month
#         curr_year = curr_date.year
#         for genType in ['SCADA', 'FREQ']:
#             res = demand_crud.generateActual96BlockData(db, genType, todays_date, False)
#             print(res)
        
#         dsm_crud.remaining_block_dsm_calculation(db, todays_date, False)
#         #-------Generating auto scheduling for intraday--------#
#         cronjob.mhCrawling({},  'INTRADAY' , db)
#         cronjob.mhCrawling({},  'DAYAHEAD' , db)
#         cronjob.wrldcCrwal(db , None, 'INTRADAY', -1)
#         cronjob.wrldcCrwal(db , None, 'DAYAHEAD', -1)
#         cronjob.save_scheduling_model_processed_data('DAYAHEAD', db)      
#         cronjob.save_scheduling_model_processed_data('INTRADAY', db)    
#         cronjob.write_outage_status(db)          
#         cronjob.get_forecast_data(curr_year,curr_month,db)
#         cronjob.import_iex_sanpshot('RTM',None,db)
#         cronjob.import_iex_sanpshot('DAM',None,db)
#         cronjob.save_obligation_data(None, db)
#         cronjob.save_bidding_data(None, db)
#         bidding.get_obligation_data('RTM', 'IEX', None, db)
         
#         #----------------Calling saveschedulingdata---------------#
#         schReq=scheduling_schema.SchedulingRequest(
#                 data_visible="INTRADAY",
#                 data_date=todays_date,
#                 is_cal_price=None
#             )   
#         save_scheduling_result = scheduling.save_scheduling_data(schReq, db) 
#         print(save_scheduling_result,'SAVE SCHEDULING RESULT')
        
# def del_token():
#     with next(get_transaction_db()) as db:
#         crud.delete_token(db)
#         print("Deleted expired tokens.")
        

# @app.on_event("startup")
# def startup_event():
#     scheduler.add_job(scheduled_task, 'interval', minutes=15)
#     scheduler.add_job(del_token, 'interval', days=1)
#     scheduler.start()

# @app.on_event("shutdown")
# def shutdown_event():
#     scheduler.shutdown()
#     print("Shutting down scheduled tasks.")

# def is_local():
#     ip = socket.gethostbyname(socket.gethostname())
#     print(ip)
#     return ip.startswith("127.") or ip == "0.0.0.0"    
