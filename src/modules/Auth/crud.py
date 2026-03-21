from fastapi import Depends, status
from datetime import timedelta, datetime
from sqlalchemy import or_, and_
from helper.customhelper import print_error_with_linenumebr, bcrypt_context, create_access_token
from helper.GlobalFunctions import printCustmMsg
from modules.common.models import Users, LoginTokens, MasterUserCategory
from modules.master.models import UserMenuPrevilage, UserMenuDetails, DynamicGraphDetails
from helper import customhelper

DASHBOARD_REDIRECT_URL = "/dashboard"

def check_user_schema(user_schema):
    if (not user_schema.email or not user_schema.password):
        response = printCustmMsg(200,'FALSE', "Either session,username or password is missing")
        return response
    
def user_login(user_schema, db):
    try:
        schema_status = check_user_schema(user_schema)
        if schema_status:
            return schema_status
        
        user = get_user_data(user_schema.email, db)
        # check User
        
        if user is None:
            response = printCustmMsg(200,'FALSE', "Incorrect Email or Password")
            return response
        
        if not bcrypt_context.verify(user_schema.password, user.Users.password):
            response = printCustmMsg(200, 'FALSE', "Incorrect Email or Password")
            db.rollback()
            return response
        existing_token = (
            db.query(LoginTokens)
            .filter(
                LoginTokens.user_id == user.Users.id,
                LoginTokens.token_expiry >= datetime.now(),
            )
            .first()
        )
        if existing_token:
            response = printCustmMsg(200, 'FALSE', "You've already logged in")
            return response
        access_token = create_access_token(user.Users.email, user.Users.id, timedelta(minutes=180))
        user.Users.last_login = datetime.now()
        db.add(LoginTokens(
            token=access_token,
            user_id=user.Users.id,
            pat_id=1,
            token_expiry=(datetime.now() + timedelta(minutes=60))
        ))
        user_dict = {
            "orgname": user.Users.orgname,
            "uid": user.Users.id,
            "first_name": user.Users.name.upper(),
            "last_name": None,
            "name": user.Users.name,
            "email": user.Users.email,
            "user_category_id": user.Users.user_category_id,
            "category_prefix": None,
            "token": access_token,
            # "menu": get_menu_list(user.Users.id, db),
            "first_redirection": 'dashboard',
            "is_firsttime_login": user.Users.is_firsttime_login,
            "last_login": user.Users.last_login,
            "redirectUrl": DASHBOARD_REDIRECT_URL,
            "is_active": False,
            "current_time": datetime.now(),
        }
        response = printCustmMsg(
            status.HTTP_200_OK,
            'TRUE',
            "Login successfully",
            user_dict,
        )
        db.commit()
        return response
    except Exception as e:
        db.rollback()
        print_error_with_linenumebr(e)
        response = printCustmMsg(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'FALSE',
            "Something went wrong. Please try after some time"
        )
        return response

def build_menu_item(menu):
    return {
        "id": menu.id,
        "title": menu.menu_name,
        "path": menu.menu_url or "",
        "priority": menu.priority,
        "sub_priority": menu.sub_priority,
        "parent_id": menu.parent_id,
        "icon": menu.icon,
        "class": "",
        "ddclass": "",
        "extralink": menu.extralink,
        "status": menu.status,
        "tag_id": menu.tag_id,
        "is_default": menu.is_default,
        "is_read": False,
        "is_write": False,
        "parent_menu": None,
        "submenu": [],
    }


def update_auth_token(user_schema, db):
    try:
        schema_status = check_user_schema(user_schema)
        if schema_status:
            return schema_status

        update_user_data = get_user_data(user_schema.email, db)

        if not update_user_data:
            update_response = printCustmMsg(200,'FALSE',"Either username or email does not exist")
            return update_response
                
        if not bcrypt_context.verify(user_schema.password, update_user_data.Users.password):
            response = printCustmMsg(
                200,
                'FALSE',
                "Invalid credentials"
            )
            return response
        
        db.query(LoginTokens).filter(LoginTokens.user_id == update_user_data.Users.id).delete()
        access_token = create_access_token(update_user_data.Users.email, update_user_data.Users.id, timedelta(minutes=180))
        update_user_data.Users.last_login = datetime.now()
        db.add(LoginTokens(
            token=access_token,
            user_id=update_user_data.Users.id,
            pat_id=1,
            token_expiry=(datetime.now() + timedelta(minutes=60))
        ))
        db.flush()
        
        # Convert user object to dictionary
        user_dict = {
            "orgname": update_user_data.Users.orgname,
            "uid": update_user_data.Users.id,
            "first_name": update_user_data.Users.name.upper(),
            "last_name": None,
            "name": update_user_data.Users.name,
            "email": update_user_data.Users.email,
            "user_category_id": update_user_data.Users.user_category_id,
            "category_prefix": None,
            "token": access_token,
            "menu": get_menu_list(update_user_data.Users.id, db),
            "first_redirection": 'dashboard',
            "is_firsttime_login": update_user_data.Users.is_firsttime_login,
            "last_login": update_user_data.Users.last_login,
            "redirectUrl": DASHBOARD_REDIRECT_URL,
            "is_active": False,
            "current_time": datetime.now()
        }
        response = printCustmMsg(200,'TRUE',"Login successfully",user_dict)
        db.commit()
        return response
    except Exception as e:
        db.rollback()
        print_error_with_linenumebr(e)
        response = printCustmMsg(
            500,
            'FALSE',
            "Something went wrong. Please try after some time"
        )
        return response


