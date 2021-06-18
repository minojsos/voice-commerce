from flask import Flask
from flask import request, make_response, jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS, cross_origin

from flask import request, make_response, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime as dt

from models.cart import Cart
from models.cartitem import CartItem
from models.user import User
from models.shop import Shop
from models.coupon import Coupon
from models.list import List
from models.listitem import ListItem
from models.category import Category
from models.item import Item
from models.order import Order
from models.orderitem import OrderItem
from models.usercoupon import UserCoupon

import requests, os, sys
import json
import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
# from gtts import gTTS
import os
warnings.filterwarnings('ignore')

import speech_recognition as sr

import nltk
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'root',
#     'host': 'cluster0.vxgus.mongodb.net',
#     'username': 'root',
#     'password': 'root',
#     'port': 27017
# }

CORS(app)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

#for downloading package files can be commented after First run
nltk.download('popular', quiet=True)
nltk.download('nps_chat',quiet=True)
nltk.download('punkt') 
nltk.download('wordnet')

# You have 50 free calls per day, after that you have to register somewhere
# around here probably https://cloud.google.com/speech-to-text/
GOOGLE_SPEECH_API_KEY = 'AIzaSyADxOB7Npq1-Q5cj5A2Zm-oKRIrzjnIbe0'

# NanoNets Model Details
model_id = os.environ.get('NANONETS_MODEL_ID')
api_key = os.environ.get('NANONETS_API_KEY')

# Keyword Matching
RESPONSE_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
RESPONSE_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def fixResponse(sentence):
    """If user's input is a fixed response, return a response that is already stored"""
    for word in sentence.split():
        if word.lower() in RESPONSE_INPUTS:
            return random.choice(RESPONSE_RESPONSES)

# Generating response and processing 
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

"""
------
Build NLP Classifier using NaiveBayesClassifier
Text with existing Text Corpus.
------
"""
def build_nlp_model():
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    # To Recognise input type as QUES. 
    def dialogue_act_features(post):
        features = {}
        for word in nltk.word_tokenize(post):
            features['contains({})'.format(word.lower())] = True
        return features
    featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)


"""
-----
OCR
-----
Convert an Image to text that we need to show in the UI
"""
@app.route('/predict', methods=['GET'])
@cross_origin(origin='*')
def predict_ocr():
    """Generate Text which is in the image"""
    if request.method == "POST":
        if "listFile" not in request.files:
            return jsonify({"result":False,"msg":"No List File Found"})
        
        file = request.files["listFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":"No List File Found"})
        
        if file:
            # Save Image and Call the NanoNets API with the Model ID and file.
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(image_path)

            url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/' + model_id + '/LabelFile/'

            data = {'file': open(image_path, 'rb'),    'modelId': ('', model_id)}

            response = requests.post(url, auth=requests.auth.HTTPBasicAuth(api_key, ''), files=data)

            print(response.text)
            return jsonify({"result":True,"msg":"Successfully Converted Image to Text Data","data":response.text})
    else:
        return jsonify({"result":False,"msg":"Invalid Method"})



"""
User Register - Speech to Text Endpoint
---------------------------------------
This Endpoint will get the User's Speech along with a Flag to indicate whether it is one of the following:
1. User's Full Name
2. Email
3. Phone Number
4. Address
5. Save => Indicating to Save all the user's details with all of the above along with the Latitude and Longitude
"""
@app.route('/register', methods=['POST'])
@cross_origin(origin='*')
def register_user():
    line = None
    flag = None
    if request.method == "POST":
        flag = request.form["flag"]
        # Check if the POST Request has the File Part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        file = request.files['audioFile']
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})

        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            
            line = recognizer.recognize_sphinx(audio_data, language="en-US")

            # line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")

            if (flag.lower() == "name"):
                # This is the Name of the user
                return jsonify({"result":True,"msg":"","flag":"register-process","data":line})
            elif (flag.lower() == "email"):
                # This is the Email of the user
                return jsonify({"result":True,"msg":"","flag":"register-process","data":line})
            elif (flag.lower() == "phone"):
                # This is the Phone Number of the user
                return jsonify({"result":True,"msg":"","flag":"register-process","data":line})
            elif (flag.lower() == "address"):
                # This is the Address of the user
                return jsonify({"result":True,"msg":"","flag":"register-process","data":line})
            elif (flag.lower() == "save"):
                try:
                    # Save the user in the database
                    name = request.form["name"]
                    email = request.form["email"]
                    phone = request.form["phone"]
                    address = request.form["address"]
                    latitude = request.form["latitude"]
                    longitude = request.form["longitude"]

                    User(name=name, email=email,phone=phone,address=address,latitude=latitude,longitude=longitude).save()

                    return jsonify({"result":True,"msg":"Successfully Registered User","flag":"register-success"})
                except:
                    return jsonify({"result":False,"msg":"Failed to Register User","flag":"register-error"})
            else:
                return jsonify({"result":False,"msg":"Invalid Flag","flag":"register-error"})
        else:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":"Invalid Request Method","flag":"register-error"})

