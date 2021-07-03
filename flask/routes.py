# https://voice-recorder-online.com/

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

import re

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
Constant Start
-----
"""

log_converted_image_2_data = "Successfully Converted Image to Text Data"
log_no_audio = "No Audio Found!"
log_invalid_method = "Invalid Method"
log_no_list_file = "No List File Found"
log_success_register_user = "Successfully Registered User"
log_fail_register_user = "Failed to Register User"
log_invalid_flag = "Invalid Flag"
log_invalid_req_method = "Invalid Request Method"
log_success_login = "Successfully Logged In!"
log_fail_login = "Failed to Login!"
log_chosen_english = "You have Chosen English"
log_chosen_tamil = "You have Chosen Tamil"
log_chosen_invalid_lang = "Invalid Language Chosen"
log_chosen_voice_search = "You have chosen Voice Search!"
log_chosen_product_list_search = "You have chosen Product List Search!"
log_chosen_image_search = "You have chosen Image Search!"
log_chosen_manage_profile = "You have chosen to Manage your Profile!"
log_chosen_view_your_orders = "You have chosen to View your Orders!"
log_chosen_light_now_assistant = "You have chosen to use our Light Now Assistant"
log_chosen_invalid_menu = "The menu item you picked is invalid!"
log_item_with_name = "Item with name "
log_success_save_cart = "Successfully Saved Cart"
log_edit_cart = "You can now edit the items in your cart"
log_total_bill_and_items_in_cart = "Your Total Bill Amount is <INSERT AMOUNT HERE>. The following are the items in your cart."
log_order_can_be_placed = "Your order can now be placed"
log_order_placed_success = "Your Order has been placed successfully"
log_invalid_audio_cmd = "Invalid Audio Command"
log_available_coupons = "The following are the available coupons"
log_item_offers_in_different_shop = "The following are the items that are on offer in different shops!"
log_view_type_of_orders = "Do you want to see Completed Orders, Cancelled Orders or Pending Orders"
log_current_pending_orders = "The following are the currently pending orders that you have!"
log_current_completed_orders = "The following are the currently completed orders that you have!"
log_success_retrieved_all = "Successfully Retrieved All"
log_success_converted_audio_2_text = "Successfully Converted Audio to Text"
log_can_create_list = "You can now create a list!"
log_success_speech_2_text = "Successfully Converted Speech to Text"
log_found_follwing_shops = "Found the following shops"
log_shops_looked_for = "Found the shop you were looking for"
log_create_new_shop = "Successfully Created New Shop"
log_delete_shop = "Successfully Deleted Shop with the Given ID"
log_success_retrieved_all_users = "Successfully Retrieved All Users"
log_success_retrieved_user = "Successfully Retrieved User with Given ID"
log_create_new_user = "Successfully Created New User"
log_delete_user = "Successfully Deleted User with the Given ID"
log_success_retrieved_all_coupons = "Successfully Retrieved All Coupons"
log_success_retrieved_coupon = "Successfully Retrieved Coupon with Given ID"
log_create_new_coupon = "Successfully Created New Coupon"
log_delete_coupon = "Successfully Deleted Coupon with the Given ID"
log_success_retrieved_all_items = "Successfully Retrieved All Items"
log_success_retrieved_category = "Successfully Retrieved Category with Given ID"
log_create_new_item = "Successfully Created New Item"
log_delete_item = "Successfully Deleted Item with the Given ID"
log_success_retrieved_all_categories = "Successfully Retrieved All Categories"
log_success_retrieved_item = "Successfully Retrieved Item with Given ID"
log_create_new_category = "Successfully Created New Category"
log_delete_category = "Successfully Deleted Category with the given ID"
log_success_retrieved_all_orders = "Successfully Retrieved All Orders"
log_success_retrieved_order = "Successfully Retrieved Order with Given ID"
log_delete_order = "Successfully Deleted Order with the given ID"
log_delete_category_Fail = "Failed to delete category / No such category"
log_delete_user_fail = "Failed to delete user / No such user"
log_shops_looked_for_failed = "Failed to retrieve shops / no such shop"
log_fail_retrieved_user = "Failed to retrieve user / no such user"
log_fail_retrieved_category = "Failed to retrieve category / no such category"
log_delete_shop_fail = "Failed to delete shop / No such shop"
log_fail_retrieved_item = "Failed to retrieve item / no such item"
log_delete_item_Fail = "Failed to delete item / No such item"
log_fail_retrieved_coupon = "Failed to retrieve coupon / no such coupon"
log_delete_coupon_fail = "Failed to delete coupon / No such coupon"
log_fail_retrieved_order = "Failed to retrieve order / no such order"
log_fail_delete_order =  "Failed to delete order / No such order"
log_available_list_coupons = "The following are the available list coupons"
log_available_list_offers = "The following are the available list offers"
log_success_order_cancelled = "Order cancellation successful"
log_fail_order_cancelled = "Order cancellation failed"
log_success_order_completed = "Order completed successful"
log_fail_order_completed = "Order completed failed"
log_success_order_returned = "Order returned successful"
log_fail_order_returned = "Order returned failed"

"""
-----
Constant End
-----
"""



"""
-----
common functions
-----
"""
# done test
def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
        #   raise Exception("Illegal word: " + word)
          return "error"

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

"""
-----
OCR
-----
Convert an Image to text that we need to show in the UI
"""
# to test
@app.route('/predict', methods=['POST'])
@cross_origin(origin='*')
def predict_ocr():
    """Generate Text which is in the image"""
    if request.method == "POST":
        if "listFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_list_file})
        
        file = request.files["listFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_list_file})
        
        if file:
            # Save Image and Call the NanoNets API with the Model ID and file.
            filename = secure_filename(file.filename)
            image_path = os.path.join('C:\\Users\\Minoj\\Documents\\', filename)
            file.save(image_path)
            model_id = '5cd82d9b-713b-476e-9497-8b620808bd8d'
            api_key = 'zBxUmD2YDUokjIRnv-Sc71TXl3UVVz5C'
            
            url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/' + model_id + '/LabelFile/'

            data = {'file': open(image_path, 'rb'),    'modelId': ('', model_id)}
 
            response = requests.post(url, auth=requests.auth.HTTPBasicAuth(api_key, ''), files=data)

            # print(response.text)

            resp = json.loads(response.text)['result'][0]['prediction']
            item_names = []
            item_qtys  = []
            item_units = []

            item_dict = {}

            for itm in resp:
                print(resp)
                if itm['label'] == 'Itemname':
                    item_names.append(itm['ocr_text'])
                elif itm['label'] == 'itemqty':
                    item_qtys.append(itm['ocr_text'])
                elif itm['label'] == 'itemunit':
                    item_units.append(itm['ocr_text'])
            
            print(item_names)
            print("\n\n")
            print(item_qtys)
            print("\n\n")
            print(item_units)
            print("\n\n")
            # Iterate Each and Create a JSON with item name, quantity (if available, else 0). Return this back to the App
            for idx, itm in enumerate(item_names):
                print(idx)
                item_dict[idx] = {}
                item_dict[idx]['item_name'] = itm
                if (len(item_qtys) > idx):
                    item_dict[idx]['item_qty'] = item_qtys[idx]
                else:
                    item_dict[idx]['item_qty'] = 0
                if (len(item_units) > idx):
                    item_dict[idx]['item_unit'] = item_units[idx]
                else:
                    item_dict[idx]['item_unit'] = 0

            return jsonify({"result":True,"msg":log_converted_image_2_data,"list":item_dict,"data":response.text})
    else:
        return jsonify({"result":False,"msg":log_invalid_method})

"""
Expected Data Format
--------------------

