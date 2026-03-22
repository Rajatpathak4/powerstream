from datetime import timedelta, datetime
import json
from config import get_setting
from helper.GlobalFunctions import printCustmMsg,print_error_with_linenumebr
import requests
from modules.weather.models import ActualData, ActualTableData, City, WeatherData
from sqlalchemy import func
import os
from concurrent.futures import ThreadPoolExecutor
from database.database import SessionLocal
import time
import threading

api_call_count = 0
lock = threading.Lock()


configObj = get_setting()

def get_cities_from_json(db):
    try:
        city_val = []
        cities = db.query(City.city_name).filter(City.is_deleted == False).all()
        if not cities:
            return printCustmMsg(200, 'FALSE', 'No cities found')
        city_val = [city.city_name for city in cities]
        return printCustmMsg(200, 'TRUE', 'Cities fetched successfully', city_val)

    except Exception as err:
        print_error_with_linenumebr(err)
        return printCustmMsg(500, 'FALSE', msg='Something went wrong-->' + str(err))
    
def fetch_and_save_weather_data(city_name):
    db = SessionLocal() 
    global api_call_count
    try:
        data_date = datetime.now().date()

        latest_rev = db.query(WeatherData).filter(
            func.lower(WeatherData.city) == city_name.lower(),
            WeatherData.is_deleted == False,
            WeatherData.data_date == data_date
        ).order_by(WeatherData.revision_no.desc()).first()

        revision_no = latest_rev.revision_no + 1 if latest_rev else 0

        ext_url = configObj.WEATHER_API_URL + f"/weather?q={city_name}&appid={configObj.WEATHER_API_KEY}&units=metric"
        response = requests.get(ext_url)
        with lock:
            api_call_count += 1
            print(api_call_count,'api_call_count')

            if api_call_count == 999:
                print("API hit count reached 999")
            elif api_call_count >= 1000:
                print("API hit count reached 1000")
                return printCustmMsg(200, 'FALSE', 'API hit count reached 1000')

        city_obj = db.query(City).filter(
            func.lower(City.city_name) == city_name.lower(),
            City.is_deleted == False
        ).first()

        if not city_obj:
            return

        if response.status_code == 200:
            data = response.json()

            weather = {
                "city": data["name"],
                "city_id": city_obj.id,
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "temperature_feels": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "weather_description": data["weather"][0]["description"],
                "temp_min": data["main"]["temp_min"],
                "temp_max": data["main"]["temp_max"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"]["deg"],
                "visibility": data["visibility"],
                "clouds": data["clouds"]["all"],
                "sunrise_unix": data["sys"]["sunrise"],
                "sunset_unix": data["sys"]["sunset"],
                "longitude": data["coord"]["lon"],
                "latitude": data["coord"]["lat"],
                "data_date": data_date,
                "revision_no": revision_no,
            }

            weather_obj = WeatherData(**weather)
            db.add(weather_obj)
            db.commit()

    except Exception as err:
        db.rollback()
        print_error_with_linenumebr(err)
        return printCustmMsg(500, 'FALSE', msg='Something went wrong-->' + str(err))
    finally:
        db.close()  

def chunk_list(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def fetch_weather_data(db):
    try:
        cities_response = get_cities_from_json(db)

        if cities_response['status'] != 'TRUE':
            return cities_response

        city_list = cities_response['value']

        worker = 10
        chunk_size = 100

        for chunk in chunk_list(city_list, chunk_size):
            print(f"Processing batch of {len(chunk)} cities")

            with ThreadPoolExecutor(max_workers=worker) as executor:
                executor.map(fetch_and_save_weather_data, chunk)

            print("Sleeping for 5 seconds...")
            time.sleep(5)

        return printCustmMsg(200, 'TRUE', 'Weather data fetched successfully')

    except Exception as err:
        print_error_with_linenumebr(err)
        return printCustmMsg(500, 'FALSE', msg='Something went wrong-->' + str(err))
    
def get_latest_weather_data(data_date, city, db):
    try:
        lastest_revision = db.query(func.max(WeatherData.revision_no)).filter(WeatherData.is_deleted == False, WeatherData.data_date == data_date).scalar()
        if lastest_revision is None:
            return printCustmMsg(200, 'FALSE', 'No data found for the specified date and city')
        # ----------------------- Get City Wise List ------------------ -----
        query = db.query(WeatherData)\
            .join(City, WeatherData.city_id == City.id)\
            .filter(
                WeatherData.revision_no == lastest_revision,
                WeatherData.is_deleted == False,
                City.is_deleted == False
            )
        if city:
            city_val = city.strip().capitalize()
            query = query.filter(WeatherData.city == city_val)

        if data_date:
            try:
                parsed_date = datetime.strptime(data_date, '%Y-%m-%d').date() if isinstance(data_date, str) else data_date
                query = query.filter(WeatherData.data_date == parsed_date)
            except ValueError:
                return printCustmMsg(200, 'FALSE', 'Invalid date format! Use YYYY-MM-DD')
            
        result = query.order_by(WeatherData.data_date.desc(), WeatherData.revision_no.desc()).all()

        if not result:
            return printCustmMsg(200, 'FALSE', 'No data found')

        return printCustmMsg(200, 'TRUE', 'Data fetched successfully', result)

    except Exception as err:
        print_error_with_linenumebr(err)
        return printCustmMsg(500, 'FALSE', msg='Something went wrong-->' + str(err))

def read_city_list(db):
    try:
        filename = "cities.json"
        
        file_path = os.path.join(configObj.ASSETS,  filename)
        cities = []

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = json.load(file)
            for row in reader:
                cities.append(row) 

        for city in cities:
            city_name = city.get('city', '').strip().capitalize()

            if city_name:
                existing_city = db.query(City).filter(
                    City.city_name == city_name,
                    City.is_deleted == False).first()

                if not existing_city:
                    new_city = City(city_name=city_name,
                                     created_at=datetime.now(), 
                                     updated_at=datetime.now(),
                                     is_deleted=False
                                    )
                    db.add(new_city)
        db.commit()
        return cities

    except Exception as err:
        print_error_with_linenumebr(err)
        return printCustmMsg(500, 'FALSE', msg='Something went wrong-->' + str(err))

def crawling_actual_data(data_date, db):
    try:
        if data_date is None:
            data_date = datetime.now().date()
        api_url = f"{configObj.ACTUAL_API_URL}?date={data_date}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = json.loads(response.text)  
            for item in data:
                record_dict = {
                    "data_date": data_date,
                    "source": item.get('name_of_data'),
                    "actual_demand":item.get('value_of_data'),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "created_by": None,
                    "updated_by": None,
                }

                data_obj = ActualData(**record_dict)
                db.add(data_obj)
            db.commit()
        return printCustmMsg(200, 'TRUE', 'Actual data added successfully')
    except Exception as err:
        print_error_with_linenumebr(err)
        return printCustmMsg(500, 'FALSE', msg='Something went wrong-->' + str(err))    