"""
User Login - Speech to Text Endpoint
---------------------------------------
This Endpoint will get the User's Speech to log the user into the app:
The Email is taken as the input and the converted to text. the user details
are then retrieved from the database and returned.
"""
@app.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login_user():
    line = None
    flag = None
    if request.method == "POST":
        flag = request.form["flag"]
        # Check if the POST Request has the File Part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        file = request.files['audioFile']
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})

        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")
            line = recognizer.recognize_sphinx(audio_data, language="en-US")
            line=line.replace('at','@')
            line=line.replace('dot','.')
            line=line.replace(' ', '')

            loggedin_user = User.objects(email=line).first()

            if (loggedin_user != None):
                return jsonify({"result":True,"msg":"Successfully Logged In!","flag":"login-success"})
            else:
                return jsonify({"result":False,"msg":"Failed to Login!","flag":"login-error"})
        else:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":"Invalid Request Method","flag":"login-error"})

"""
Language Picker - English or Tamil
"""
@app.route('/language', methods=["POST"])
@cross_origin(origin='*')
def language_picker():
    """Convert Speech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        file = request.files['audioFile']
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")
            line = recognizer.recognize_sphinx(audio_data, language="en-US")

            if ("english" in line) and ("tamil" not in line):
                return jsonify({"result":False,"msg":"You have Chosen English","flag":"language-success","language":"english"})
            elif ("english" not in line) and ("tamil" in line):
                return jsonify({"result":False,"msg":"You have Chosen Tamil","flag":"language-success","language":"tamil"})
            elif ("english" in line) and ("tamil" in line):
                return jsonify({"result":False,"msg":"Invalid Language Chosen","flag":"language-error","language":"invalid"})
            else:
                return jsonify({"result":False,"msg":"Invalid Language Chosen","flag":"language-error","language":"invalid"})
            
        else:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":"Invalid Request Method","flag":"language-error"})

"""
Navigation - English
-----
Convert Speech to Text using Google Speech to Text and Check what the Chosen Menu Item is.
"""
@app.route('/navigation/en', methods=["POST"])
@cross_origin(origin='*')
def navigation_en():
    """Convert Speech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        file = request.files['audioFile']
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")
            line = recognizer.recognize_sphinx(audio_data, language="en-US")

            if "voice search" in line:
                return jsonify({"result":True,"msg":"You have chosen Voice Search!","flag":"voice-search"})
            elif "product list search" in line:
                return jsonify({"result":True,"msg":"You have chosen Product List Search!","flag":"create-list"})
            elif "image search" in line:
                return jsonify({"result":True,"msg":"You have chosen Image Search!","flag":"image-list"})
            elif "profile" in line:
                return jsonify({"result":True,"msg":"You have chosen to Manage your Profile!","flag":"profile"})
            elif "orders" in line:
                return jsonify({"result":True,"msg":"You have chosen to View your Orders!","flag":"order"})
            elif "assistant" in line:
                return jsonify({"result":True,"msg":"You have chosen to use our Light Now Assistant","flag":"assistant"})
            else:
                return jsonify({"result":True,"msg":"The menu item you picked is invalid!","flag":"navigation-error"})
        else:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":"Invalid Request Method","flag":"navigation-error"})