{"data": [{"itemname":"yoghurt","itemqty":10},{"itemname":"rice","itemqty":1},{"itemname":"oil","itemqty":1}], "userId":1}
"""
@app.route('/ocr/search', methods=['POST'])
@cross_origin(origin='*')
def ocr_search():
    """Use the List of Items to Add to Cart"""
    if request.method == "POST":
        # Read Each Item
        print("Reading")
        data = request.json['data']

        allitems = {}

        idx=0
        for itm in data:
            print(itm)
            # Use the Item name and Quantity to check if it is in stock or not
            # Return each item in the format: {"itemname":"","itemqty":10,"available":true}
            # Return as an array of objects
            item = Item.objects(item_name=itm['itemname']).first()
            if (item != None):
                item_jsn = json.loads(item.to_json()) # Convert it to JSON
        
                # Check if Quantity Available in Cart
                if (item_json["item_stock"] >= itm['itemqty']):
                    # Stock Available
                    allitems[idx] = {"item_name":itm['itemname'],"item_qty":itm['itemqty'],"item_price":item_json['item_price'],"item_offer_price":item_json['item_offer_price'],"available":True}
                else:
                    allitems[idx] = {"item_name":itm['itemname'],"item_qty":itm['itemqty'],"available":False}
            else:
                allitems[idx] = {"item_name":itm['itemname'],"item_qty":itm['itemqty'],"available":False}
            idx=idx+1

        return jsonify({"result":True,"msg":"Successfully searched items","list":allitems,"flag":"ocr-success"})
    else:
        return jsonify({"result":False,"msg":log_invalid_method,"list":None})

"""
Expected Data Format
--------------------

{"data": [{"itemname":"yoghurt","itemqty":10},{"itemname":"rice","itemqty":1},{"itemname":"oil","itemqty":1}], "userId":1}
"""
@app.route('/ocr/add', methods=['POST'])
@cross_origin(origin='*')
def ocr_addcart():
    """Use the List of Items to Add to Cart"""
    if request.method == "POST":
        # Read Each Item
        print("Reading")
        data = request.json['data']
        userId = request.json['userId']

        for itm in data:
            print(itm)
            # Add Item to Cart if not in Cart
            # Update Stock in Cart if Already in Cart
            # Do the rest similar to voice search
            # Check if the Item exists by the name
            for itm in data:
                print(itm)
                if (itm['available'] == True):
                    item = Item.objects(item_name=itm['itemname']).first()                    
                    item_jsn = json.loads(item.to_json()) # Convert it to JSON

                    # Check if item is already in cart - then edit. Else New Item
                    cart = Cart.objects(user_id=userId).first().to_json()
                    if cart is not None:
                        # Cart Already Exists - Check if item is in Cart Alrady
                        cartitem = CartItem.objects(cart_id=cart["cart_id"],item_id=item_jsn["item_id"]).first()
                        if (cartitem is None):
                            
                            # If Item is not in 
                            if (item_jsn["item_stock"] >= item_qty):
                                # Stock Available
                                # Add to Cart and Send Response Back to User
                                CartItem(cart_id=cart["cart_id"], item_id=item_jsn["item_id"], item_name=item_jsn["item_name"], item_code=item_jsn["item_code"], item_rate=item_jsn["item_rate"], item_offer_price=item_jsn["item_offer_price"], item_qty=item_qty).save() # Save the Item to the Cart
                                return jsonify({"result":True,"msg":log_item_with_name + item_name + " and Quantity " + item_qty + " has been successfully added to your Cart!","flag":"ocr-success"})
                            
                            else:
                                return jsonify({"result":False,"msg":log_item_with_name + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!","flag":"ocr-error"})
                        else:
                            # Item Already in Cart. So Update the Existing
                            cartitm_item_qty = json.loads(cartitem.to_json())["item_qty"]
                            if (item_jsn["item_stock"] >= (cartitm_item_qty + item_qty)):
                                # Stock Available
                                cartitem.update(item_qty=(cartitm_item_qty+item_qty))
                                return jsonify({"result":True,"msg":log_item_with_name + item_name + " and Quantity " + item_qty + " has been successfully updated in your Cart! New Quantity is " + str((cartitm_item_qty + item_qty)),"flag":"search-success"})
                            
                            else:
                                # Stock Not Available
                                return jsonify({"result":False,"msg":log_item_with_name + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!", "flag":"ocr-error"})

                    else:
                        # New Cart - No need to check if Item is in cart already
                        # Check if Item is in Stock
                        if (item_jsn["item_stock"] >= item_qty):
                            
                            # Sotck Available
                            # Add Item to Cart and Send Response Back to User
                            cart = Cart(user_id=request.form["userId"]).save() # Create New Cart and get the Cart Object
                            CartItem(cart_id=cart.cart_id, item_id=item_jsn["item_id"], item_name=item_jsn["item_name"], item_code=item_jsn["item_code"], item_rate=item_jsn["item_rate"], item_offer_price=item_jsn["item_offer_price"], item_qty=item_qty).save() # Save the Item to the Cart

                            return jsonify({"result":True,"msg":log_item_with_name + item_name + " and Quantity " + item_qty + " has been successfully added to your Cart!", "flag":"ocr-success"})
                        
                        else:
                            return jsonify({"result":False,"msg":log_item_with_name + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!","flag":"ocr-error"})

        return jsonify({"result":True,"msg":"Successfully added items to cart"})
    else:
        return jsonify({"result":False,"msg":log_invalid_method})

"""
Checkout
--------

"""
@app.route('/ocr/checkout', methods=['POST'])
def ocr_checkout():
    if request.method == "POST":
        # Read Each Item
        print("Reading")
        data = request.json['data']
        user_id = request.json['userId']
        # Move Cart to Order and Cart Item to Order Item        
        # Place the Order by Moving the Cart to the Order and CartItem to OrderItem
        # Empty the Cart
        cart = json.loads(Cart.objects(user_id=user_id).first().to_json())
        cartitems = CartItem.objects(cart_id=cart["cart_id"])

        # Iterate Each item in the Cart and Save it to CarItem
        order = Order().save().to_json()
        for item in cartitems:
            item = json.loads(item.to_json())
            OrderItem(order_id=order["order_id"],item_id=item["item_id"],item_name=item["item_name"],item_code=item["item_code"],item_rate=item["item_rate"],item_offer_price=item["item_offer_price"],item_qty=item["item_qty"]).save()
            
        # delete all items from the Cart
        # remove cart and cartitem
        cart = Cart.objects(cart_id= cart['cart_id']).first()
        cartitems = CartItem.objects(cart_id=cart['cart_id'])

        cartitems.delete()
        cart.delete()
        
        return jsonify({"result":True,"msg":log_order_placed_success})

"""
Place Order
-----------

