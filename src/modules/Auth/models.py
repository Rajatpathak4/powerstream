from sqlalchemy import Column, Integer, String, SmallInteger, TIMESTAMP, Boolean, DateTime
from database.database import Base
from datetime import datetime


class UserDetails(Base):
    __tablename__="user_details"
    __table_args__ = {'extend_existing': True}
    id  = Column(Integer, primary_key = True)
    name = Column(String(255))
    orgname = Column(String(255), nullable = False)    
    email = Column(String(255), nullable = False)
    password = Column(String(255), nullable = False)
    user_type = Column(String(10), nullable = False)
    user_category_id=  Column(Integer, nullable = False)
    is_active =  Column(String(30), nullable = False)
    last_login =  Column(TIMESTAMP, nullable = True)
    profile_compress_image_path =  Column(String(255), nullable = True)
    is_firsttime_login =  Column(SmallInteger, nullable = False)
    is_deleted =  Column(SmallInteger, nullable = False)

class LoginTokens(Base):
    __tablename__='login_tokens'
    __table_args__ = {'extend_existing': True}
    id=Column(Integer,primary_key=True)
    token=Column(String,nullable=False)
    user_id=Column(Integer,nullable=False)
    pat_id=Column(Integer,nullable=False)
    token_expiry=Column(DateTime)