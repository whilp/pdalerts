#!/usr/bin/env python
# coding: utf-8

import csv
import datetime
import os
import sys
import logging

import pytz
import requests

subdomain = os.getenv("PAGERDUTY_SUBDOMAIN")   
user = os.getenv("PAGERDUTY_USER")
password = os.getenv("PAGERDUTY_PASS")
auth = (user, password)
timezone = pytz.timezone(os.getenv("TZ", "UTC"))
log = logging.getLogger()

def main():
    log.addHandler(logging.StreamHandler())
    log.level = logging.DEBUG

    API = "https://%s.pagerduty.com/api/v1" % subdomain

    since, until = sys.argv[1:3]
    emails = sys.argv[3:]

    out = csv.DictWriter(sys.stdout, (
            "timestamp", "timezone", "utc_timestamp", "hour", "week",
            "month", "day_of_week", "type", "email"),
        extrasaction="ignore")

    out.writeheader()

    for alert in alerts(since, until):
        alert.update(alert["user"])
        utc_dt = strptime(alert["started_at"])
        dt = timezone.localize(utc_dt)
        alert["timezone"] = timezone.zone
        alert["utc_timestamp"] = utc_dt.strftime("%s")
        alert["timestamp"] = dt.strftime("%s")
        alert["day_of_week"] = dt.strftime("%w")
        alert["week"] = dt.strftime("%U")
        alert["month"] = dt.strftime("%m")
        alert["hour"] = dt.strftime("%H")
        if not emails or alert["email"] in emails:
            out.writerow(alert)
               
def alerts(since, until):
    global auth
    params={"since": since, "until": until, "offset": 0}

    data = True
    while data:
        result = requests.get(API + "/alerts", auth=auth, params=params)
        
        data = result.json().get("alerts", [])
        for alert in data:
            yield alert
        params["offset"] += len(data)

def strptime(string):
    """2012-06-01T05:10:54-07:00"""
    stamp, offset = string.rsplit("-", 1)
    hours, minutes = [int(x) for x in offset.split(":")]

    dt = datetime.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S")
    dt += datetime.timedelta(hours=hours, minutes=minutes)

    return dt

if __name__ == "__main__":
    main()