"""
@app.route('/ocr/placeorder', methods=['POST'])
def ocr_placeorder():
    if request.method == "POST":
        print("Reading")
        user_id = request.json['userId']
        # Get the user's address and total amount to be paid - Total of All Items
        # coupons - Hari
        # offer - Hari
        user_id = request.form["userId"]
        cart = json.loads(Cart.objects(user_id=user_id).first().to_json())
        cartitems = json.loads(CartItem.objects(cart_id=cart["_id"]).to_json())
        user =json.loads(User.objects(user_id=user_id).first().to_json())

        couponValue = 0
        if(cart["coupon_value"] != None or cart["coupon_value"] > 0):
            couponValue = cart["coupon_value"]

        totalValue = 0
        for cartitemObj in cartitems:
            print(cartitemObj)
            if(cartitemObj["item_offer_price"] == None or cartitemObj["item_offer_price"] == 0):
                totalValue = totalValue + (float(cartitemObj["item_rate"]) * float(cartitemObj["item_qty"]))
            else:
                totalValue = totalValue + (float(cartitemObj["item_offer_price"]) * float(cartitemObj["item_qty"]))
                

        total = totalValue - couponValue

        return jsonify({"result":True,"msg":log_order_can_be_placed,"address":user["user_address"],"total":total,"payment":"Cash On Delivery"})

"""
Cancel Checkout
---------------

"""
@app.route('/ocr/cancel', methods=['POST'])
def ocr_cancel():
    if request.method == "POST":
        print("Reading")
        userId = request.json['userId']
        # Remove All Items from Cart
        cart = Cart.objects(user_id=userId).first()
        cartitems = CartItem.objects(cart_id=cart['cart_id'])
        cartitems.delete()
        cart.delete()

        return jsonify({"result":True,"msg":"Successfully Emptied Cart","flag":"ocr-cart-empty"})


# repeat - Hari
# constant - Hari
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
# done test
@app.route('/register', methods=['POST'])
@cross_origin(origin='*')
def register_user():
    line = None
    flag = None
    if request.method == "POST":
        flag = request.form["flag"]
        # Check if the POST Request has the File Part.
        if(("audioFile" not in request.files) and flag.lower() != "save"):
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        if(flag.lower() != "save"):
            file = request.files['audioFile']
            if file.filename == "":
                return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})

            if(file):
                # Speech Recognition Stuff.
                recognizer = sr.Recognizer()
                audio_file = sr.AudioFile(file)
                with audio_file as source:
                    audio_data = recognizer.record(source)
                
                # line = recognizer.recognize_sphinx(audio_data, language="en-US")

                # If empty send an error - Hari
                line = recognizer.recognize_google(audio_data, key="AIzaSyAkni5khBB5CSXPnJNO6qAts3XQCc_eYY4", language="en-IN")

                if((line == "" or line == None) and flag.lower() != "save"):
                    return jsonify({"result":False,"msg":log_invalid_audio_cmd,"flag":"invalid register-process","data":""})
                elif (flag.lower() == "" or flag.lower() == None):
                    # This is invalid flag
                    return jsonify({"result":False,"msg":log_invalid_audio_cmd,"flag":"invalid register-process","data":""})
                elif (flag.lower() == "name"):
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
                else:
                    return jsonify({"result":False,"msg":log_invalid_flag,"flag":"register-error"})
            else:
                return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        else:
            if (flag.lower() == "save"):
                try:
                    # Save the user in the database
                    name = request.form["name"]
                    email = request.form["email"]
                    phone = request.form["phone"]
                    address = request.form["address"]
                    latitude = request.form["latitude"]
                    longitude = request.form["longitude"]

                    User(user_name=name, user_email=email,user_phone=phone,user_address=address,user_lat=latitude,user_long=longitude).save()

                    return jsonify({"result":True,"msg":log_success_register_user,"flag":"register-success"})
                except:
                    return jsonify({"result":False,"msg":log_fail_register_user,"flag":"register-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"register-error"})

"""
User Login - Speech to Text Endpoint
---------------------------------------
This Endpoint will get the User's Speech to log the user into the app:
The Email is taken as the input and the converted to text. the user details
are then retrieved from the database and returned.
"""
# to test
@app.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login_user():
    line = None
    flag = None
    if request.method == "POST":
        flag = request.form["flag"]
        # Check if the POST Request has the File Part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        file = request.files['audioFile']
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})

        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_sphinx(audio_data, language="en-US")
            line = recognizer.recognize_google(audio_data, key="AIzaSyAkni5khBB5CSXPnJNO6qAts3XQCc_eYY4", language="en-IN")
            line=line.replace('at','@')
            line=line.replace('dot','.')
            line=line.replace(' ', '')

            loggedin_user = User.objects(email=line).first()

            if (loggedin_user != None):
                return jsonify({"result":True,"msg":log_success_login,"flag":"login-success"})
            else:
                return jsonify({"result":False,"msg":log_fail_login,"flag":"login-error"})
        else:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"login-error"})

"""
Language Picker - English or Tamil
"""
# done test
@app.route('/language', methods=["POST"])
@cross_origin(origin='*')
def language_picker():
    """Convert Speech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        file = request.files['audioFile']
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_sphinx(audio_data, language="en-US")
            line = recognizer.recognize_google(audio_data, key="AIzaSyAkni5khBB5CSXPnJNO6qAts3XQCc_eYY4", language="en-IN")

            if ("english" in line) and ("tamil" not in line):
                return jsonify({"result":False,"msg":log_chosen_english,"flag":"language-success","language":"english"})
            elif ("english" not in line) and ("tamil" in line):
                return jsonify({"result":False,"msg":log_chosen_tamil,"flag":"language-success","language":"tamil"})
            elif ("english" in line) and ("tamil" in line):
                return jsonify({"result":False,"msg":log_chosen_invalid_lang,"flag":"language-error","language":"invalid"})
            else:
                return jsonify({"result":False,"msg":log_chosen_invalid_lang,"flag":"language-error","language":"invalid"})
            
        else:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"language-error"})

"""
Navigation - English
-----
Convert Speech to Text using Google Speech to Text and Check what the Chosen Menu Item is.
"""
# done test
@app.route('/navigation/en', methods=["POST"])
@cross_origin(origin='*')
def navigation_en():
    """Convert Speech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        file = request.files['audioFile']
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_sphinx(audio_data, language="en-US")
            line = recognizer.recognize_google(audio_data, key="AIzaSyAkni5khBB5CSXPnJNO6qAts3XQCc_eYY4", language="en-IN")

            if "voice search" in line:
                return jsonify({"result":True,"msg":log_chosen_voice_search,"flag":"voice-search"})
            elif "product list search" in line:
                return jsonify({"result":True,"msg":log_chosen_product_list_search,"flag":"create-list"})
            elif "image search" in line:
                return jsonify({"result":True,"msg":log_chosen_image_search,"flag":"image-list"})
            elif "profile" in line:
                return jsonify({"result":True,"msg":log_chosen_manage_profile,"flag":"profile"})
            elif "orders" in line:
                return jsonify({"result":True,"msg":log_chosen_view_your_orders,"flag":"order"})
            elif "assistant" in line:
                return jsonify({"result":True,"msg":log_chosen_light_now_assistant,"flag":"assistant"})
            else:
                return jsonify({"result":True,"msg":log_chosen_invalid_menu,"flag":"navigation-error"})
        else:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"navigation-error"})

"""
Navigation - Tamil
-----
Convert Speech to Text using Google Speech to Text and Check what the Chosen Menu Item is.
"""
# to test
@app.route('/navigation/ta', methods=["POST"])
@cross_origin(origin='*')
def navigation_ta():
    """Convert Speech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        file = request.files['audioFile']
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="ta-LK")

            return jsonify({"result":True})
        else:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"navigation-error"})