"""
Navigation - Tamil
-----
Convert Speech to Text using Google Speech to Text and Check what the Chosen Menu Item is.
"""
@app.route('/navigation/ta', methods=["POST"])
@cross_origin(origin='*')
def navigation_ta():
    """Convert Speech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        file = request.files['audioFile']
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="ta-LK")

            return jsonify({"result":True})
        else:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":"Invalid Request Method","flag":"navigation-error"})

"""
Voice Search - Create List (EN)
----
This Endpoint allows to Search for Each item and Allow User to Pick the Item they Want to Add to their Cart.
"""
@app.route('/voicesearch/en', methods=["GET","POST"])
@cross_origin(origin='*')
def voicesearch_en():
    """ Convert Speeech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found!"})
        
        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")
            line = recognizer.recognize_sphinx(audio_data, language="en-US")

            # We Search Based on the Item Name in the Audio - Expected Audio Format: Item [Item Name] [Qty] [Unit] - Item Rice 2KG
            if "item" in line:
                # Split By Space Assuming the Text is in the said format - Add some checks to Confirm the format
                item_det = line.split(" ")
                item_name = item_det[1] # Item Name
                item_qty = item_det[2] # Item Quantity
                item_unit = item_det[3] # Item Unit

                # Check if the Item exists by the name
                item = Item.objects(item_name=item_name).first()
                if (item != None):
                    item_jsn = item.to_json() # Convert it to JSON
            
                    # Check if item is already in cart - then edit. Else New Item
                    cart = Cart.objects(user_id=request.form["userId"]).first().to_json()
                    if cart is not None:
                        
                        # Cart Already Exists - Check if item is in Cart Alrady
                        cartitem = CartItem(cart_id=cart["cart_id"],item_id=item_jsn["item_id"])
                        if (cartitem is None):
                            
                            # If Item is not in 
                            if (item_jsn["item_stock"] >= item_qty):
                                # Stock Available
                                # Add to Cart and Send Response Back to User
                                CartItem(cart_id=cart["cart_id"], item_id=item_jsn["item_id"], item_name=item_jsn["item_name"], item_code=item_jsn["item_code"], item_rate=item_jsn["item_rate"], item_offer_price=item_jsn["item_offer_price"], item_qty=item_qty).save() # Save the Item to the Cart
                                return jsonify({"result":True,"msg":"Item with name " + item_name + " and Quantity " + item_qty + " has been successfully added to your Cart!","flag":"search-success"})
                            
                            else:
                                return jsonify({"result":False,"msg":"Item with name " + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!","flag":"search-error"})
                        else:
                            # Item Already in Cart. So Update the Existing
                            cartitm_item_qty = cartitem.to_json()["item_qty"]
                            if (item_jsn["item_stock"] >= (cartitm_item_qty + item_qty)):
                                # Stock Available
                                cartitem.update(item_qty=(cartitm_item_qty+item_qty))
                                return jsonify({"result":True,"msg":"Item with name " + item_name + " and Quantity " + item_qty + " has been successfully updated in your Cart! New Quantity is " + str((cartitm_item_qty + item_qty)),"flag":"search-success"})
                            
                            else:
                                # Stock Not Available
                                return jsonify({"result":False,"msg":"Item with name " + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!", "flag":"search-error"})

                    else:
                        
                        # New Cart - No need to check if Item is in cart already
                        # Check if Item is in Stock
                        if (item_jsn["item_stock"] >= item_qty):
                            
                            # Sotck Available
                            # Add Item to Cart and Send Response Back to User
                            cart = Cart(user_id=request.form["userId"]).save() # Create New Cart and get the Cart Object
                            CartItem(cart_id=cart.cart_id, item_id=item_jsn["item_id"], item_name=item_jsn["item_name"], item_code=item_jsn["item_code"], item_rate=item_jsn["item_rate"], item_offer_price=item_jsn["item_offer_price"], item_qty=item_qty).save() # Save the Item to the Cart

                            return jsonify({"result":True,"msg":"Item with name " + item_name + " and Quantity " + item_qty + " has been successfully added to your Cart!", "flag":"search-success"})
                        
                        else:
                            return jsonify({"result":False,"msg":"Item with name " + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!","flag":"search-error"})
                
                else:
                    return jsonify({"result":False, "msg":"Item with name " + item_name + " not found!","flag":"search-error"})
            elif "save changes" in line:
                # Save the Cart and Proceed to next screen to confirm
                # Get the Current Cart of the User. So Expects the userId
                user_id = request.form["userId"]
                cart = Cart.objects(user_id=user_id).first()
                cartitems = CartItem.objects(cart_id=cart.to_json()["cart_id"])
                items = Item.objects(shop_id=cart.to_json()["shop_id"])
                
                return jsonify({"result":True,"msg":"Successfully Saved Cart","flag":"search-save","cart":cart.to_json(),"cartitems":cartitems.to_json(),"items":items.to_json()})
            elif "alter" in line:
                # Take the user back to the Edit Screen
                user_id = request.form["userId"]
                cart = Cart.objects(user_id=user_id).first()
                cartitems = CartItem.objects(cart_id=cart.to_json()["cart_id"])
                items = Item.objects(shop_id=cart.to_json()["shop_id"])
                
                return jsonify({"result":True,"msg":"You can now edit the items in your cart","flag":"search-edit","cart":cart.to_json(),"cartitems":cartitems.to_json(),"items":items.to_json()})
            elif "search" in line:
                # Search it Against the Availability
                # not in first 50% - Instead take them to the Place Order Page
                user_id = request.form["userId"]
                cart = Cart.objects(user_id=user_id).first()
                cartitems = CartItem.objects(cart_id=cart.to_json()["cart_id"])
                items = Item.objects(shop_id=cart.to_json()["shop_id"])
                
                return jsonify({"result":True,"msg":"Your Total Bill Amount is <INSERT AMOUNT HERE>. The following are the items in your cart.","flag":"search-edit","cart":cart.to_json(),"cartitems":cartitems.to_json(),"items":items.to_json()})
            elif "place order" in line:
                # Get the user's address and total amount to be paid - Total of All Items
                user_id = request.form["userId"]
                cart = Cart.objects(user_id=user_id).first().to_json()
                cartitems = CartItem.objects(cart_id=cart["cart_id"])
                user = User.objects(user_id=user_id).first().to_json()
                total=0

                return jsonify({"result":True,"msg":"Your order can now be placed","address":user["user_address"],"total":total,"payment":"Cash On Delivery"})
                # Iterate and tally the total
            elif "checkout" in line:
                # Place the Order by Moving the Cart to the Order and CartItem to OrderItem
                # Empty the Cart
                user_id = request.form["userId"]
                cart = Cart.objects(user_id=user_id).first().to_json()
                cartitems = CartItem.objects(cart_id=cart["cart_id"])

                # Iterate Each item in the Cart and Save it to CarItem
                order = Order().save().to_json()
                for item in cartitems:
                    item = item.to_json()
                    OrderItem(order_id=order["order_id"],item_id=item["item_id"],item_name=item["item_name"],item_code=item["item_code"],item_rate=item["item_rate"],item_offer_price=item["item_offer_price"],item_qty=item["item_qty"]).save()
                    
                # delete all items from the Cart
                
                return jsonify({"result":True,"msg":"Your Order has been placed successfully"})
            else:
                return jsonify({"result":False,"msg":"Invalid Audio Command","flag":"search-error"})
        
        else:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":"Invalid Request Method","flag":"search-error"})

"""
Voice Search - Create List (LK)
----
This Endpoint allows to Search for Each item and Allow User to Pick the Item they Want to Add to their Cart.
"""
@app.route('/voicesearch/ta', methods=["POST"])
@cross_origin(origin='*')
def voicesearch_ta():
    """ Convert Speeech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found!"})
        
        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="ta-LK")

            return jsonify({"result":True})
        else:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":"Invalid Request Method","flag":"navigation-error"})

"""
Voice Assistant - EN
-----
Retrieve Data based on wht is requested from the Voice Assistant
"""
@app.route('/voicebot/en', methods=["POST"])
@cross_origin(origin='*')
def voiceassist_en():
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")
            line = recognizer.recognize_sphinx(audio_data, language="en-US")

            if ("coupon" in line) or ("coupons" in line):
                # Retrieve All Coupons - Check usercoupon for each coupon to ensure that it is not used
                user_id=request.form["userId"]
                coupons = Coupon.objects().to_json()
                usercoupons = UserCoupon.objects(user_id=user_id).to_json()

                return jsonify({"result":True,"msg":"The following are the available coupons","flag":"coupon-success"})
            elif ("offer" in line) or ("offers" in line):
                # Retrieve All Offers - Where item_offer_price is not None
                items = Item.objects.filter(item_offer_price__isnull=False).to_json()
                shops = Shop.objects().to_json()

                return jsonify({"result":True,"msg":"The following are the items that are on offer in different shops!","flag":"offer-success","items":items,"shops":shops})
            
            elif ("order" in line) or ("orders" in line):
                return jsonify({"result":True,"msg":"Do you want to see Completed Orders, Cancelled Orders or Pending Orders","flag":"order-menu"})
            
            elif ("pending" in line) or ("pending orders" in line):
                # Retrieve Pending orders
                orders = Order.objects(order_status=0).to_json()
                return jsonify({"result":True, "msg":"The following are the currently pending orders that you have!","flag":"order-pending","orders":orders})
            
            elif ("completed" in line) or ("completed orders" in line):
                # Retrieve Completed Orders
                orders = Order.objects(order_status=1).to_json()
                return jsonify({"result":True, "msg":"The following are the currently completed orders that you have!","flag":"order-completed","orders":orders})
            
            elif ("cancelled" in line) or ("cancelled orders" in line):
                # Retrieve Cancelled Orders
                orders = Order.objects(order_status=1).to_json()
                return jsonify({"result":True, "msg":"The following are the currently cancelled orders that you have!","flag":"order-cancelled","orders":orders})

            elif ("cancel order" in line):
                # Cancel a Specific order assuming the speech is in the format: Cancel Order <ORDERID> - Check if Order is Pending (Not Completed or Already Cancelled). Ask user to give reason.
                return None
            elif ("received order" in line):
                # Received a Specifc order assuming the speech is in the format: Received order <ORDERID> - Check if Order is Pending (Not Completed or Already Cancelled). Ask for review.
                return None
            elif ("return order" in line):
                # Return a Specific Order sssuming the speech is in the format: Return Order <ORDERID> - Check if the Order is Pending (Not Completed or Already Cancelled). Ask for reason.
                return None
            elif ("profile" in line):
                # Get the Profile Details
                return None
        else:
            return jsonify({"result":False,"msg":"No Audio Found!","flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":"Invalid Request Method","flag":"assistant-error"})
    return jsonify({"result":True,"msg":"Successfully Retrieved All"})

"""
Voice Assistant - TA
-----
Retrieve Data based on wht is requested from the Voice Assistant
"""
@app.route('/voicebot/en', methods=["POST"])
@cross_origin(origin='*')
def voiceassist_ta():
    return jsonify({"result":True,"msg":"Successfully Retrieved All"})

"""
-----
Speech to Text - English
-----
Convert Speech to Text using Google Speech to Text
"""
@app.route('/speech/en', methods=["GET", "POST"])
@cross_origin(origin='*')
def speech_to_text_en():
    """Convert Speech to Text"""
    extra_line = ''
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found"})

        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found"})

        if file:
            # Speech Recognition stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # extra_line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")
            extra_line = recognizer.recognize_sphinx(audio_data, language="en-US")

            # Saving the file.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Check what the command is
            if "create" in extra_line and "list" in extra_line:
                return jsonify({"result":True,"msg":"You can now create a list!","flag":"create-list"})
            
            # Check which command this is
            if "coupons" in extra_line:
                # Get All Coupons
                print("Retrieve all Coupons")

            elif "view cart" in extra_line:
                # Retrieve Cart
                print("Retrieve Users Cart - If Exists")

            elif "find nearest shops" in extra_line:
                # Retrieve all nearest shops
                print("Find Nearest Shops based on Latitude and Longitude")

            elif "item" in extra_line:
                # If the Word Item is in the Audio then retrieve all the items from the database and check if name matches
                items = Item.query.all()
                for itm in items:
                    if (itm.item_code in extra_line):
                        # Item Code is in the Speech
                        # Check quantity

                        return jsonify({"result":True,"item":itm})


            return jsonify({"result":True,"msg":"Successfully Converted Speech to Text","command":extra_line})
    else:
        return jsonify({"result":False,"msg":"Invalid Method"})

"""
Search Items given the List as a JSON
- Works for both Voice Search and OCR Search
- Searches Through the Items List (Assuming One Shop Only) and identifies all the available items along with the percentage available.
"""
@app.route('/search', methods=["GET", "POST"])
@cross_origin(origin='*')
def search_items():
    """Search Text based List against the Database"""
    extra_line = ''
    if request.method == "POST":
        # Read the item list
        items = json.loads(request.json['items'])
        items_db = []
        num_items = 0
        total_items = len(items)

        for itm in items:
            # Check Against the Database for Item (One Shop Only for Now)
            item_db = Item.query().filter_by(item_name = itm['item_name'])
            items_db.append(item_db)
        
        for i in range(0, len(items_db)):
            if (items_db[i] != None and items[i]['item_qty'] <= items_db[i].item_stock):
                num_items = num_items + 1
        
        percentage = (num_items/total_items)*100

        print("Percentage : " + str(percentage))

        return jsonify({"result":True,"originalItems":items, "foundItems":items_db, "totalItems":total_items, "numItems": num_items, "percentage": percentage})


"""
-----
Speech to Text - Tamil
-----
Convert Speech to Text using Google Speech to Text
"""
@app.route('/speech/ta', methods=["GET", "POST"])
@cross_origin(origin='*')
def speech_to_text_ta():
    """Convert Speech to Text"""
    extra_line = ''
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":"No Audio Found"})

        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":"No Audio Found"})

        if file:
            # Speech Recognition stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(
                audio_data, key=GOOGLE_SPEECH_API_KEY, language="ta-LK"
            )
            extra_line = f'Your text: "{text}"'

            # Saving the file.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            return jsonify({"result":True,"msg":"Successfully Converted Speech to Text","command":extra_line})
    else:
        return jsonify({"result":False,"msg":"Invalid Method"})

"""
------
SHOP
------
"""
@app.route('/shops', methods=['GET'])
@cross_origin(origin='*')
def get_all_shops():
    """Retrieve all shops from our database."""
    shops = Shop.objects().to_json()

    return jsonify({"result":True,"msg":"Found the following shops","data":shops})

@app.route('/shop/<int:shop_id>', methods=['GET'])
@cross_origin(origin='*')
def get_shop(shop_id):
    """Retrieve the Shop with the Given Shop ID"""
    shop = Shop.objects(shop_id=shop_id).first().to_json()
    
    return jsonify({"result":True,"msg":"Found the shop you were looking for","data":shop})

@app.route('/shop', methods=['POST'])
@cross_origin(origin='*')
def new_shop():
    """ Add New Shop to our Database."""
    shop_name = request.args.post('shop_name')
    shop_phone = request.args.post('shop_phone')
    shop_addr = request.args.post('shop_address')
    shop_email = request.args.post('shop_email')
    shop_lat = request.args.post('shop_lat')
    shop_long = request.args.post('shop_long')
    shop_available = request.args.post('shop_available')

    """Create a user via query string parameters."""
    new_shop = Shop(shop_name=shop_name, shop_phone=shop_phone, shop_address=shop_addr, shop_email=shop_email, shop_lat=shop_lat, shop_long=shop_long, shop_available=shop_available).save()
    return jsonify({"result":True,"msg":"Successfully Created New Shop"})

@app.route('/shop/<int:shop_id>',methods=['DELETE'])
@cross_origin(origin='*')
def delete_shop(shop_id):
    """Delete a Shop given the ID of the Shop"""
    shop = Shop.objects(shop_id=shop_id).first()
    shop.delete()

    return jsonify({"result":True,"msg":"Successfully Deleted Shop with the Given ID"})

"""
------
USER
------
"""
@app.route('/users', methods=['GET'])
@cross_origin(origin='*')
def get_all_users():
    """Retrieve all Users from our database."""
    users = User.objects().to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved All Users","data":users})

@app.route('/user/<int:user_id>', methods=['GET'])
@cross_origin(origin='*')
def get_user(user_id):
    """Retrieve the User with the Given User ID"""
    user = User.objects(user_id=user_id).first().to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved User with Given ID","data":user})

@app.route('/user', methods=['POST'])
@cross_origin(origin='*')
def new_user():
    """ Add New User to our Database."""
    user_name = request.args.post('user_name')
    user_phone = request.args.post('user_phone')
    user_email = request.args.post('user_email')
    user_password = request.args.post('user_password')
    user_address = request.args.post('user_address')

    """Create a user via query string parameters."""
    new_user = User(user_name=user_name, user_phone=user_phone, user_email=user_email, user_password=user_password, user_address=user_address).save()
    return jsonify({"result":True,"msg":"Successfully Created New User"})

@app.route('/user/<int:user_id>', methods=['DELETE'])
@cross_origin(origin='*')
def delete_user(user_id):
    """Delete a User given the ID of the User"""
    user = User.objects(user_id=user_id).first()
    user.delete()

    return jsonify({"result":True,"msg":"Successfully Deleted User with the Given ID"})

"""
--------
COUPON
--------
"""
@app.route('/coupons', methods=['GET'])
def get_all_coupons():
    """Retrieve all Coupons from our database."""
    coupons = Coupon.objects().to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved All Coupons","data":coupons})

@app.route('/coupon/<int:coupon_id>',methods=['GET'])
def get_coupon(coupon_id):
    """Retrieve a Coupon given the ID of the Coupon"""
    coupon = Coupon.objects(coupon_id=coupon_id).first().to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved Coupon with Given ID","data":coupon})

@app.route('/coupon',methods=['POST'])
def new_coupon():
    """Add New Coupon to Our Database."""
    shop_id = request.args.post('shop_id')
    coupon_value = request.args.post('coupon_value')

    new_coupon = Coupon(shop_id=shop_id, coupon_value=coupon_value).save()
    return jsonify({"result":True,"msg":"Successfully Created New Coupon"})

@app.route('/coupon/<int:coupon_id>', methods=['DELETE'])
def delete_coupon(coupon_id):
    """Delete a Coupon given the ID of the Coupon"""
    coupon = Coupon.objects(coupon_id=coupon_id).first().to_json()
    coupon.delete()
    return jsonify({"result":True,"msg":"Successfully Deleted Coupon with the Given ID"})

"""
-------
ITEM
-------
"""
@app.route('/items', methods=['GET'])
def get_all_items():
    """Retrieve all items from our database."""
    items = Item.objects().to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved All Items","data":items})

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieve an item given the ID of the Item"""
    item = Item.objects(item_id=item_id).to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved Item with Given ID","data":item})

@app.route('/item', methods=['POST'])
def new_item():
    """Add New Item to Our Database."""
    item_code = request.args.post('item_code')
    shop_id = request.args.post('shop_id')
    item_name = request.args.post('item_name')
    item_stock = request.args.post('item_stock')
    item_rate = request.args.post('item_rate')
    item_unit = request.args.post('item_unit')

    new_item = Item(item_code=item_code, shop_id=shop_id, item_name=item_name, item_stock=item_stock, item_rate=item_rate, item_unit=item_unit).save()
    return jsonify({"result":True,"msg":"Successfully Created New Item"})

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item given the ID of the Item"""
    item = Item.query.get_or_404(item_id).first()
    item.delete()
    return jsonify({"result":True,"msg":"Successfully Deleted Item with the Given ID"})

"""
----------
CATEGORY
----------
"""
@app.route('/categories',methods=['GET'])
def get_all_categories():
    """Retrieve all Categories from our database."""
    categories = Category.objects().to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved All Categories","data":categories})

@app.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Retrieve a Category given the ID of the Category"""
    category = Category.objects().first().to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved Item with Given ID","data":category})

@app.route('/category',methods=['POST'])
def new_category():
    """ Add New Category to Our Database."""
    category_name = request.args.post('category_name')

    new_category = Category(category_name=category_name).save()
    return jsonify({"result":True,"msg":"Successfully Created New Category"})

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a Category given the ID of the Category"""
    category = Category.objects(category_id=category_id).first()
    category.delete()
    return jsonify({"result":True,"msg":"Successfully Deleted Category with the given ID"})

"""
------
ORDER
------
"""
@app.route('/orders',methods=['GET'])
def get_all_orders():
    """Retrieve all Orders"""
    orders = Order.objects().to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved All Orders","data":orders})

@app.route('/order/<int:order_id>',methods=['GET'])
def get_order(order_id):
    """Retrieve a Order given the ID of the Order"""
    order = Order.objects().first().to_json()
    return jsonify({"result":True,"msg":"Successfully Retrieved Order with Given ID","data":order})

@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an Order given the ID of the Order"""
    order = Order.objects(order_id=order_id).first()
    order.delete()
    return jsonify({"result":True,"msg":"Successfully Deleted Order with the given ID"})

if __name__ == "__main__":
    app.run(debug=True, threaded=True)