def get_user_data(email, db):
    user_data = db.query(
        Users,
        MasterUserCategory
    ).join(
        MasterUserCategory,
        MasterUserCategory.id ==Users.user_category_id
    ).filter(
        Users.email == email,
        MasterUserCategory.is_deleted == False,
        Users.is_deleted == 0
    ).first()
    return user_data

def make_user_data(user_data, db, access_token=None):
    return {
        "orgname": user_data.Users.orgname,
        "uid": user_data.Users.id,
        "first_name": user_data.Users.name.upper(),
        "last_name": None,
        "name": user_data.Users.name,
        "email": user_data.Users.email,
        "user_category_id": user_data.Users.user_category_id,
        "category_prefix": None,
        "token": access_token,
        "menu": get_menu_list(user_data.Users.id, db),
        "first_redirection": 'dashboard',
        "is_firsttime_login": user_data.Users.is_firsttime_login,
        "last_login": user_data.Users.last_login,
        "redirectUrl": DASHBOARD_REDIRECT_URL,
        "is_active": False,
        "current_time": datetime.now()
    }

def delete_token(db):
    try:
        now = datetime.now() 

        db.query(LoginTokens).filter(
            or_(
                LoginTokens.token_expiry < now,
                LoginTokens.token_expiry == None,
            )
        ).delete(synchronize_session=False)

        db.commit()

        response = printCustmMsg(200, 'TRUE', "Token removed successfully")
        return response
    except Exception as err:
        print_error_with_linenumebr(err)
        return printCustmMsg(500, 'FALSE', msg='Something went wrong --> ' + str(err))

def signout(db, token):
    try:
        raw_token = token.credentials
        if not raw_token:
            return printCustmMsg(200, 'FALSE', "Token is required")
        deleted_count = db.query(LoginTokens).filter(LoginTokens.token == raw_token).delete(synchronize_session=False)
        db.commit()
        if deleted_count == 0:
            return printCustmMsg(404, 'FALSE', "Token not found or already deleted")
        return printCustmMsg(200, 'TRUE', "User logged out successfully")

    except Exception as err:
        print_error_with_linenumebr(err)
        return printCustmMsg(500, 'FALSE', msg='Something went wrong --> ' + str(err))

# def get_menu_list(user_id, db):
#     result = []
#     try:
#         db_data = db.query(
#             UserMenuDetails.id,
#             UserMenuDetails.menu_name,
#             UserMenuDetails.menu_url,
#             UserMenuDetails.parent_id,
#             UserMenuDetails.priority,
#             UserMenuDetails.sub_priority,
#             UserMenuDetails.icon,
#             UserMenuDetails.ddclass,
#             UserMenuDetails.extralink,
#             UserMenuDetails.class_name,
#             UserMenuPrevilage.is_read,
#             UserMenuPrevilage.is_write,
#             UserMenuDetails.status,
#             UserMenuDetails.tag_id,
#             UserMenuDetails.is_default,
#         ).join(
#             UserMenuPrevilage,
#             UserMenuPrevilage.menu_id == UserMenuDetails.id
#         ).filter(
#             UserMenuPrevilage.user_id == user_id,
#             UserMenuPrevilage.is_deleted == 0,
#             UserMenuDetails.is_deleted == 0,
#             UserMenuPrevilage.is_read == 'TRUE'
#         ).all()

#         menu_dict = {}

#         for menu in db_data:
#             if menu.parent_id:
#                 parent_id_str = str(menu.parent_id)
#                 if parent_id_str not in menu_dict:
#                     menu_dict[parent_id_str] = {
#                         "id": None,
#                         "title": None,
#                         "path": "",
#                         "priority": None,
#                         "sub_priority": None,
#                         "parent_id": None,
#                         "icon": None,
#                         "class": 'has-arrow',
#                         "ddclass": '',
#                         "extralink": 0,
#                         "submenu": []
#                     }

#                 submenu_item = build_menu_item(menu)
#                 submenu_item["parent_menu"] = menu_dict[parent_id_str]["title"]
#                 menu_dict[parent_id_str]["submenu"].append(submenu_item)

#             else:
#                 menu_id_str = str(menu.id)
#                 if menu_id_str not in menu_dict:
#                     menu_dict[menu_id_str] = build_menu_item(menu)

#         result = sorted(
#             [
#                 {
#                     **item,
#                     "submenu": sorted(item["submenu"], key=lambda c: c["sub_priority"])
#                     if item.get("submenu") else []
#                 }
#                 for item in menu_dict.values()
#             ],
#             key=lambda x: x["priority"] if x["priority"] is not None else 999
#         )

#     except Exception as e:
#         print_error_with_linenumebr(e)

#     return result