"""
Voice Search - Create List (EN)
----
This Endpoint allows to Search for Each item and Allow User to Pick the Item they Want to Add to their Cart.
"""
# done test
#  
# Hari
@app.route('/voicesearch/en', methods=["GET","POST"])
@cross_origin(origin='*')
def voicesearch_en():
    """ Convert Speeech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio})
        
        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_sphinx(audio_data, language="en-US")
            line = recognizer.recognize_google(audio_data, key="AIzaSyAkni5khBB5CSXPnJNO6qAts3XQCc_eYY4", language="en-IN")

            # We Search Based on the Item Name in the Audio - Expected Audio Format: Item [Item Name] [Qty] [Unit] - Item Rice 2KG
            if "item" in line:
                # Split By Space Assuming the Text is in the said format - Add some checks to Confirm the format

                split_words = line.split("item ")
                line = split_words[1]

                item_name = "" # Item Name
                item_qty = 0 # Item Quantity
                item_unit = "" # Item Unit

                handled = False
                i = 0
                # Handle numeric numbers
                words = line.split()
                for word in words:
                    isNumeric = re.search("^[1-9]\d*(\.\d+)?$", word)
                    if(isNumeric):
                        break
                    i = i + 1

                wordsLength = len(words)
                if(wordsLength != i):
                    handled = True
                    other = line.split(" " + words[i] + " ")
                    print(other[0])
                    print(float(words[i]))
                    print(other[1])
                    
                    item_name = other[0] # Item Name
                    item_qty = float(words[i]) # Item Quantity
                    item_unit = other[1] # Item Unit

                # Handle English word numbers
                if(handled == False):
                    isFound = False
                    isDotFound = False
                    isPointFound = False

                    wordNumber = ""
                    for word in words:

                        if(word.lower() == "point"):
                            isPointFound = True
                            wordNumber = wordNumber + " point"
                        elif(word.lower() == "dot"):
                            isDotFound = True
                            wordNumber = wordNumber + " dot"
                        elif(text2int(word.lower()) != "error" and word.lower() != "and" and isFound):
                            isFound = True
                            wordNumber = wordNumber + " " + word.lower()
                        elif(text2int(word.lower()) != "error" and word.lower() != "and" and isFound == False):
                            isFound = True
                            wordNumber = word.lower()
                        elif(word.lower() == "and" and isFound == True):
                            wordNumber = wordNumber + " " + word.lower()

                    print("wordNumber: " + wordNumber)

                    numberStr = ""

                    if(isDotFound):
                        numberWords = wordNumber.split(" dot ")
                        decimals = numberWords[1].split()

                        numberStr = str(text2int(numberWords[0]))
                        numberStr = numberStr + "."
                        for decimal in decimals:
                            numberStr = numberStr + str(text2int(decimal))

                    if(isPointFound):
                        numberWords = wordNumber.split(" point ")
                        decimals = numberWords[1].split()

                        numberStr = str(text2int(numberWords[0]))
                        numberStr = numberStr + "."
                        for decimal in decimals:
                            numberStr = numberStr + str(text2int(decimal))

                    if(isDotFound == False and isPointFound == False):
                        numberStr = str(text2int(wordNumber))

                    print("numberStr: " + numberStr)
                    value = numberStr

                    other = line.split(" " + wordNumber + " ")
                    print(other[0])
                    print(float(value))
                    print(other[1])

                    item_name = other[0] # Item Name
                    item_qty = float(value) # Item Quantity
                    item_unit = other[1] # Item Unit

                item_det = line.split(" ")
                # item_name = item_det[1] # Item Name
                # item_qty = item_det[2] # Item Quantity
                # item_unit = item_det[3] # Item Unit

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
                                return jsonify({"result":True,"msg":log_item_with_name + item_name + " and Quantity " + item_qty + " has been successfully added to your Cart!","flag":"search-success"})
                            
                            else:
                                return jsonify({"result":False,"msg":log_item_with_name + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!","flag":"search-error"})
                        else:
                            # Item Already in Cart. So Update the Existing
                            cartitm_item_qty = cartitem.to_json()["item_qty"]
                            if (item_jsn["item_stock"] >= (cartitm_item_qty + item_qty)):
                                # Stock Available
                                cartitem.update(item_qty=(cartitm_item_qty+item_qty))
                                return jsonify({"result":True,"msg":log_item_with_name + item_name + " and Quantity " + item_qty + " has been successfully updated in your Cart! New Quantity is " + str((cartitm_item_qty + item_qty)),"flag":"search-success"})
                            
                            else:
                                # Stock Not Available
                                return jsonify({"result":False,"msg":log_item_with_name + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!", "flag":"search-error"})

                    else:
                        
                        # New Cart - No need to check if Item is in cart already
                        # Check if Item is in Stock
                        if (item_jsn["item_stock"] >= item_qty):
                            
                            # Sotck Available
                            # Add Item to Cart and Send Response Back to User
                            cart = Cart(user_id=request.form["userId"]).save() # Create New Cart and get the Cart Object
                            CartItem(cart_id=cart.cart_id, item_id=item_jsn["item_id"], item_name=item_jsn["item_name"], item_code=item_jsn["item_code"], item_rate=item_jsn["item_rate"], item_offer_price=item_jsn["item_offer_price"], item_qty=item_qty).save() # Save the Item to the Cart

                            return jsonify({"result":True,"msg":log_item_with_name + item_name + " and Quantity " + item_qty + " has been successfully added to your Cart!", "flag":"search-success"})
                        
                        else:
                            return jsonify({"result":False,"msg":log_item_with_name + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!","flag":"search-error"})
                
                else:
                    return jsonify({"result":False, "msg":log_item_with_name + item_name + " not found!","flag":"search-error"})
            elif "save changes" in line:
                # Save the Cart and Proceed to next screen to confirm
                # Get the Current Cart of the User. So Expects the userId
                user_id = request.form["userId"]
                cart = Cart.objects(user_id=user_id).first()
                cartitems = CartItem.objects(cart_id=cart.to_json()["cart_id"])
                items = Item.objects(shop_id=cart.to_json()["shop_id"])
                
                return jsonify({"result":True,"msg":log_success_save_cart,"flag":"search-save","cart":cart.to_json(),"cartitems":cartitems.to_json(),"items":items.to_json()})
            elif "alter" in line:
                # doubt
                # Take the user back to the Edit Screen
                user_id = request.form["userId"]
                cart = Cart.objects(user_id=user_id).first()
                cartitems = CartItem.objects(cart_id=cart.to_json()["cart_id"])
                items = Item.objects(shop_id=cart.to_json()["shop_id"])
                
                return jsonify({"result":True,"msg":log_edit_cart,"flag":"search-edit","cart":cart.to_json(),"cartitems":cartitems.to_json(),"items":items.to_json()})
            elif "search" in line:
                # doubt
                # Search it Against the Availability
                # not in first 50% - Instead take them to the Place Order Page
                user_id = request.form["userId"]
                cart = Cart.objects(user_id=user_id).first()
                cartitems = CartItem.objects(cart_id=cart.to_json()["cart_id"])
                items = Item.objects(shop_id=cart.to_json()["shop_id"])
                
                return jsonify({"result":True,"msg":log_total_bill_and_items_in_cart,"flag":"search-edit","cart":cart.to_json(),"cartitems":cartitems.to_json(),"items":items.to_json()})
            elif "place order" in line:
                # Get the user's address and total amount to be paid - Total of All Items
                user_id = request.form["userId"]
                cart = json.loads(Cart.objects(user_id=user_id).first().to_json())
                cartitems = json.loads(CartItem.objects(cart_id=cart["_id"]).to_json())
                user =json.loads(User.objects(user_id=user_id).first().to_json())

                couponValue = 0
                if(cart["coupon_value"] != None or cart["coupon_value"] > 0):
                    couponValue = cart["coupon_value"]

                totalValue = 0
                for cartitemObj in cartitems:
                    print(cartitemObj)
                    if(cartitemObj["item_offer_price"] == None or cartitemObj["item_offer_price"] == 0):
                        totalValue = totalValue + (float(cartitemObj["item_rate"]) * float(cartitemObj["item_qty"]))
                    else:
                        totalValue = totalValue + (float(cartitemObj["item_offer_price"]) * float(cartitemObj["item_qty"]))
                        

                total = totalValue - couponValue

                return jsonify({"result":True,"msg":log_order_can_be_placed,"address":user["user_address"],"total":total,"payment":"Cash On Delivery"})
                # Iterate and tally the total
            elif "checkout" in line:
                # Place the Order by Moving the Cart to the Order and CartItem to OrderItem
                # Empty the Cart
                user_id = request.form["userId"]
                address = request.form["address"]
                order_payment = request.form["order_payment"]

                cart = json.loads(Cart.objects(user_id=user_id).first().to_json())
                print("cart: " + str(cart))
                cartitems = json.loads(CartItem.objects(cart_id=cart["_id"]).to_json())
                print("cartitems: " + str(cartitems))

                # Iterate Each item in the Cart and Save it to CarItem
                print("Placed order")
                order = json.loads(Order(shop_id=cart['shop_id'], user_id=user_id, coupon_id=cart['coupon_id'], coupon_value=cart['coupon_value'], order_status=0, order_payment=order_payment, address=address).save().to_json())
                for item in cartitems:
                    print("OrderItem save: " + str(item))
                    OrderItem(order_id=order["_id"],item_id=item["_id"],item_name=item["item_name"],item_code=item["item_code"],item_rate=item["item_rate"],item_offer_price=item["item_offer_price"],item_qty=item["item_qty"]).save()
                                
                # delete all items from the Cart
                # remove cart and cartitem
                cart1 = Cart.objects(cart_id= cart['_id']).first()
                cartitems = CartItem.objects(cart_id=cart['_id'])

                # print("cart delete: " + str(cart))
                # print("cartitems delete: " + str(cartitems))
                cartitems.delete()
                cart1.delete()
                            
                return jsonify({"result":True,"msg":log_order_placed_success})
            elif "cancelorder" in line:
                # Cancel the Placed Order by Removing all items from the Cart
                # Empty the Cart
                user_id = request.form["userId"]
                cart = json.loads(Cart.objects(user_id=user_id).first().to_json())
                cart1 = Cart.objects(user_id=user_id).first()
                cartitems = CartItem.objects(cart_id=cart["_id"])

                cartitems.delete() # Delete the Cart
                cart1.delete() # Delete Cart

                return jsonify({"result":True,"msg":"Successfully Cancelled Order","flag":"cancel-order"})
            else:
                return jsonify({"result":False,"msg":log_invalid_audio_cmd,"flag":"search-error"})
        
        else:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"search-error"})

"""
Voice Search - Create List (LK)
----
This Endpoint allows to Search for Each item and Allow User to Pick the Item they Want to Add to their Cart.
"""
# to test
@app.route('/voicesearch/ta', methods=["POST"])
@cross_origin(origin='*')
def voicesearch_ta():
    """ Convert Speeech to Text"""
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio})
        
        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="ta-LK")

            return jsonify({"result":True})
        else:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"navigation-error"})

"""
Voice Assistant - EN
-----
Retrieve Data based on wht is requested from the Voice Assistant
"""
# done test
@app.route('/voicebot/en', methods=["POST"])
@cross_origin(origin='*')
def voiceassist_en():
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        # hari: list coupons
        if file:
            # userId=request.form["userId"]
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_sphinx(audio_data, language="en-US")
            line = recognizer.recognize_google(audio_data, key="AIzaSyAkni5khBB5CSXPnJNO6qAts3XQCc_eYY4", language="en-IN")

            if("list coupons" in line):
                # List all coupons according to user usage
                userId = request.form['userId']
                isCartThere = False
                isUserCouponListThere = False
                couponIdFromCart = 0
                adjustedCoupons1 = []

                allCoupons = json.loads(Coupon.objects().to_json())
                # print("allCoupons: " + str(allCoupons))

                # Retreive user's cart
                try:
                    cart = json.loads(Cart.objects(user_id=userId).first().to_json())
                    isCartThere = True
                    couponIdFromCart = cart["coupon_id"]
                    # print("cart: " + str(cart))
                    # print("couponIdFromCart: " + str(couponIdFromCart) + " available in cart")
                except:
                    isCartThere = False

                # Retreive user's used coupons
                try:
                    userCouponList = json.loads(UserCoupon.objects(user_id=userId).to_json())
                    # print("userCouponList: " + str(userCouponList))
                    isUserCouponListThere = True
                except:
                    isUserCouponListThere = False

                if(isCartThere):
                    for coupon in allCoupons:
                        if(coupon["_id"] != couponIdFromCart):
                            adjustedCoupons1.append(coupon)
                else:
                    adjustedCoupons1 = allCoupons

                if(isUserCouponListThere):
                    for coupon in adjustedCoupons1:
                        for userCoupon in userCouponList:
                            if(coupon["_id"] == userCoupon["coupon_id"]):
                                # print("coupon id: " + str(userCoupon["coupon_id"]) + " already used")
                                adjustedCoupons1.remove(coupon)  

                return jsonify({"result":True,"msg":log_available_list_coupons,"flag":"list-coupon-success","listCoupons":adjustedCoupons1})  
            elif ("complete order" in line):
                # complete order
                orderId = request.form['orderId']
                reviewReason = request.form['reviewReason']

                order = Order.objects(order_id=orderId).first()
                # print("Order: " + str(order))

                if(order["order_status"] == 0):
                    # order in processing stage.
                    try:
                        order.update(order_status=1, review_reason=reviewReason)
                        return jsonify({"result":True,"msg":log_success_order_completed, "flag":"success order completed"})
                    except:
                        return jsonify({"result":True,"msg":log_fail_order_completed, "flag":"failed to complete order"})
                else:
                    # order not in processing stage.
                    return jsonify({"result":False,"msg":log_fail_order_completed, "flag":"failed to complete order"})

            elif ("cancel order" in line):
                # cancel order
                orderId = request.form['orderId']
                cancelReason = request.form['cancelReason']

                order = Order.objects(order_id=orderId).first()
                # print("Order: " + str(order))

                if(order["order_status"] == 0):
                    # order in processing stage.
                    try:
                        order.update(order_status=2, cancel_reason=cancelReason)
                        return jsonify({"result":True,"msg":log_success_order_cancelled, "flag":"success order cancelled"})
                    except:
                        return jsonify({"result":True,"msg":log_fail_order_cancelled, "flag":"failed to cancel order"})
                else:
                    # order not in processing stage.
                    return jsonify({"result":False,"msg":log_fail_order_cancelled, "flag":"failed to cancel order"})

            elif ("return order" in line):
                # return order
                orderId = request.form['orderId']
                returnReason = request.form['returnReason']

                order = Order.objects(order_id=orderId).first()
                print("Order: " + str(order))

                if(order["order_status"] == 1):
                    # order in completed stage.
                    try:
                        order.update(order_status=3, return_reason=returnReason)
                        return jsonify({"result":True,"msg":log_success_order_returned, "flag":"success order returned"})
                    except:
                        return jsonify({"result":True,"msg":log_fail_order_returned, "flag":"failed to return order"})
                else:
                    # order not in completed stage.
                    return jsonify({"result":False,"msg":log_fail_order_returned, "flag":"failed to return order"})

            elif ("list offers" in line):
                # List all offers
                items = json.loads(Item.objects().to_json())
                for item in items:
                    if(item["item_offer_price"] == 0 or item["item_offer_price"] == None):
                        items.remove(item)

                return jsonify({"result":True,"msg":log_available_list_offers,"flag":"list-offer-success","listOffers":items})  
            elif ("add coupon to cart" in line):
                # add coupon to cart
                couponId = request.form['couponId']
                userId = request.form['userId']
                coupon = Coupon.objects(coupon_id=couponId).first()
                coupon1 = json.loads(Coupon.objects(coupon_id=couponId).first().to_json())
                cart = Cart.objects(user_id=userId).first()
                cart.update(coupon_id=coupon1["_id"], coupon_value=coupon1["coupon_value"])

            elif ("coupon" in line) or ("coupons" in line):
                # Retrieve All Coupons - Check usercoupon for each coupon to ensure that it is not used
                user_id=request.form["userId"]
                coupons = json.loads(Coupon.objects().to_json())
                print(coupons)
                usercoupons = json.loads(UserCoupon.objects(user_id=user_id).to_json())
                print(usercoupons)

                return jsonify({"result":True,"msg":log_available_coupons,"flag":"coupon-success","coupons":coupons,"usercoupons":usercoupons})
                
            elif ("offer" in line) or ("offers" in line):
                # Retrieve All Offers - Where item_offer_price is not None
                items = json.loads(Item.objects().to_json())
                for item in items:
                    if(item["item_offer_price"] == 0 or item["item_offer_price"] == None):
                        items.remove(item)
                shops = Shop.objects().to_json()

                return jsonify({"result":True,"msg":log_item_offers_in_different_shop,"flag":"offer-success","items":items,"shops":shops})
                
            elif ("order" in line) or ("orders" in line):
                return jsonify({"result":True,"msg":log_view_type_of_orders,"flag":"order-menu"})
            
            elif ("pending" in line) or ("pending orders" in line):
                # Retrieve Pending orders
                orders = Order.objects(order_status=0).to_json()
                return jsonify({"result":True, "msg":log_current_pending_orders,"flag":"order-pending","orders":orders})
            
            elif ("completed" in line) or ("completed orders" in line):
                # Retrieve Completed Orders
                orders = Order.objects(order_status=1).to_json()
                return jsonify({"result":True, "msg":log_current_completed_orders,"flag":"order-completed","orders":orders})
            
            elif ("cancelled" in line) or ("cancelled orders" in line):
                # Retrieve Cancelled Orders
                orders = Order.objects(order_status=2).to_json()
                return jsonify({"result":True, "msg":"The following are the currently cancelled orders that you have!","flag":"order-cancelled","orders":orders})

            elif ("profile" in line):
                # Get the Profile Details
                return None
        else:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"assistant-error"})

"""
Voice Assistant - TA
-----
Retrieve Data based on wht is requested from the Voice Assistant
"""
# to test
@app.route('/voicebot/ta', methods=["POST"])
@cross_origin(origin='*')
def voiceassist_ta():
    return jsonify({"result":True,"msg":log_success_retrieved_all})

"""
Example Endpoint to Convert Audio to Text
"""
# done test
@app.route('/example', methods=["POST"])
@cross_origin(origin='*')
def example_audio():
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        
        if file:
            # Speech Recognition Stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # line = recognizer.recognize_sphinx(audio_data, language="en-US")
            line = recognizer.recognize_google(audio_data, key="AIzaSyAkni5khBB5CSXPnJNO6qAts3XQCc_eYY4", language="en-IN")

            print(line)
            return jsonify({"result":True,"msg":log_success_converted_audio_2_text,"data":line})
        else:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"assistant-error"})

"""
-----
Speech to Text - English
-----
Convert Speech to Text using Google Speech to Text
"""
# to test
@app.route('/speech/en', methods=["GET", "POST"])
@cross_origin(origin='*')
def speech_to_text_en():
    """Convert Speech to Text"""
    extra_line = ''
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio})

        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio})

        if file:
            # Speech Recognition stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            # extra_line = recognizer.recognize_sphinx(audio_data, language="en-US")
            extra_line = recognizer.recognize_google(audio_data, key="AIzaSyAkni5khBB5CSXPnJNO6qAts3XQCc_eYY4", language="en-IN")

            # Saving the file.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Check what the command is
            if "create" in extra_line and "list" in extra_line:
                return jsonify({"result":True,"msg":log_can_create_list,"flag":"create-list"})
            
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


            return jsonify({"result":True,"msg":log_success_speech_2_text,"command":extra_line})
    else:
        return jsonify({"result":False,"msg":log_invalid_method})

"""
Search Items given the List as a JSON
- Works for both Voice Search and OCR Search
- Searches Through the Items List (Assuming One Shop Only) and identifies all the available items along with the percentage available.
"""
# to test
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
# to test
@app.route('/speech/ta', methods=["GET", "POST"])
@cross_origin(origin='*')
def speech_to_text_ta():
    """Convert Speech to Text"""
    extra_line = ''
    if request.method == "POST":
        # Check if the post request has the file part.
        if "audioFile" not in request.files:
            return jsonify({"result":False,"msg":log_no_audio})

        file = request.files["audioFile"]
        if file.filename == "":
            return jsonify({"result":False,"msg":log_no_audio})

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

            return jsonify({"result":True,"msg":log_success_speech_2_text,"command":extra_line})
    else:
        return jsonify({"result":False,"msg":log_invalid_method})

"""
------
SHOP
------
"""
# done test
@app.route('/shops', methods=['GET'])
@cross_origin(origin='*')
def get_all_shops():
    """Retrieve all shops from our database."""
    shops = Shop.objects().to_json()

    return jsonify({"result":True,"msg":log_found_follwing_shops,"data":shops})

# done test
@app.route('/shop/<int:shop_id>', methods=['GET'])
@cross_origin(origin='*')
def get_shop(shop_id):
    """Retrieve the Shop with the Given Shop ID"""
    try:
        shop = Shop.objects(shop_id=shop_id).first().to_json()
        return jsonify({"result":True,"msg":log_shops_looked_for,"data":shop})
    except:
        return jsonify({"result":False,"msg":log_shops_looked_for_failed,"data":None})

# done test
@app.route('/shop', methods=['POST'])
@cross_origin(origin='*')
def new_shop():
    """ Add New Shop to our Database."""
    shop_name = request.form['shop_name']
    shop_phone = request.form['shop_phone']
    shop_addr = request.form['shop_address']
    shop_email = request.form['shop_email']
    shop_lat = request.form['shop_lat']
    shop_long = request.form['shop_long']
    shop_available = request.form['shop_available']

    """Create a user via query string parameters."""
    new_shop = Shop(shop_name=shop_name, shop_phone=shop_phone, shop_address=shop_addr, shop_email=shop_email, shop_lat=shop_lat, shop_long=shop_long, shop_available=shop_available).save()
    return jsonify({"result":True,"msg":log_create_new_shop})

# done test
@app.route('/shop/<int:shop_id>',methods=['DELETE'])
@cross_origin(origin='*')
def delete_shop(shop_id):
    """Delete a Shop given the ID of the Shop"""
    try:
        shop = Shop.objects(shop_id=shop_id).first()
        shop.delete()
        return jsonify({"result":True,"msg":log_delete_shop})
    except:
        return jsonify({"result":False,"msg":log_delete_shop_fail})

"""
------
USER
------
"""
# done test
@app.route('/users', methods=['GET'])
@cross_origin(origin='*')
def get_all_users():
    """Retrieve all Users from our database."""
    users = User.objects().to_json()
    return jsonify({"result":True,"msg":log_success_retrieved_all_users,"data":users})

# done test
@app.route('/user/<int:user_id>', methods=['GET'])
@cross_origin(origin='*')
def get_user(user_id):
    """Retrieve the User with the Given User ID"""
    try:
        user = User.objects(user_id=user_id).first().to_json()
        return jsonify({"result":True,"msg":log_success_retrieved_user,"data":user})
    except:
        return jsonify({"result":False,"msg":log_fail_retrieved_user,"data":None})


# done test
@app.route('/user', methods=['POST'])
@cross_origin(origin='*')
def new_user():
    """ Add New User to our Database."""
    user_name = request.form['user_name']
    user_phone = request.form['user_phone']
    user_email = request.form['user_email']
    user_password = request.form['user_email']
    user_address = request.form['user_address']
    user_lat = request.form['user_lat']
    user_long = request.form['user_long']

    """Create a user via query string parameters."""
    new_user = User(user_name=user_name, user_phone=user_phone, user_email=user_email, user_address=user_address, user_lat=user_lat, user_long=user_long).save()
    return jsonify({"result":True,"msg":log_create_new_user})

# done test
@app.route('/user/<int:user_id>', methods=['DELETE'])
@cross_origin(origin='*')
def delete_user(user_id):
    """Delete a User given the ID of the User"""
    try:
        user = User.objects(user_id=user_id).first()
        user.delete()
        return jsonify({"result":True,"msg":log_delete_user})
    except:
        return jsonify({"result":False,"msg":log_delete_user_fail})

"""
--------
COUPON
--------
"""
# done test
@app.route('/coupons', methods=['GET'])
def get_all_coupons():
    """Retrieve all Coupons from our database."""
    coupons = Coupon.objects().to_json()
    return jsonify({"result":True,"msg":log_success_retrieved_all_coupons,"data":coupons})

# done test
@app.route('/coupon/<int:coupon_id>',methods=['GET'])
def get_coupon(coupon_id):
    """Retrieve a Coupon given the ID of the Coupon"""
    try:
        coupon = Coupon.objects(coupon_id=coupon_id).first().to_json()
        return jsonify({"result":True,"msg":log_success_retrieved_coupon,"data":coupon})
    except:
        return jsonify({"result":False,"msg":log_fail_retrieved_coupon,"data":None})

# done test
@app.route('/coupon',methods=['POST'])
def new_coupon():
    """Add New Coupon to Our Database."""
    shop_id = request.form['shop_id']
    coupon_value = request.form['coupon_value']
    coupon_available = request.form['coupon_available']

    new_coupon = Coupon(shop_id=shop_id, coupon_value=coupon_value, coupon_available=coupon_available).save()
    return jsonify({"result":True,"msg":log_create_new_coupon})

# done test
@app.route('/coupon/<int:coupon_id>', methods=['DELETE'])
def delete_coupon(coupon_id):
    """Delete a Coupon given the ID of the Coupon"""
    try:
        coupon = Coupon.objects(coupon_id=coupon_id).first()
        coupon.delete()
        return jsonify({"result":True,"msg":log_delete_coupon})
    except:
        return jsonify({"result":False,"msg":log_delete_coupon_fail})

"""
-------
ITEM
-------
"""
# done test
@app.route('/items', methods=['GET'])
def get_all_items():
    """Retrieve all items from our database."""
    items = Item.objects().to_json()
    return jsonify({"result":True,"msg":log_success_retrieved_all_items,"data":items})

# done test
@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieve an item given the ID of the Item"""
    try:
        item = Item.objects(item_id=item_id).first().to_json()
        return jsonify({"result":True,"msg":log_success_retrieved_item,"data":item})
    except:
        return jsonify({"result":False,"msg":log_fail_retrieved_item,"data":None})

