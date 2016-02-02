"""
    Very simple Flask web site, with one page
    displaying a course schedule.
    """

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling
import math # Using the modf() function to help determine the hours and mins to be added
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times


# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def calc_times():
    """
    Calculates open/close times from miles, using rules
    described at http://www.rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request");
    
    date = request.args.get('date', 0, type=str)
    time = request.args.get('time', 0, type=str)
    brev_dist = request.args.get('brevet_dist', 0, type=int)
    dist_unit = request.args.get('units', 0, type=str)
    dist = request.args.get('miles', 0, type=int)
    
    date_time = "{} {}".format(date, time)
    arrow_time = arrow.get(date_time, "MM/DD/YYYY HH:mm")
    
    min_limits = [15, 15, 15, 11.428, 13.333]
    max_limits = [34, 32, 30, 28, 26]
    change_list = [200, 400, 600, 1000, 1300]
    st_control = [0, 200/34, 825/68, 3835/204, 47245/1428, 828385/18564]
    end_control = [600/15, 400/11.428, 300/13.333]
    max_spd = 0
    min_spd = 0
    start_time = 0
    end_time = 0
    extra_time = 0
    
    #Check if the units selected is miles, if so convert to kilometers.
    if dist_unit == "mi":
        dist *= 1.609
    
    #A for-loop/conditional hybrid to find for the correct speeds to use
    if dist >= 0:
        for change in change_list:
            if dist < change:
                max_spd = max_limits[change_list.index(change)]
                min_spd = min_limits[change_list.index(change)]
                break

    #Calculates the extra time that is need under certain conditions.
    if dist >= 0:
        for change in change_list:
            if brev_dist == dist:
                if dist >= brev_dist:
                    dist = brev_dist
                    if dist == 200 or dist == 1000:
                        extra_time = 10
                    elif dist == 400:
                        extra_time = 20

    #Calculates the times depending on the distance
    if dist in range(0,200):
        start_time = dist/max_spd + st_control[0]
        end_time = dist/min_spd

    elif dist in range(200,400):
        start_time = (dist-200)/max_spd + st_control[1]
        end_time = dist/min_spd

    elif dist in range(400,600):
        start_time = (dist-400)/max_spd + st_control[2]
        end_time = dist/min_spd

    elif dist in range(600,1000):
        start_time = (dist-600)/max_spd + st_control[3]
        end_time = dist/min_spd + end_control[0]

    elif dist in range(1000,1300):
        start_time = (dist-1000)/max_spd + st_control[4]
        end_time = (dist-1000)/min_spd + end_control[0] + end_control[1]

    elif dist > 1300:
        start_time = (dist-1300)/max_spd + st_control[5]
        end_time = (dist-600)/min_spd + end_control[0] + end_control[1] + end_control[2]

    #Takes the calculated time from above and seperates minutes from hours, respectively.
    start_mins, start_hours = math.modf(start_time)
    end_mins, end_hours = math.modf(end_time)

    start_hours = int(start_hours)
    start_mins = round(start_mins*60)

    end_hours = int(end_hours)
    end_mins = round(end_mins*60)
    end_mins = end_mins + extra_time


    if start_hours < 24:
        start_days = 0
    else:
        start_days = start_hours//24
        start_hours = start_hours%24

    if end_hours < 24:
        end_days = 0
    else:
        end_days = end_hours//24
        end_hours = end_hours%24
            
    opening_time = arrow_time.replace(days=+start_days, hours=+start_hours, minutes=+start_mins)
    closing_time = arrow_time.replace(days=+end_days, hours=+end_hours, minutes=+end_mins)

    opening = opening_time.format("MM/DD HH:mm")
    closing = closing_time.format("MM/DD HH:mm")

    rslt = {"open": opening, "close": closing}
    
    return jsonify(result=rslt)

#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try:
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try:
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"

#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT, host="0.0.0.0")