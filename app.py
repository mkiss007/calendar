from flask import Flask, render_template, request, jsonify, make_response
import holidays
import datetime
from init import extraWorkingDay, extraHoliday

from werkzeug.wrappers import response

app = Flask(__name__)


def validateInput(base_date, offset, country):
    return True
    
    
def isWorkingDay(param, country):
    is_working_day = True
    if (param.isoweekday() in [6, 7]) or (param.strftime('%Y-%m-%d')  in extraHoliday[country]) or holidays.CountryHoliday(country).get(param.strftime('%Y-%m-%d')):
        is_working_day = False

    if  param.strftime('%Y-%m-%d')  in extraWorkingDay[country]:
        is_working_day = True  

    return(is_working_day)


def getNextWorkingDay(base_date, offset, country):
    ret = 'Error'
    if validateInput(base_date, offset, country):
        #holidays = holidays.CountryHoliday(country)
        next_date = datetime.datetime.strptime(base_date, "%Y-%m-%d").date()

        n = 1
        while n <= offset:
            next_date = next_date + datetime.timedelta(days=1)

            if isWorkingDay(next_date, country):
                n += 1

        ret = next_date

    return ret    

@app.route('/getnextworkingday', methods=['GET'])
def getNWD():

    args = request.args

    if "country" in args:
        country = args.get("country")
        if "offset" in args:
            offset = int(args.get("offset"))
            if "basedate" in args:
                base_date = args.get("basedate")
                resp = {'response': 
                                {'nextWorkingDay': getNextWorkingDay(base_date, offset, country)}}

                response = jsonify(resp)      
                return response    
    else:
        raise RuntimeError("Don't know how to handle method {}".format(request.method))        