# done test
@app.route('/item', methods=['POST'])
def new_item():
    """Add New Item to Our Database."""
    category_id = request.form['category_id']
    item_code = request.form['item_code']
    shop_id = request.form['shop_id']
    item_name = request.form['item_name']
    item_stock = request.form['item_stock']
    item_rate = request.form['item_rate']
    item_unit = request.form['item_unit']
    item_offer_price = request.form['item_offer_price']

    new_item = Item(item_offer_price=item_offer_price, category_id=category_id, item_code=item_code, shop_id=shop_id, item_name=item_name, item_stock=item_stock, item_price=item_rate, item_unit=item_unit).save()
    return jsonify({"result":True,"msg":log_create_new_item})

# done test
@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item given the ID of the Item"""
    try:
        item = Item.objects(item_id=item_id).first()
        item.delete()
        return jsonify({"result":True,"msg":log_delete_item})
    except:
        return jsonify({"result":False,"msg":log_delete_item_Fail})

"""
----------
CATEGORY
----------
"""
# done test
@app.route('/categories',methods=['GET'])
def get_all_categories():
    """Retrieve all Categories from our database."""
    categories = Category.objects().to_json()
    return jsonify({"result":True,"msg":log_success_retrieved_all_categories,"data":categories})

# done test
@app.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Retrieve a Category given the ID of the Category"""
    try:
        category = Category.objects(category_id=category_id).first().to_json()
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data":category})
    except:
        return jsonify({"result":False,"msg":log_fail_retrieved_category,"data":None})

