import requests
import json
from helpers.mail import send_mail


url = "https://www.ubereats.com/api/getFeedV1?localeCode=pt"

data = {
    "cacheKey": "JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk1hcnF1JUMzJUFBcyUyMGRlJTIwUG9tYmFsJTIyJTJDJTIycmVmZXJlbmNlJTIyJTNBJTIyQ2hJSmVYRGZMWGN6R1EwUmo0clhYbzMtaUwwJTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMmdvb2dsZV9wbGFjZXMlMjIlMkMlMjJsYXRpdHVkZSUyMiUzQTM4LjcyNDk0JTJDJTIybG9uZ2l0dWRlJTIyJTNBLTkuMTUwOTkyMiU3RA",
    "feedSessionCount": {
        "announcementCount": 0,
        "announcementLabel": ""
    },
    "showSearchNoAddress": False,
    "userQuery": "",
    "date": "",
    "startTime": 0,
    "endTime": 0,
    "carouselId": "",
    "sortAndFilters": [{
        "uuid": "2c7cf7ef-730f-431f-9072-27bc39f7c021",
        "options": [{
            "uuid": "2c7cf7ef-730f-431f-9072-26bc39f7c025"
        }]
    }],
    "marketingFeedType": "",
    "billboardUuid": "",
    "feedProvider": "",
    "promotionUuid": "",
    "targetingStoreTag": "",
    "venueUuid": "",
    "favorites": "",
    "pageInfo": {
        "offset": 0,
        "pageSize": 10000
    }}

r = requests.post(url, data=json.dumps(data), headers={
    "content-type": "application/json",
    "x-csrf-token": "x",
    "cookie": "uev2.loc=%7B%22address%22%3A%7B%22address1%22%3A%22Marqu%C3%AAs%20de%20Pombal%22%2C%22address2%22%3A%22Lisboa%22%2C%22aptOrSuite%22%3A%22%22%2C%22eaterFormattedAddress%22%3A%221250-160%20Lisboa%2C%20Portugal%22%2C%22subtitle%22%3A%22Lisboa%22%2C%22title%22%3A%22Marqu%C3%AAs%20de%20Pombal%22%2C%22uuid%22%3A%22%22%7D%2C%22latitude%22%3A38.72494%2C%22longitude%22%3A-9.1509922%2C%22reference%22%3A%22ChIJeXDfLXczGQ0Rj4rXXo3-iL0%22%2C%22referenceType%22%3A%22google_places%22%2C%22type%22%3A%22google_places%22%2C%22source%22%3A%22manual_auto_complete%22%2C%22addressComponents%22%3A%7B%22countryCode%22%3A%22PT%22%2C%22firstLevelSubdivisionCode%22%3A%22Lisboa%22%2C%22city%22%3A%22Lisboa%22%2C%22postalCode%22%3A%221250-160%22%7D%2C%22originType%22%3A%22user_autocomplete%22%7D;",
})

if r.status_code != 200:
    print("Unexpected response code.")
    print(r.status_code)
    exit()

feedItems = r.json()['data']['feedItems']
print(len(feedItems), "items")

def buyOneGetOneFreeFilterFunction(store):
    if store["type"] == "MINI_STORE":
        for signpost in store["store"]["signposts"]:
            if signpost["text"] == "Compre 1, receba 1 grátis":
                return True
    return False

buyOneGetOneIter = filter(buyOneGetOneFreeFilterFunction, feedItems)

notification_body = "";
for feedItem in buyOneGetOneIter:
    notification_body = notification_body + feedItem["store"]["title"]["text"] + "\n"

if len(notification_body) > 0:
    print(notification_body)
    send_mail('[Alert] Uber Eats - Buy One, Get One', notification_body)