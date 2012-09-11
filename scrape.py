#!/usr/bin/env python
# coding: utf-8

import csv
import datetime
import os
import sys

import requests

subdomain = os.getenv("PAGERDUTY_SUBDOMAIN")   
user = os.getenv("PAGERDUTY_USER")
password = os.getenv("PAGERDUTY_PASS")
auth = (user, password)
API = "https://simple.pagerduty.com/api/v1"

def main():
    since, until = sys.argv[1:]

    out = csv.DictWriter(sys.stdout, ("timestamp", "type", "email"),
        extrasaction="ignore")

    out.writeheader()

    for alert in alerts(since, until):
        alert.update(alert["user"])
        alert["timestamp"] = strptime(alert["started_at"]).strftime("%s")
        out.writerow(alert)

def alerts(since, until):
    global auth
    params={"since": since, "until": until, "offset": 0}

    data = True
    while data:
        result = requests.get(API + "/alerts", auth=auth, params=params)
        data = result.json.get("alerts", [])
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
