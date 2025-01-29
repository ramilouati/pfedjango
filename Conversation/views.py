from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from googlesearch import search
import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
from langdetect import detect, detect_langs

model = load_model('Conversation/model.h5')
import json
import random
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
autopart=[]
karhabti=[]

intents = json.loads(open('Conversation/data.json',encoding="utf-8").read())
words = pickle.load(open('Conversation/texts.pkl','rb'))
classes = pickle.load(open('Conversation/labels.pkl','rb'))

fileModel='Conversation/finalized_model.sav'
fileScaler='Conversation/scaler.sav'
scaler= pickle.load(open('Conversation/scaler.sav', 'rb'))

m = pickle.load(open('Conversation/finalized_model.sav', 'rb'))
def fetch_top_search_results(query, num_results=10):
    search_results = search(query, num_results=num_results)
    return search_results


def scrape_autopart_data(url,res):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all list items with the given class
    list_items = soup.find_all("li", class_="items flower printitems")

    # List to hold the scraped data
    res = []
    print(list_items)


    for item in list_items:
        # Extract the image URL
        image_div = item.find("div", class_="col-sm-3 col-lg-3 printitemsWall text-center")
        image_url = image_div.find("img")["src"]

        # Extract the data from the specified element
        data_div = item.find("div", class_="col-sm-6 col-lg-6 printitemsData")
        data_text = data_div.get_text(separator="\n", strip=True)
        price_tag = soup.find('b')
     
        # Store the extracted data in a dictionary
        item_data = {
            "image_url": image_url,
            "data_text": data_text
        }
        print(item_data)
        # Append the dictionary to the list
        res.append(item_data)
        print(res.__len__())

    return res


def scrape_karhabtk_data(url,res):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")


    img_url=soup.find("img", class_="js-qv-product-cover")["src"]
    data_txt =soup.find("h1", class_="h1").get_text()
    price = soup.find("div",class_="current-price").get_text()
   
    item_data = {
            "image_url": img_url,
            "data_text": data_txt,
            "price": price
        }
    res.append(item_data)
    print(res)
    return res

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    
    ERROR_THRESHOLD = 0.6  # You can adjust this based on the performance of the model
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    # If no result exceeds the threshold, return an empty list
    if len(results) == 0:
        print("No intent found with sufficient confidence.")
        return []
    print(f"Model predictions: {res}")
    print(f"Filtered results: {results}")

    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]





def pipeline_predict (X):
  X=scaler.transform([X])
  return m.predict(X)[0]


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result
def chatbot_response(msg):
    # try:
        # Predict the intent
        ints = predict_class(msg, model)

        # If no intent is found, return the fallback response
        # if not ints:
        #     lang = detect(msg)
        #     print(f"Detected language: {lang}")
        #     return "Merci de reposer votre question, je n'ai pas compris votre question."
          
        
        # If an intent is found, return the appropriate response
        res = getResponse(ints, intents)
        print(f"Predicted intent: {ints}")
        return res
    # except Exception as e:
    #     print(f"Error: {str(e)}")
    #     # Handle any other error and default to fallback response
    #     lang = detect(msg)
    #     return "Merci de reposer votre question, je n'ai pas compris votre question."
      
  
@csrf_exempt
def talk(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        type = data.get('type', '')
        print(message)
        print(type)
        print('ff')

        if message:
            if type == "scrapping":
                top_results = fetch_top_search_results(message, num_results=10)

                print("Top 10 search results:")
                for idx, result in enumerate(top_results, 1):
                    print(f"{idx}. {result}")
                    if result.startswith("https://autopart.tn"):
                        autopart.append(result)
                    # elif result.startswith("https://www.karhabtk.tn"):
                    #     karhabti.append(result)
                print(karhabti)
                # scrape_autopart_data(autopart[0],autopart)
                # scrape_karhabtk_data(karhabti[0],autopart)
                print(autopart)
                response = [scrape_autopart_data(autopart[0],autopart),"scrapping result"]
                print(scrape_autopart_data(autopart[0],autopart))
            else:
                response = [chatbot_response(message),"chatbot"]





        return JsonResponse({'response': response})
    else:
        return HttpResponse('Method not allowed', status=405)
  
    