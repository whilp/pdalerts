# how bad is it?

Tools to visualize your pagerduty alert activity.

## Get your data

        export PAGERDUTY_SUBDOMAIN=example
        export PAGERDUTY_USER=you@example.com
        export PAGERDUTY_PASS=yourpassword

        pip install -r requirements.txt
        python ./scrape.py 2012-09-01 2012-09-10 > data.csv
