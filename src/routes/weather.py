import asyncio
from fastapi import APIRouter, Depends, BackgroundTasks, Query
from config import get_setting
from database.database import get_db, get_transaction_db
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from helper import GlobalFunctions
from datetime import  date,datetime,timedelta, time as datetime_time
from dateutil.relativedelta import relativedelta
from typing import Optional
from fastapi import FastAPI, File, UploadFile
from helper.GlobalFunctions import printCustmMsg, run_in_background
import sys
from modules.weather import crud


routes = APIRouter(tags=["Weather Crons"])
configObj = get_setting()

@routes.get("/crawl_weather_data")
def fetch_weather_data(background_tasks: BackgroundTasks, db: Session= Depends(get_transaction_db)):
    try:
        background_tasks.add_task(run_in_background,fetch_weather_data_crawl, db)
       
        return {"Weather data crawl started in background"}
    except Exception as err:
        GlobalFunctions.print_error_with_linenumebr(err)
        return printCustmMsg(200, 'FALSE',msg='Something went wrong-->' + str(err))
    
def fetch_weather_data_crawl(db:Session = Depends(get_transaction_db)):
    start_time = datetime.now()
    print(f"Weather crawl started at: {start_time}")

    try:
        response = crud.fetch_weather_data(db)
        return response

    except Exception as err:
        GlobalFunctions.print_error_with_linenumebr(err)
        return printCustmMsg(200, 'FALSE', msg='Something went wrong-->' + str(err))

    finally:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print(f"Weather crawl finished at: {end_time}")
        print(f"Total time taken: {duration} seconds")
    
@routes.get("/get_latest_weather_data")
def get_weather_data(data_date: Optional[date]= None, city: Optional[str]= None , db:Session= Depends(get_db)):
    try:
        if data_date is None:
            data_date = datetime.now().date()
        response = crud.get_latest_weather_data(data_date, city, db)
        return response
    except Exception as err:
        GlobalFunctions.print_error_with_linenumebr(err)
        return printCustmMsg(200, 'FALSE',msg='Something went wrong-->' + str(err))
    
@routes.get('/add_city_list')
def add_city_list(db: Session = Depends(get_db)):
    try:
        cities = crud.read_city_list(db)
        return cities
    except Exception as err:
        GlobalFunctions.print_error_with_linenumebr(err)
        return printCustmMsg(200, 'FALSE', msg='Something went wrong-->' + str(err))
    