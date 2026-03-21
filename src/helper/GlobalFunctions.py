from fastapi.responses import JSONResponse
from datetime import timedelta
import sys, os



def printCustmMsg(statusCode = 200, type = 'TRUE', msg = '', value = None):
    if statusCode in [200,201] and value is not None:
        resp = {"status": type,"message": msg, "value": value}
        return resp
    else: 
         resp = JSONResponse(status_code=statusCode,content={"status": type, "message": msg})
         return resp

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def print_error_with_linenumebr(e):   
    exc_type, exc_obj, exc_tb = sys.exc_info()        
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]        
    print(exc_type, fname, exc_tb.tb_lineno)
    print(str(e))