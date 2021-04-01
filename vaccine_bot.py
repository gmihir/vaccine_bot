import requests
import time
import tweepy

state = "CA"
city = "SAN DIEGO"

# twitter config


found_vaccine = False

def formCVSURL():
        return("https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status." + state + ".json?vaccineinfo")

def checkVaccineAppointment():
        global found_vaccine
        # form request url
        url = formCVSURL()

        # get response and convert to json 
        response = requests.get(url, headers={"Referer":"https://www.cvs.com/immunizations/covid-19-vaccine"})
        vaccine_availability = response.json()
        print(vaccine_availability)
        # iterate through all cities and determine if vaccine available for desired city
        cities_json = vaccine_availability["responsePayloadData"]["data"][state]
        for city_json in cities_json:
                if(city_json["city"] == city):
                        print(city_json["status"])
                        found_vaccine = (city_json["status"] == "Available")
                        # done looking for city, can exit loop now
                        break

        print(found_vaccine)
        
def sendTweet():
        print("found in " + "city")

checkVaccineAppointment()

print("after check call")
print(found_vaccine)
if(found_vaccine):
        print("before call")
        sendTweet()

print("after call")