# done test
@app.route('/category',methods=['POST'])
def new_category():
    """ Add New Category to Our Database."""
    category_name = request.form['category_name']

    new_category = Category(category_name=category_name).save()
    return jsonify({"result":True,"msg":log_create_new_category})

# done test
@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a Category given the ID of the Category"""
    try:
        category = Category.objects(category_id=category_id).first()
        category.delete()
        return jsonify({"result":True,"msg":log_delete_category})
    except:
        return jsonify({"result":False,"msg":log_delete_category_Fail})

"""
------
ORDER
------
"""
# done test
@app.route('/orders',methods=['GET'])
def get_all_orders():
    """Retrieve all Orders"""
    orders = Order.objects().to_json()
    return jsonify({"result":True,"msg":log_success_retrieved_all_orders,"data":orders})

# done test
@app.route('/order/<int:order_id>',methods=['GET'])
def get_order(order_id):
    """Retrieve a Order given the ID of the Order"""
    try:
        order = Order.objects(order_id=order_id).first().to_json()
        return jsonify({"result":True,"msg":log_success_retrieved_order,"data":order})
    except:
        return jsonify({"result":False,"msg":log_fail_retrieved_order,"data":None})

# done test
@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an Order given the ID of the Order"""
    try:
        order = Order.objects(order_id=order_id).first()
        order.delete()
        return jsonify({"result":True,"msg":log_delete_order})
    except:
        return jsonify({"result":False,"msg":log_fail_delete_order})

