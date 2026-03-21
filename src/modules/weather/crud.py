from datetime import timedelta, datetime
from config import get_setting
from helper.GlobalFunctions import printCustmMsg,print_error_with_linenumebr
import requests
from modules.weather.models import WeatherData
from sqlalchemy import func



configObj = get_setting()

def fetch_weather_data(city, db):
    try:
        if not city:
            return printCustmMsg(200, 'FALSE', 'Select Valid City')

        city_val = city.strip().capitalize()
        data_date = datetime.now().date()

        latest_rev = db.query(WeatherData).filter(
            func.lower(WeatherData.city) == city_val.lower(),
            WeatherData.is_deleted == False,
            WeatherData.data_date == data_date
        ).order_by(WeatherData.revision_no.desc()).first()
        if latest_rev:
            revision_no = latest_rev.revision_no + 1
        else:
            revision_no = 0

        ext_url = configObj.WEATHER_API_URL + f"/weather?q={city_val}&appid={configObj.WEATHER_API_KEY}&units=metric"
        response = requests.get(ext_url)

        if response.status_code == 200:
            data = response.json()
            weather = {
                "city": data["name"],
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
            db.refresh(weather_obj)
            return printCustmMsg(200, 'TRUE', 'Weather data saved successfully', weather)

        elif response.status_code == 404:
            return printCustmMsg(200, 'FALSE', 'City not found!')

        elif response.status_code == 401:
            return printCustmMsg(200, 'FALSE', 'Invalid API Key!')

        else:
            return printCustmMsg(200, 'FALSE', f'API Error --> {response.status_code}')

    except Exception as err:
        db.rollback()
        print_error_with_linenumebr(err)
        return printCustmMsg(500, 'FALSE', msg='Something went wrong-->' + str(err))
    

def get_latest_weather_data(data_date, city, db):
    try:
        lastest_revision = db.query(func.max(WeatherData.revision_no)).filter(
            WeatherData.is_deleted == False,
            WeatherData.data_date == data_date
        ).scalar()
        if lastest_revision is None:
            return printCustmMsg(200, 'FALSE', 'No data found for the specified date and city')
        query = db.query(WeatherData).filter(WeatherData.is_deleted == False, WeatherData.revision_no == lastest_revision)

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


