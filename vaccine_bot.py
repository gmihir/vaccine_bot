import requests
import time
import tweepy
import os
import dateutil.parser
from datetime import datetime
import re

state = "CA"
city = "SAN DIEGO"

# twitter config
api_key = os.environ.get("API_KEY")
api_key_secret = os.environ.get("API_KEY_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

found_vaccine = False
timestamp = datetime.now()


def formCVSURL():
        return("https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status." + state + ".json?vaccineinfo")

def checkVaccineAppointment():
        global timestamp
        global found_vaccine
        # form request url
        url = formCVSURL()

        # get response and convert to json 
        response = requests.get(url, headers={"Referer":"https://www.cvs.com/immunizations/covid-19-vaccine"})
        vaccine_availability = response.json()
        # print(vaccine_availability)
        timestamp = dateutil.parser.parse(vaccine_availability["responsePayloadData"]["currentTime"])
        # iterate through all cities and determine if vaccine available for desired city
        cities_json = vaccine_availability["responsePayloadData"]["data"][state]
        for city_json in cities_json:
                if(city_json["city"] == city):
                        # print(city_json["status"])
                        found_vaccine = (city_json["status"] == "Available")
                        # done looking for city, can exit loop now
                        break



def formTweetText(updated_timestamp):
        time_string = updated_timestamp.ctime()

        ## strip out extra spaces
        time_string = "As of: " + re.sub('\s+', ' ', time_string)
        notification_string = "Appointments found at CVS locations in San Diego!"
        reservation_string = "Schedule here:" 
        reservation_url = "https://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns"
        return (time_string + "\n\n" + notification_string + "\n\n" + reservation_string + "\n" + reservation_url)
        
def sendTweet():
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        tweet_text = formTweetText(timestamp)
        api.update_status(tweet_text)
        print("Tweet sent at: " + datetime.now().ctime())

checkVaccineAppointment()

if(found_vaccine):
        sendTweet()
else:
        print("No vaccines available at: " + datetime.now().ctime())

