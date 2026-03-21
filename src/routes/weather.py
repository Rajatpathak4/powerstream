import asyncio
from fastapi import APIRouter, Depends, BackgroundTasks, Query
from config import get_setting
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from helper import GlobalFunctions
from datetime import  date,datetime,timedelta, time as datetime_time
from dateutil.relativedelta import relativedelta
from typing import Optional
from fastapi import FastAPI, File, UploadFile
from helper.GlobalFunctions import printCustmMsg
import sys
from modules.weather import crud


routes = APIRouter(tags=["Weather Routes"])
configObj = get_setting()

@routes.get("/crawl_weather_data")
def fetch_weather_data(city: Optional[str] = None, db: Session= Depends(get_db)):
    try:
        response = crud.fetch_weather_data(city, db)
        return response
    except Exception as err:
        GlobalFunctions.print_error_with_linenumebr(err)
        return printCustmMsg(200, 'FALSE',msg='Something went wrong-->' + str(err))
    
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