# done test
@app.route('/order',methods=['POST'])
def new_order():
    """ Add New order to Our Database."""
    shop_id = request.form['shop_id']
    user_id = request.form['user_id']
    coupon_id = request.form['coupon_id']
    coupon_value = request.form['coupon_value']

    new_order = Order(shop_id=shop_id, user_id=user_id, coupon_id=coupon_id, coupon_value=coupon_value).save()
    return jsonify({"result":True,"msg":log_create_new_category})

"""
------
Usercoupon
------
"""
# done test
@app.route('/usercoupons',methods=['GET'])
def get_all_usercoupons():
    """Retrieve all Usercoupons from our database."""
    usercoupons = UserCoupon.objects().to_json()
    return jsonify({"result":True,"msg":log_success_retrieved_all_categories,"data":usercoupons})

# done test
@app.route('/usercoupon/<int:usercoupon_id>', methods=['GET'])
def get_usercoupon(usercoupon_id):
    """Retrieve a Usercoupon given the ID of the Usercoupon"""
    try:
        usercoupon = UserCoupon.objects(id=usercoupon_id).first().to_json()
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data":usercoupon})
    except:
        return jsonify({"result":False,"msg":log_fail_retrieved_category,"data":None})

# done test
@app.route('/usercoupon',methods=['POST'])
def new_usercoupon():
    """ Add New Usercoupon to Our Database."""
    user_id = request.form['user_id']
    coupon_id = request.form['coupon_id']
    coupon_value = request.form['coupon_value']
    coupon_available = request.form['coupon_available']

    new_usercoupon = UserCoupon(user_id=user_id, coupon_id=coupon_id, coupon_value=coupon_value, coupon_available=coupon_available).save()
    return jsonify({"result":True,"msg":log_create_new_category})

