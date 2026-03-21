from fastapi.responses import JSONResponse
from datetime import timedelta





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