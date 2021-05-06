import logging
import requests
import json
import datetime
import urllib
import cloudscraper
from json import loads
scraper = cloudscraper.create_scraper()

def get_update(district , age) :
    date = str(f"{datetime.datetime.now():%d-%m-%Y}")
    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district}&date={date}"
    data = json.loads(url)
    results = []
    print("*********************")
    for i in range(len(data['centers'])):
        for j in range(len(data['centers'][i]['sessions'])):
            if data['centers'][i]['sessions'][j]['min_age_limit'] == age :
                if  data['centers'][i]['sessions'][j]['available_capacity'] != 0 :
                    num_vcc = json.dumps(data['centers'][i]['sessions'][j]['available_capacity'])
                    center_name = json.dumps(data['centers'][i]['name'])
                    time_slot = json.dumps(data["centers"][i]["sessions"][j]["date"])
                    msg = "Number of Vaccines : "+num_vcc +"\n"+"Vaccines avaialble at : " + center_name +"\n"+ "For Time Slot : "+time_slot
                    results.append(msg)
    if len(results) == 0:
        return(["No Vaccines Available"])
    else :
        return(results)