# done test
@app.route('/usercoupon/<int:usercoupon_id>', methods=['DELETE'])
def delete_usercoupon(usercoupon_id):
    """Delete a usercoupon given the ID of the usercoupon"""
    try:
        usercoupon = UserCoupon.objects(id=usercoupon_id).first()
        usercoupon.delete()
        return jsonify({"result":True,"msg":log_delete_category})
    except:
        return jsonify({"result":False,"msg":log_delete_category_Fail})

"""
------
Cart
------
"""
# done test
@app.route('/carts',methods=['GET'])
def get_all_carts():
    """Retrieve all cart from our database."""
    carts = Cart.objects().to_json()
    return jsonify({"result":True,"msg":log_success_retrieved_all_categories,"data":carts})

# done test
@app.route('/cart/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    """Retrieve a cart given the ID of the cart"""
    try:
        cart = Cart.objects(cart_id=cart_id).first().to_json()
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data":cart})
    except:
        return jsonify({"result":False,"msg":log_fail_retrieved_category,"data":None})

# done test
@app.route('/cart',methods=['POST'])
def new_cart():
    """ Add New cart to Our Database."""
    shop_id = request.form['shop_id']
    user_id = request.form['user_id']
    coupon_id = request.form['coupon_id']
    coupon_value = request.form['coupon_value']
    
    new_cart = Cart(shop_id=shop_id, user_id=user_id, coupon_id=coupon_id, coupon_value=coupon_value).save()
    return jsonify({"result":True,"msg":log_create_new_category})

# done test
@app.route('/cart/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    """Delete a cart given the ID of the cart"""
    try:
        cart = Cart.objects(cart_id=cart_id).first()
        cart.delete()
        return jsonify({"result":True,"msg":log_delete_category})
    except:
        return jsonify({"result":False,"msg":log_delete_category_Fail})

"""
------
CartItem
------
"""
# done test
@app.route('/cartitems',methods=['GET'])
def get_all_cartitems():
    """Retrieve all cartitems from our database."""
    cartitems = CartItem.objects().to_json()
    return jsonify({"result":True,"msg":log_success_retrieved_all_categories,"data":cartitems})

# done test
@app.route('/cartitem/<int:cartitem_id>', methods=['GET'])
def get_cartitem(cartitem_id):
    """Retrieve a cartitem given the ID of the cartitem"""
    try:
        cartitem = CartItem.objects(id=cartitem_id).first().to_json()
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data":cartitem})
    except:
        return jsonify({"result":False,"msg":log_fail_retrieved_category,"data":None})

# done test
@app.route('/cartitem',methods=['POST'])
def new_cartitem():
    """ Add New Usercoupon to Our Database."""
    cart_id = request.form['cart_id']
    item_id = request.form['item_id']
    item_name = request.form['item_name']
    item_code = request.form['item_code']
    item_rate = request.form['item_rate']
    item_offer_price = request.form['item_offer_price']
    item_qty = request.form['item_qty']

    new_cartitem = CartItem(cart_id=cart_id, item_id=item_id, item_name=item_name, item_code=item_code, item_rate=item_rate, item_offer_price=item_offer_price, item_qty=item_qty).save()
    return jsonify({"result":True,"msg":log_create_new_category})

# done test
@app.route('/cartitem/<int:cartitem_id>', methods=['DELETE'])
def delete_cartitem(cartitem_id):
    """Delete a usercoupon given the ID of the usercoupon"""
    try:
        cartitem = CartItem.objects(id=cartitem_id).first()
        cartitem.delete()
        return jsonify({"result":True,"msg":log_delete_category})
    except:
        return jsonify({"result":False,"msg":log_delete_category_Fail})

"""
------
OrderItem
------
"""
# done test
@app.route('/orderitems',methods=['GET'])
def get_all_orderitems():
    """Retrieve all orderitems from our database."""
    orderitems = OrderItem.objects().to_json()
    return jsonify({"result":True,"msg":log_success_retrieved_all_categories,"data":orderitems})

# done test
@app.route('/orderitem/<int:orderitem_id>', methods=['GET'])
def get_orderitem(orderitem_id):
    """Retrieve a orderitem given the ID of the orderitem"""
    try:
        orderitem = OrderItem.objects(id=orderitem_id).first().to_json()
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data":orderitem})
    except:
        return jsonify({"result":False,"msg":log_fail_retrieved_category,"data":None})


# done test
@app.route('/orderitem/<int:orderitem_id>', methods=['DELETE'])
def delete_orderitem(orderitem_id):
    """Delete a orderitem given the ID of the usercoupon"""
    try:
        orderitem = OrderItem.objects(id=orderitem_id).first()
        orderitem.delete()
        return jsonify({"result":True,"msg":log_delete_category})
    except:
        return jsonify({"result":False,"msg":log_delete_category_Fail})

"""
------
TEST
------
"""
# done test
@app.route('/test',methods=['GET'])
def test_function():
    return "true"

    
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
