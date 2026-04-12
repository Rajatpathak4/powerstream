from sqlalchemy import Column, Integer, String, SmallInteger, TIMESTAMP, Boolean, DateTime, Float, DATE, ForeignKey
from database.database import Base
from datetime import datetime


class WeatherData(Base):
    __tablename__ = 'weather_data'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    data_date = Column(DATE, nullable=False)
    revision_no = Column(Integer, default=0)
    city = Column(String(255), nullable=False)
    temperature = Column(Float)
    temperature_feels = Column(Float)
    humidity = Column(Integer)
    weather_description = Column(String(255))
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    wind_speed = Column(Float)
    wind_direction = Column(Integer)
    visibility = Column(Integer)
    clouds = Column(Integer)
    country = Column(String(255))
    sunrise_unix = Column(Integer)
    sunset_unix = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
    created_by = Column(Integer)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_by = Column(Integer)
    deleted_on = Column(DateTime)
    updated_timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, nullable=False, default=False)
 

class City(Base):
    __tablename__ = 'cities'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

class ActualData(Base):
    __tablename__ = 'actual_data'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_date = Column(DATE, nullable=False)
    source = Column(String(255), nullable=False)
    actual_demand = Column(Float, nullable=False)
    file_name= Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.utcnow)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_deleted = Column(Boolean, default=False)
