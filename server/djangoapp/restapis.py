import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    if "api_key" in kwargs:
        api_key = kwargs['api_key']
    else:
        api_key = ''

    print(api_key)
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs['params'], auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                            params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealer_reviews_from_cf(url, dealership):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealership=dealership)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        try:
            reviews = json_result["filtered_entries"]
        except:
            return results
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review["doc"]
            # Create a CarDealer object with values in `doc` object
            if review_doc['purchase']:
                review_obj = DealerReview(
                    dealership=review_doc['dealership'],
                    name=review_doc['name'],
                    purchase=review_doc['purchase'],
                    purchase_date=review_doc['purchase_date'],
                    review=review_doc['review'],
                    car_make=review_doc['car_make'],
                    car_model=review_doc['car_model'],
                    car_year=review_doc['car_year'],
                    sentiment="")

            else:
                review_obj = DealerReview(
                    dealership=review_doc['dealership'],
                    name=review_doc['name'],
                    purchase=review_doc['purchase'],
                    purchase_date="",
                    review=review_doc['review'],
                    car_make="",
                    car_model="",
                    car_year="",
                    sentiment="")
            
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["filtered_entries"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/03cd4645-5c60-40ac-8c3d-b5cd4e2f4998"
    api_key = "SCKoDjMCMtnxywk81KPIosg_VwOlDU7z7ExJMX-AvW9W"
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator
    )
    nlu.set_service_url(url)
    try:
        response = nlu.analyze(
            text=text,
            features=Features(sentiment=SentimentOptions(document=True))
        ).get_result()
        sent = response['sentiment']['document']['label']
    except:
        sent = "neutral"

    return sent


def post_request(url, **kwargs):
    print("POST to {} ".format(url))

    try:
        response = requests.post(url, data=kwargs['data'])
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    json_data = json.loads(response.text)
    print("With status {} ".format(status_code))
    print(json_data)
    return json_data

def post_review(doc):
    url = "https://00b8e258.us-south.apigw.appdomain.cloud/api/review"
    post_request(url, data=doc)
    return 


