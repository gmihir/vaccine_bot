import requests
import time
import tweepy
import os
import dateutil.parser
from datetime import datetime
import re
import pytz
from pytz import timezone



state = "CA"
city = "SAN DIEGO"

# twitter config
api_key = os.environ.get("API_KEY")
api_key_secret = os.environ.get("API_KEY_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


#REQUEST INFO

## cvs
cvs_request_url = os.environ.get("CVS_REQUEST_URL")

## walgreens
walgreens_request_url = os.environ.get("WALGREENS_REQUEST_URL")
walgreens_cookie = os.environ.get("WALGREENS_COOKIE")
walgreens_token = os.environ.get("WALGREENS_TOKEN")

## vons
vons_request_url = os.environ.get("VONS_REQUEST_URL")

#RESERVATION/VENDOR INFO

## cvs
cvs_reservation_url = "https://www.cvs.com/immunizations/covid-19-vaccine"
cvs_vendor = "CVS"

## walgreens
walgreens_reservation_url = "https://www.walgreens.com/findcare/vaccination/covid-19"
walgreens_vendor = "Walgreens"

## vons
vons_reservation_url = "https://www.mhealthappointments.com/covidappt"
vons_vendor = "Vons"


longitude = os.environ.get("LONGITUDE")
latitude = os.environ.get("LATITUDE")


found_vaccine_cvs = False
found_vaccine_vons = False
found_vaccine_walgreens = False

timestamp = datetime.now(tz=pytz.utc)
timestamp = timestamp.astimezone(timezone('US/Pacific'))

current_time = datetime.now(tz=pytz.utc)
current_time = current_time.astimezone(timezone('US/Pacific'))

def checkCVSVaccineAppointment():
        global timestamp
        global found_vaccine_cvs
        

        # get response and convert to json 
        response = requests.get(cvs_request_url, headers={"Referer":"https://www.cvs.com/immunizations/covid-19-vaccine"})
        vaccine_availability = response.json()
        # print(vaccine_availability)
        timestamp = dateutil.parser.parse(vaccine_availability["responsePayloadData"]["currentTime"])
        # iterate through all cities and determine if vaccine available for desired city
        cities_json = vaccine_availability["responsePayloadData"]["data"][state]
        for city_json in cities_json:
                if(city_json["city"] == city):
                        # print(city_json["status"])
                        found_vaccine_cvs = (city_json["status"] == "Available")
                        # done looking for city, can exit loop now
                        break


def checkVonsVaccineAppointment():
        vons_response = requests.get(vons_request_url)
        vons_vaccine_availability = vons_response.json()
        if(vons_vaccine_availability):
                vons_vaccine_availability = True


def checkWalgreensVaccineAppointment():
        walgreens_referer = "https://www.walgreens.com/findcare/vaccination/covid-19/location-screening"
        walgreens_headers = {'cookie': walgreens_cookie, 'Referer': walgreens_referer, 'x-xsrf-token': walgreens_token}



def formTweetText(vendor, updated_timestamp, reservation_url):
        time_string = updated_timestamp.ctime()

        ## strip out extra spaces
        time_string = "As of: " + re.sub('\s+', ' ', time_string)
        notification_string = "Appointments found at " + vendor + " locations in San Diego!"
        reservation_string = "Schedule here:" 
        return (time_string + "\n\n" + notification_string + "\n\n" + reservation_string + "\n" + reservation_url)
        
def sendTweet(text):
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)


        api.update_status(text)
        print("Tweet sent at: " + current_time.ctime())
        print("Tweet text: " + text)


# check cvs
try:
        checkCVSVaccineAppointment()
        if(found_vaccine_cvs):
                cvs_tweet_text = formTweetText(cvs_vendor, timestamp, cvs_reservation_url)
                sendTweet(cvs_tweet_text)
        else:
                print("No CVS vaccines available at: " + current_time.ctime())
except:
        # something failed, log failure
        print("EXCEPTION IN FINDING CVS VACCINES")

## check vons
try:
        checkVonsVaccineAppointment()
        if(found_vaccine_vons):
                vons_tweet_text = formTweetText(vons_vendor, current_time, vons_reservation_url)
                sendTweet(vons_tweet_text)
        else:
                print("No Vons vaccines available at: " + current_time.ctime())
except:
        print("EXCEPTION IN FINDING VONS VACCINES")





