from fastapi import APIRouter, Depends, Request, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import  datetime
from modules.auth.schemas import (
    LoginSchema
)
from dependencies import tokenvalidation
from database.database import get_db
from modules.auth.crud import user_login, update_auth_token, make_user_data, get_user_data, delete_token,signout
from helper import customhelper, GlobalFunctions
from modules.common.models import LoginTokens
from helper.sessionData import getSessionUserId, getSessionUserEmail
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


is_valid = [Depends(tokenvalidation)]
routes = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)


@routes.post("/login")
def login(user_request: LoginSchema, request: Request, db: Session = Depends(get_db)):
    customhelper.do_nothing(request)
    return user_login(user_request, db)