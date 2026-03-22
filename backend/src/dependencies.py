
from fastapi import HTTPException, Header, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.postgresdb import get_db
from config import get_setting
from modules.common import models

from src.modules.master.models import UserMenuDetails,UserMenuPrevilage
from sqlalchemy import  func
from helper.sessionData import getSessionUserId
from datetime import datetime, timedelta


config = get_setting()
ACCESS_TOKEN_EXPIRE_MINUTES = 300

auth_scheme = HTTPBearer()
def tokenvalidation(dbObj: Session = Depends(get_db),token: HTTPAuthorizationCredentials = Depends(auth_scheme),request:Request=None):# Authorization: str = Header(...)):
    try:
        token= request.headers['Authorization'].replace('Bearer ','')  
        tokenData=dbObj.query(models.LoginTokens).with_entities(
            models.Users.id,
            models.Users.name,
            models.Users.orgname,
            models.Users.user_category_id,
            models.Users.user_type,
            models.Users.email,
            models.LoginTokens.token
        ).join(
            models.Users,
            models.LoginTokens.user_id==models.Users.id
        ).filter(
            models.LoginTokens.token==token
        ).first() 
        if tokenData:
            request.session['userData']=dict(tokenData)
            if (request.url.path != "/auth/health_check"):
                dbObj.query(models.LoginTokens).filter(models.LoginTokens.token == token).update(
                    {"token_expiry": datetime.now() + timedelta(minutes=180)},
                    synchronize_session=False
                )
                dbObj.commit()
            return True             
        else:           
            raise HTTPException(
                status_code=401,
                detail='You are not authorised to access')
    except Exception as e:  # catches any exception
       
        print(e)
        raise HTTPException(
            status_code=401,
            detail='You are not authorised to access')
    