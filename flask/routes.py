# https://voice-recorder-online.com/

from logging import DEBUG, debug
from flask import Flask
from flask import request, make_response, jsonify
from flask.wrappers import Response
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
from models.storelist import StoreList

import requests, os, sys
import json
import io
import random
import string
import warnings
import numpy as np
import warnings
from collections import defaultdict
# from gtts import gTTS
import os
warnings.filterwarnings('ignore')

import speech_recognition as sr
from google.cloud import speech_v1p1beta1 as speech
import geopy.distance
from scipy.io import wavfile
import soundfile as sf


import re

from googletrans import Translator
# translator = Translator(service_urls=[
#       'translate.google.com',
#       'translate.google.co.kr',
#     ])

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': 'cluster0.vxgus.mongodb.net',
    'username': 'root',
    'password': 'root',
    'port': 27017,
    'alias':'default'
}

# app.config['MONGODB_SETTINGS'] = {'db':'testing', 'alias':'default'}

# DB_URI = "mongodb+srv://root:root@cluster0.vxgus.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# app.config["MONGODB_HOST"] = DB_URI
# app.config['MONGODB_SETTINGS'] = {
#     'alias': 'default',
#     'db': 'myFirstDatabase',
#     'host': 'mongodb+srv://root:root@cluster0.vxgus.mongodb.net',
#     'port': 27017
# }


CORS(app)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

# You have 50 free calls per day, after that you have to register somewhere
# around here probably https://cloud.google.com/speech-to-text/
GOOGLE_SPEECH_API_KEY = 'AIzaSyADxOB7Npq1-Q5cj5A2Zm-oKRIrzjnIbe0'

# NanoNets Model Details
model_id = os.environ.get('NANONETS_MODEL_ID')
api_key = os.environ.get('NANONETS_API_KEY')

# Keyword Matching
RESPONSE_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
RESPONSE_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

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
            filename = file.filename
            # image_path = os.path.join('C:\\Users\\Minoj\\Documents\\', filename)
            image_path = "C:/Users/Harrish/Desktop/tamil-list.jpg"
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

            item_dict = []

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
                indv_dict = {}
                indv_dict['item_name'] = itm
                if (len(item_qtys) > idx):
                    indv_dict['item_qty'] = item_qtys[idx]
                else:
                    indv_dict['item_qty'] = 0
                if (len(item_units) > idx):
                    indv_dict['item_unit'] = item_units[idx]
                else:
                    indv_dict['item_unit'] = 0
                
                item_dict.append(indv_dict)

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
        lang = request.json['lang']

        allitems = {}

        if lang == 'tm':
            translator = Translator()
            for item in data:
                item_name = translator.translate(item['itemname']).text
                item['itemname'] = item_name.lower()
            print(data)

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
                if (item_jsn["item_stock"] >= itm['itemqty']):
                    # Stock Available
                    allitems[idx] = {"item_name":itm['itemname'],"item_qty":itm['itemqty'],"item_price":item_jsn['item_price'],"item_offer_price":item_jsn['item_offer_price'],"available":True}
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

{"data": [{"itemname":"yoghurt","itemqty":10,"available":True},{"itemname":"rice","itemqty":1,"available":False},{"itemname":"oil","itemqty":1,"available":True}], "userId":3}
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
            if (itm['available'] == True):
                item = Item.objects(item_name=itm['itemname']).first()                    
                item_jsn = json.loads(item.to_json()) # Convert it to JSON
                # Check if item is already in cart - then edit. Else New Item
                cart = Cart.objects(user_id=userId).first()
                
                if cart is not None:
                    cart = json.loads(cart.to_json())
                    # Cart Already Exists - Check if item is in Cart Alrady
                    cartitem = CartItem.objects(cart_id=cart["_id"],item_id=item_jsn["_id"]).first()
                    
                    if (cartitem is None):
                        # If Item is not in 
                        if (item_jsn["item_stock"] >= itm['itemqty']):
                            # Stock Available
                            # Add to Cart and Send Response Back to User
                            CartItem(cart_id=cart["_id"], item_id=item_jsn["_id"], item_name=item_jsn["item_name"], item_code=item_jsn["item_code"], item_rate=item_jsn["item_price"], item_offer_price=item_jsn["item_offer_price"], item_qty=itm['itemqty']).save() # Save the Item to the Cart
                    else:
                        # Item Already in Cart. So Update the Existing
                        cartitm_item_qty = json.loads(cartitem.to_json())["item_qty"]
                        if (item_jsn["item_stock"] >= (cartitm_item_qty + itm['itemqty'])):
                            # Stock Available
                            cartitem.update(item_qty=(cartitm_item_qty+itm['itemqty']))
                else:
                    # New Cart - No need to check if Item is in cart already
                    # Check if Item is in Stock
                    if (item_jsn["item_stock"] >= itm['itemqty']):
                        
                        # Sotck Available
                        # Add Item to Cart and Send Response Back to User
                        cart = Cart(user_id=userId).save() # Create New Cart and get the Cart Object
                        CartItem(cart_id=cart.cart_id, item_id=item_jsn["_id"], item_name=item_jsn["item_name"], item_code=item_jsn["item_code"], item_rate=item_jsn["item_price"], item_offer_price=item_jsn["item_offer_price"], item_qty=itm['itemqty']).save() # Save the Item to the Cart
        return jsonify({"result":True,"msg":"Successfully added items to cart","list":data})
    else:
        return jsonify({"result":False,"msg":log_invalid_method})

"""
Edit Item
---------
"""
@app.route('/ocr/audio', methods=['POST'])
def ocr_edit():
    if request.method == "POST":
        user_id = request.form['userId']
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
            line = ""
            try:
                line = recognizer.recognize_google(audio_data, language="en-IN")
                line = line.lower()
                print(line)
            except:
                return jsonify({"result":False,"msg":"Invalid Audio File","flag":"file-error"})

    # We Search Based on the Item Name in the Audio - Expected Audio Format: Item [Item Name] [Qty] [Unit] - Item Rice 2KG
    if "go back" in line:
        return jsonify({"result":True,"msg":"You will be taken to the navigation","flag":"back"})
        
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

        print(item_name)
        print(item_qty)
        print(item_unit)

        # Banana 5 KG Delete
        if "delete" in line:
            print("Inside Delete Item")
            item = Item.objects(item_name=item_name).first()

            if (item != None):
                # Check if Item  in Cart - Remove if it is in Cart
                item_jsn = json.loads(item.to_json()) # Convert it to JSON

                # Check if item is already in cart - then edit. Else New Item
                cart = Cart.objects(user_id=request.form["userId"]).first()
                if cart is not None:
                    cart = json.loads(cart.to_json())

                    # Cart Already Exists - Check for Item in Cart and Delete
                    cartitem = CartItem.objects(cart_id=cart["_id"], item_id=item_jsn["_id"]).first()
                    if (cartitem is None):
                        # IF Item not in cart
                        return jsonify({"result":False,"msg":log_item_with_name + item_name + " not in your cart","flag":"delete-error"})
                    else:
                        itm = json.loads(item.to_json())
                        cartitem.delete()
                        return jsonify({"result":True,"msg":log_item_with_name + item_name + " deleted from cart","itemid":item_jsn["_id"],"flag":"delete-success"})
                else:
                    return jsonify({"result":False,"msg":"Empty Cart","flag":"delete-error"})
            else:
                return jsonify({"result":False, "msg":log_item_with_name + item_name + " not found!","flag":"audio-error"})
        elif "edit" in line:
            # Banana 5 KG Edit
            print("Inside Edit Item")
            item = Item.objects(item_name=item_name).first()

            if (item != None):
                # Check if Item in Cart Already
                item_jsn = json.loads(item.to_json()) # Convert it to JSON

                # Check if item is already in cart - then edit. Else New Item
                cart = Cart.objects(user_id=request.form["userId"]).first()
                if cart is not None:
                    cart = json.loads(cart.to_json())
                    # Cart Already Exists - Check if item is in Cart Already
                    cartitem = CartItem.objects(cart_id=cart["_id"], item_id=item_jsn["_id"])
                    if (cartitem is None):
                        return jsonify({"result":False,"msg":"Cannot Edit Item","flag":"edit-error"})
                    else:
                        itm = json.loads(item.to_json())
                        cartitem.update(item_qty=item_qty)
                        return jsonify({"result":True,"msg":"Successfully Updated Item","itemid":item_jsn["_id"],"flag":"edit-success"})
                else:
                    return jsonify({"result":False,"msg":"Cannot Edit Item","flag":"audio-error"})
        else:
            return jsonify({"result":False,"msg":"I do not understand this command","flag":"audio-error"})
    else:
        return jsonify({"result":False,"msg":"Cannot Edit Item","flag":"audio-error"})



"""
Checkout
--------

"""
@app.route('/ocr/checkout', methods=['POST'])
def ocr_checkout():
    if request.method == "POST":
        # Read Each Item
        print("Reading")
        user_id = request.json['userId']
        # Move Cart to Order and Cart Item to Order Item        
        # Place the Order by Moving the Cart to the Order and CartItem to OrderItem
        # Empty the Cart
        cart = Cart.objects(user_id=user_id).first()
        if (cart is not None):
            cart = json.loads(cart.to_json())
            cartitems = CartItem.objects(cart_id=cart["_id"])

            # Iterate Each item in the Cart and Save it to CarItem
            order = json.loads(Order(user_id=user_id,address="").save().to_json())
            for item in cartitems:
                item = json.loads(item.to_json())
                OrderItem(order_id=order["_id"],item_id=item["_id"],item_name=item["item_name"],item_code=item["item_code"],item_rate=item["item_rate"],item_offer_price=item["item_offer_price"],item_qty=item["item_qty"]).save()
                
            # delete all items from the Cart
            # remove cart and cartitem
            cart1 = Cart.objects(cart_id= cart['_id']).first()
            cartitems = CartItem.objects(cart_id=cart['_id'])

            cartitems.delete()
            cart1.delete()
            
            return jsonify({"result":True,"msg":log_order_placed_success,"flag":"checkout"})
        else:
            return jsonify({"result":False,"msg":"Cart Empty","flag":"checkout-error"})

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
        cart = Cart.objects(user_id=user_id).first()
        if (cart is not None):
            cart = json.loads(cart.to_json())
            cartitems = json.loads(CartItem.objects(cart_id=cart["_id"]).to_json())
            user =json.loads(User.objects(user_id=user_id).first().to_json())

            couponValue = 0
            try:
                if(cart["coupon_value"] != None or cart["coupon_value"] > 0):
                    couponValue = cart["coupon_value"]
            except:
                couponValue = 0

            totalValue = 0
            for cartitemObj in cartitems:
                print(cartitemObj)
                if(cartitemObj["item_offer_price"] == None or cartitemObj["item_offer_price"] == 0):
                    totalValue = totalValue + (float(cartitemObj["item_rate"]) * float(cartitemObj["item_qty"]))
                else:
                    totalValue = totalValue + (float(cartitemObj["item_offer_price"]) * float(cartitemObj["item_qty"]))
                    

            total = totalValue - couponValue

            return jsonify({"result":True,"msg":log_order_can_be_placed,"address":user["user_address"],"total":total,"payment":"Cash On Delivery","flag":"placeorder"})
        else:
            return jsonify({"result":False,"msg":"Cart Empty","flag":"placeorder-error"})

"""
Cancel Checkout
---------------

"""
@app.route('/ocr/cancel', methods=['POST'])
def ocr_cancel():
    if request.method == "POST":
        userId = request.json['userId']
        # Remove All Items from Cart
        cart = Cart.objects(user_id=userId).first()
        if cart is not None:
            cartitems = CartItem.objects(cart_id=cart['cart_id'])
            cartitems.delete()
            cart.delete()

            return jsonify({"result":True,"msg":"Successfully Emptied Cart","flag":"cancel"})
        else:
            return jsonify({"result":True,"msg":"Failed to Empty Cart","flag":"cancel"})

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
                
                try:
                    line = recognizer.recognize_google(audio_data, language="en-IN")
                except:
                    return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})

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

            try:
                line = recognizer.recognize_google(audio_data, language="en-IN")
            except:
                return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
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
            
            try:
                line = recognizer.recognize_google(audio_data, language="en-IN")
            except Exception as e:
                return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

            print(line)

            if ("english" in line.lower()) and ("tamil" not in line.lower()):
                return jsonify({"result":False,"msg":log_chosen_english,"flag":"language-success","language":"english"})
            elif ("english" not in line.lower()) and ("tamil" in line.lower()):
                return jsonify({"result":False,"msg":log_chosen_tamil,"flag":"language-success","language":"tamil"})
            elif ("english" in line.lower()) and ("tamil" in line.lower()):
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
            
            try:
                line = recognizer.recognize_google(audio_data, language="en-IN")
            except:
                return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})

            print(line)
            if "voice search" in line.lower():
                return jsonify({"result":True,"msg":log_chosen_voice_search,"flag":"voice-search"})
            elif "product list search" in line.lower():
                return jsonify({"result":True,"msg":log_chosen_product_list_search,"flag":"create-list"})
            elif "image search" in line.lower():
                return jsonify({"result":True,"msg":log_chosen_image_search,"flag":"image-list"})
            elif "profile" in line.lower():
                return jsonify({"result":True,"msg":log_chosen_manage_profile,"flag":"profile"})
            elif "orders" in line.lower():
                return jsonify({"result":True,"msg":log_chosen_view_your_orders,"flag":"order"})
            elif "assistant" in line.lower():
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
Get Cart
"""
@app.route('/getcart', methods=["POST"])
@cross_origin(origin='*')
def getcart():
    if request.method == "POST":
        user_id = request.form["userId"]
        cart = Cart.objects(user_id=user_id).first()
        if (cart is not None):
            cart = json.loads(cart.to_json())
            cart1 = Cart.objects(user_id=user_id).first()
            cartitems = CartItem.objects(cart_id=cart["_id"])

            print(cart)
            print(cartitems)

            return jsonify({"result":True,"cart":cart,"cartitems":json.loads(cartitems.to_json()), "msg":"The following items are in your cart"})
        else:
            return jsonify({"result":True,"cart":None,"cartitems":None,"msg":"Empty Cart"})

"""
Voice Search - Create List (EN)
----
This Endpoint allows to Search for Each item and Allow User to Pick the Item they Want to Add to their Cart.
"""
# done test
#  
# Hari
@app.route('/voicesearch', methods=["GET","POST"])
@cross_origin(origin='*')
def voicesearch():
    """ Convert Speeech to Text"""
    if request.method == "POST":
        try:
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
                line = ""
                try:
                    line = recognizer.recognize_google(audio_data, language="en-IN")
                    line = line.lower()
                    print(line)
                except:
                    return jsonify({"result":False,"msg":"Invalid Audio File","flag":"file-error"})

                # We Search Based on the Item Name in the Audio - Expected Audio Format: Item [Item Name] [Qty] [Unit] - Item Rice 2KG
                if "go back" in line:
                    return jsonify({"result":True,"msg":"You will be taken to the navigation","flag":"back"})
                elif "item" in line:
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

                    print(item_name)
                    print(item_qty)
                    print(item_unit)

                    # Banana 5 KG Delete
                    if "delete" in line:
                        print("Inside Delete Item")
                        item = Item.objects(item_name=item_name).first()

                        if (item != None):
                            # Check if Item  in Cart - Remove if it is in Cart
                            item_jsn = json.loads(item.to_json()) # Convert it to JSON

                            # Check if item is already in cart - then edit. Else New Item
                            cart = Cart.objects(user_id=request.form["userId"]).first()
                            if cart is not None:
                                cart = json.loads(cart.to_json())

                                # Cart Already Exists - Check for Item in Cart and Delete
                                cartitem = CartItem.objects(cart_id=cart["_id"], item_id=item_jsn["_id"]).first()
                                if (cartitem is None):
                                    # IF Item not in cart
                                    return jsonify({"result":False,"msg":log_item_with_name + item_name + " not in your cart","flag":"delete-error"})
                                else:
                                    itm = json.loads(item.to_json())
                                    cartitem.delete()
                                    return jsonify({"result":True,"msg":log_item_with_name + item_name + " deleted from cart","itemid":item_jsn["_id"],"flag":"delete-success"})
                            else:
                                return jsonify({"result":False,"msg":"Empty Cart","flag":"delete-error"})
                        else:
                            return jsonify({"result":False, "msg":log_item_with_name + item_name + " not found!","flag":"search-error"})
                    elif "edit" in line:
                        # Banana 5 KG Edit
                        print("Inside Edit Item")
                        item = Item.objects(item_name=item_name).first()

                        if (item != None):
                            # Check if Item in Cart Already
                            item_jsn = json.loads(item.to_json()) # Convert it to JSON

                            # Check if item is already in cart - then edit. Else New Item
                            cart = Cart.objects(user_id=request.form["userId"]).first()
                            if cart is not None:
                                cart = json.loads(cart.to_json())
                                # Cart Already Exists - Check if item is in Cart Already
                                cartitem = CartItem.objects(cart_id=cart["_id"], item_id=item_jsn["_id"])
                                if (cartitem is None):
                                    return jsonify({"result":False,"msg":"Cannot Edit Item","flag":"edit-error"})
                                else:
                                    itm = json.loads(item.to_json())
                                    cartitem.update(item_qty=item_qty)
                                    return jsonify({"result":True,"msg":"Successfully Updated Item","itemid":item_jsn["_id"],"flag":"edit-success"})
                            else:
                                return jsonify({"result":False,"msg":"Cannot Edit Item","flag":"edit=error"})

                    else:
                        # Check if the Item exists by the name
                        item = Item.objects(item_name=item_name).first()
                        if (item != None):
                            item_jsn = json.loads(item.to_json()) # Convert it to JSON
                    
                            # Check if item is already in cart - then edit. Else New Item
                            cart = Cart.objects(user_id=request.form["userId"]).first()
                            if cart is not None:
                                cart = json.loads(cart.to_json())

                                # Cart Already Exists - Check if item is in Cart Alrady
                                cartitem = CartItem.objects(cart_id=cart["_id"],item_id=item_jsn["_id"]).first()

                                if (cartitem is None):
                                    # If Item is not in 
                                    if (item_jsn["item_stock"] >= item_qty):
                                        # Stock Available
                                        # Add to Cart and Send Response Back to User
                                        CartItem(cart_id=cart["_id"], item_id=item_jsn["_id"], item_name=item_jsn["item_name"], item_code=item_jsn["item_code"], item_rate=item_jsn["item_price"], item_offer_price=item_jsn["item_offer_price"], item_qty=item_qty).save() # Save the Item to the Cart
                                        return jsonify({"result":True,"msg":log_item_with_name + item_name + " and Quantity " + str(item_qty) + " has been successfully added to your Cart!","flag":"search-success","item":{"item_name":item_name,"item_qty":item_qty,"item_unit":item_jsn["item_unit"]}})
                                    
                                    else:
                                        return jsonify({"result":False,"msg":log_item_with_name + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!","flag":"search-error"})
                                else:
                                    # Item Already in Cart. So Update the Existing
                                    newcartitem = json.loads(cartitem.to_json())
                                    print(newcartitem)
                                    cartitm_item_qty = newcartitem["item_qty"]
                                    if (item_jsn["item_stock"] >= (cartitm_item_qty + item_qty)):
                                        # Stock Available
                                        cartitem.update(item_qty=(cartitm_item_qty+item_qty))
                                        return jsonify({"result":True,"msg":log_item_with_name + item_name + " and Quantity " + str(item_qty) + " has been successfully updated in your Cart! New Quantity is " + str((cartitm_item_qty + item_qty)),"flag":"search-success","item":{"item_name":item_name,"item_qty":item_qty,"item_unit":item_jsn["item_unit"]}})
                                    
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

                                    print(item_jsn)

                                    CartItem(cart_id=cart.id, item_id=item_jsn["_id"], item_name=item_jsn["item_name"], item_code=item_jsn["item_code"], item_rate=item_jsn["item_price"], item_offer_price=item_jsn["item_offer_price"], item_qty=item_qty).save() # Save the Item to the Cart

                                    return jsonify({"result":True,"msg":log_item_with_name + item_name + " and Quantity " + str(item_qty) + " has been successfully added to your Cart!", "flag":"search-success","item":{"item_name":item_name,"item_qty":item_qty,"item_unit":item_jsn["item_unit"]}})
                                
                                else:
                                    return jsonify({"result":False,"msg":log_item_with_name + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!","flag":"search-error"})
                        
                        else:
                            return jsonify({"result":False, "msg":log_item_with_name + item_name + " not found!","flag":"search-error"})
                elif "save changes" in line:
                    # Save the Cart and Proceed to next screen to confirm
                    # Get the Current Cart of the User. So Expects the userId
                    user_id = request.form["userId"]
                    cart = Cart.objects(user_id=user_id).first()
                    cartitems = CartItem.objects(cart_id=json.loads(cart.to_json())["_id"])
                    items = Item.objects(shop_id=3)
                    
                    return jsonify({"result":True,"msg":log_success_save_cart,"flag":"search-save","cart":cart.to_json(),"cartitems":cartitems.to_json(),"items":items.to_json()})
                elif "alter" in line:
                    # doubt
                    # Take the user back to the Edit Screen
                    user_id = request.form["userId"]
                    cart = Cart.objects(user_id=user_id).first()
                    cartitems = json.loads(CartItem.objects(cart_id=json.loads(cart.to_json())["_id"]))
                    items = Item.objects(shop_id=3)

                    return jsonify({"result":True,"msg":log_edit_cart,"flag":"search-edit","cart":cart.to_json(),"cartitems":cartitems.to_json()})
                elif "search" in line:
                    # doubt
                    # Search it Against the Availability
                    # not in first 50% - Instead take them to the Place Order Page
                    user_id = request.form["userId"]
                    cart = Cart.objects(user_id=user_id).first()
                    cartitems = CartItem.objects(cart_id=json.loads(cart.to_json())["_id"])
                    items = Item.objects(shop_id=3)
                    
                    return jsonify({"result":True,"msg":"The following are the items in your cart.","flag":"search-edit","cart":cart.to_json(),"cartitems":cartitems.to_json(),"items":items.to_json()})
                elif "place order" in line or "please order" in line:
                    # Get the user's address and total amount to be paid - Total of All Items
                    user_id = request.form["userId"]
                    cart = json.loads(Cart.objects(user_id=user_id).first().to_json())
                    cartitems = CartItem.objects(cart_id=cart["_id"])
                    user = User.objects(user_id=user_id).first()
                    if (user != None):
                        user = json.loads(user.to_json())

                    couponValue = 0
                    try:
                        if(cart["coupon_value"] != None or cart["coupon_value"] > 0):
                            couponValue = cart["coupon_value"]
                    except:
                        couponValue = 0

                    totalValue = 0
                    for cartitemObj in cartitems:
                        cartitemObj = json.loads(cartitemObj.to_json())
                        if(cartitemObj["item_offer_price"] == None or cartitemObj["item_offer_price"] == 0):
                            totalValue = totalValue + (float(cartitemObj["item_rate"]) * float(cartitemObj["item_qty"]))
                        else:
                            totalValue = totalValue + (float(cartitemObj["item_offer_price"]) * float(cartitemObj["item_qty"]))
                            

                    total = totalValue - couponValue
                    
                    return jsonify({"result":True,"msg":log_order_can_be_placed,"address":user["user_address"],"total":total,"payment":"Cash On Delivery","flag":"place-order"})
                    # Iterate and tally the total
                elif "checkout" in line.replace(" ",""):
                    # Place the Order by Moving the Cart to the Order and CartItem to OrderItem
                    # Empty the Cart
                    user_id = request.form["userId"]
                    try:
                        address = line.split("out")[1]
                    except:
                        address = "Default address"

                    cart = json.loads(Cart.objects(user_id=user_id).first().to_json())
                    print("cart: " + str(cart))
                    cartitems = json.loads(CartItem.objects(cart_id=cart["_id"]).to_json())
                    print("cartitems: " + str(cartitems))

                    # Iterate Each item in the Cart and Save it to CarItem
                    print("Placed order")
                    if "coupon_id" in cart and "coupon_value" in cart:
                        order = json.loads(Order(user_id=user_id, coupon_id=cart['coupon_id'], coupon_value=cart['coupon_value'], order_status=0, order_payment=0, address=address).save().to_json())
                    else:
                        order = json.loads(Order(user_id=user_id, order_status=0, order_payment=0, address="default address").save().to_json())
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
                                
                    return jsonify({"result":True,"msg":log_order_placed_success,"flag":"checkout"})
                elif "cancel order" in line:
                    # Cancel the Placed Order by Removing all items from the Cart
                    # Empty the Cart
                    user_id = request.form["userId"]
                    cart = json.loads(Cart.objects(user_id=user_id).first().to_json())
                    cart1 = Cart.objects(user_id=user_id).first()
                    cartitems = CartItem.objects(cart_id=cart["_id"])

                    cartitems.delete() # Delete the Cart
                    cart1.delete() # Delete Cart

                    return jsonify({"result":True,"msg":"Successfully Cancelled Order","flag":"cancel-order"})
                elif "check order" in line:
                    # View your Cart
                    user_id = request.form["userId"]
                    cart = Cart.objects(user_id=user_id).first()
                    if (cart is not None):
                        cart = json.loads(cart.to_json())
                        cart1 = Cart.objects(user_id=user_id).first()
                        cartitems = CartItem.objects(cart_id=cart["_id"])

                        print(cart)
                        print(cartitems)

                        return jsonify({"result":True,"cart":cart,"cartitems":json.loads(cartitems.to_json()), "msg":"The following items are in your cart", "flag":"check-order"})
                    else:
                        return jsonify({"result":True,"cart":None,"cartitems":None,"msg":"Empty Cart","flag":"check-order"})
                else:
                    return jsonify({"result":False,"msg":log_invalid_audio_cmd,"flag":"search-error"})
            
            else:
                return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        except Exception as e:
            print(e)
            return jsonify({"result":False,"msg":"Something is wrong with the server","flag":"search-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"search-error"})


@app.route('/voicesearch/en', methods=["POST"])
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
            # audio_file = sf.read(file) 
            with audio_file as source:
                audio_data = recognizer.record(source)
            try:
                # y = (np.iinfo(np.int32).max * (audio_data/np.abs(audio_data).max())).astype(np.int32)
                # wavfile.write(wav_path, fs, y)
                # sf.read('msg0000 (2).WAV') 
                print(audio_data)
                line = recognizer.recognize_google(audio_data, language="en-US")
                line = line.lower()
                print(line)
            except Exception as e:
                return jsonify({"result":False,"msg":"Error \n %s" % (e),"flag":"file-error"})

            # translator = Translator()
            # text = translator.translate(line, dest="en").text
            item_det = line.split()
            item_name = item_det[0] 
            item_qty = item_det[1] 
            item_unit = item_det[2]
            item_cmd = item_det[3]
            # Banana 5 KG Delete
            if item_cmd == "add":
                return jsonify({"result":[{"name": item_name, "qty": item_qty, "unit": item_unit, "action": 1}],"msg":"sucess"})

            if item_cmd == "delete":
                return jsonify({"result":[{"name": item_name, "qty": item_qty, "unit": item_unit, "action": 0}],"msg":"sucess"})
            
            if item_cmd == "edit":
                return jsonify({"result":[{"name": item_name, "qty": item_qty, "unit": item_unit, "action": 2}],"msg":"sucess"})
            return jsonify({"result":item_det,"msg":"Wrong Action","flag":"Wrong Action"})
        else:
            return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
    else:
        return jsonify({"result":False,"msg":log_invalid_req_method,"flag":"navigation-error"})


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
            # audio_file = sf.read(file) 
            with audio_file as source:
                audio_data = recognizer.record(source)
            try:
                # y = (np.iinfo(np.int32).max * (audio_data/np.abs(audio_data).max())).astype(np.int32)
                # wavfile.write(wav_path, fs, y)
                # sf.read('msg0000 (2).WAV') 
                line = recognizer.recognize_google(audio_data, language="ta-LK")
                line = line.lower()
                print(line)
            except Exception as e:
                return jsonify({"result":False,"msg":"Error \n %s" % (e),"flag":"file-error"})

            translator = Translator()
            text = translator.translate(line, dest="en").text
            item_det = line.split()
            item_name = item_det[0] 
            item_qty = item_det[1] 
            item_unit = item_det[2]
            item_cmd = item_det[3]
            # Banana 5 KG Delete
            if item_cmd == "கூட்டு":
                return jsonify({"result":[{"name": item_name, "qty": item_qty, "unit": item_unit, "action": 1}],"msg":"sucess"})

            if item_cmd == "அழி" or item_cmd == "பள்ளி" or item_cmd == "வள்ளி":
                return jsonify({"result":[{"name": item_name, "qty": item_qty, "unit": item_unit, "action": 0}],"msg":"sucess"})
            
            if item_cmd == "மாற்ற" or item_cmd == "மாற்று":
                return jsonify({"result":[{"name": item_name, "qty": item_qty, "unit": item_unit, "action": 2}],"msg":"sucess"})
            return jsonify({"result":item_det,"msg":"Wrong Action","flag":"file-error"})
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
        try:
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
                
                try:
                    # line = recognizer.recognize_sphinx(audio_data, language="en-US")
                    line = recognizer.recognize_google(audio_data, language="en-IN")
                    print(line)
                except:
                    return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})

                if ("go back" in line):
                    return jsonify({"result":True,"msg":"You will be taken to the navigation","flag":"back"})
                elif("list coupons" in line):
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
                        couponIdFromCart = cart["_id"]
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
                                if(coupon["_id"] == userCoupon["_id"]):
                                    # print("coupon id: " + str(userCoupon["coupon_id"]) + " already used")
                                    adjustedCoupons1.remove(coupon)  

                    return jsonify({"result":True,"msg":log_available_list_coupons,"flag":"list-coupon-success","listCoupons":adjustedCoupons1})
                elif ("complete order" in line):
                    # complete order
                    orderId = request.form['orderId']
                    reviewReason = line.split("order")[1]

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
                    cancelReason = line.split("order")[1]

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
                    returnReason = line.split("order")[1]

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
                elif ("select coupon" in line):
                    # add coupon to cart
                    couponId = text2int(line.split(" ")[2])
                    userId = request.form['userId']
                    coupon = Coupon.objects(coupon_id=couponId).first()
                    try:
                        coupon1 = json.loads(Coupon.objects(coupon_id=6).first().to_json())
                        
                        cart = Cart.objects(user_id=userId).first()
                        if (cart is not None):
                            cart.update(coupon_id=coupon1["_id"], coupon_value=coupon1["coupon_value"])
                        else:
                            Cart(user_id=userId,coupon_id=coupon1["_id"],coupon_value=coupon1["coupon_value"])

                        return jsonify({"result":True,"msg":"Coupon with ID "+str(couponId)+" and Value "+ str(coupon1["coupon_value"])+" has been added to your cart!","flag":"coupon-success"})
                    except:
                        return jsonify({"result":True,"msg":"Coupon with ID "+str(couponId)+" not found!","flag":"coupon-error"})
                elif ("coupons" in line):
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
                elif ("select order" in line):
                    # Order
                    # orderId = text2int(line.split(" ")[2]) # Assuming Text will be like "order 123"
                    orderId = line.split(" ")[2]
                    order = Order.objects(order_id=orderId).first()
                    
                    if (order is not None):
                        return jsonify({"result":True, "msg":"The following is the order that you have selected","flag":"order-received","order":json.loads(order.to_json())})
                    else:
                        return jsonify({"result":False, "msg":"Order with provided ID not found","flag":"order-not-found","order":None})
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
                elif ("orders" in line):
                    return jsonify({"result":True,"msg":log_view_type_of_orders,"flag":"order-menu"})
                elif ("profile" in line):
                    # Get the Profile Details
                    return None
                else:
                    return jsonify({"result":False,"msg":"I do not understand that command","flag":"command-error"})
            else:
                return jsonify({"result":False,"msg":log_no_audio,"flag":"file-error"})
        except:
            return jsonify({"result":False,"msg":""})
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
            # line = recognizer.recognize_google(audio_data, key="AIzaSyAkni5khBB5CSXPnJNO6qAts3XQCc_eYY4", language="en-IN")
            line = recognizer.recognize_google(audio_data, language="en-IN")

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
    id= request.args.get('id')
    coupons = Coupon.objects().to_json()
    userCoupons = UserCoupon.objects(user_id=id).to_json
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
    item_price = request.form['item_price']
    item_unit = request.form['item_unit']
    item_offer_price = request.form['item_offer_price']

    new_item = Item(item_offer_price=item_offer_price, category_id=category_id, item_code=item_code, shop_id=shop_id, item_name=item_name, item_stock=item_stock, item_price=item_price, item_unit=item_unit).save()
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
    order_status = request.form['order_status']
    address = request.form['address']

    new_order = Order(shop_id=shop_id, user_id=user_id, coupon_id=coupon_id, coupon_value=coupon_value, order_status=order_status, address=address).save()
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
    item_price = request.form['item_price']
    item_offer_price = request.form['item_offer_price']
    item_qty = request.form['item_qty']

    new_cartitem = CartItem(cart_id=cart_id, item_id=item_id, item_name=item_name, item_code=item_code, item_price=item_price, item_offer_price=item_offer_price, item_qty=item_qty).save()
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
STORE LIST FOR FUTURE
------
"""
@app.route('/storeList', methods=['POST'])
def store_orderList():
    try:
        data = request.get_json()
        user_id = data.get('user_id', '')
        lang = data.get('lang', '')
        list = data.get('list', '')

        # transalate to english if list in tamil
        if lang == 'tm':
            translator = Translator()
            for item in list:
                item_name = translator.translate(item['item_name']).text
                item['item_name'] = item_name.lower()
            print(list)

        itemList = json.loads(Item.objects().to_json())
        print(itemList)
        array = []
        for i in list:
            print( i['item_name'], "i")
            for x in itemList:
                print(x['item_name'])
                if i['item_name'] == x['item_name']:
                    obj = {
                        "item_code": x['item_code'],
                        "item_qty": i['item_qty'],
                        "item_unit": i['item_unit'],
                        "item_name": i['item_name']
                    }
                    array.append(obj)

        print(array)
        storeList = StoreList( user_id=user_id, items=array )
        storeList.save()
        return jsonify({"result": True, "msg":"list stored for future"})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})


@app.route('/storeList', methods=['GET'])
def get_store_orderList():
    try:
        storeList_id= request.args.get('id')
        storeList = json.loads(StoreList.objects(storeList_id=storeList_id).first().to_json())
        if request.args.get('lang') == 'tm':
            translator = Translator()
            for x in storeList.get('items', ''):
                x['item_name'] = translator.translate(x['item_name'], dest="ta").text
            return jsonify({"result":True,"msg":log_success_retrieved_category,"data": storeList})
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": storeList})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})


@app.route('/storeList', methods=['DELETE'])
def delete_store_orderList():
    """Delete a orderitem given the ID of the usercoupon"""
    try:
        storeList_id= request.args.get('id')
        storeList = StoreList.objects(storeList_id=storeList_id).first()
        storeList.delete()
        return jsonify({"result":True,"msg":log_delete_category})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

"""
------
Predit item availability
------
"""
@app.route('/predictAvailability', methods=['POST'])
def predict_availability():
    try:
        data = request.get_json()
        print(data[1].get('items'))
        item_ids =data[1].get('items')
        lang = data[0].get('lang')
        shopList = json.loads(Shop.objects().to_json())
        itemList = json.loads(Item.objects().to_json())
        shopArray = []
        for x in shopList:
            items = []
            for y in itemList:
                if x['_id'] == y['shop_id']:
                    it = {
                        "id": y['_id'],
                        "shop_id": y['shop_id'],
                        "item_name": y["item_name"],
                        "item_stock": y["item_stock"],
                        "item_price": y["item_price"],
                        "item_offer_price": y["item_offer_price"],
                        "item_unit": y["item_unit"],
                        "available": False,
                        "category_id": y["category_id"]
                        # "pharmaceutical": y["pharmaceutical"],
                        # "prescription": y["prescription"]
                    }
                    items.append(it)
            obj = {
                'shopObj': x,
                "items": items
            }
            shopArray.append(obj)
        
        shopItems = []
        translator = Translator()
        for a in shopArray:
            itemNo = 0
            item = []
            # for z in a['items']:
            for b in item_ids:
                if [x for x in a['items'] if x['item_name'] == b['name']] and [x for x in a['items'] if b['quan'] <= x['item_stock']]:
                    itemNo = itemNo + 1
                    # z['available'] = True
                    # z['item_name'] = translator.translate(b['name'], dest=lang).text
                    print([x for x in a['items'] if x['item_name'] == b['name']])
                    obj ={  "name": translator.translate(b['name'], dest=lang).text, 
                            "quan": b['quan'],  
                            "available": True,
                            "item_price": [x for x in a['items'] if x['item_name'] == b['name']][0].get('item_price'),
                            "item_offer_price": [x for x in a['items'] if x['item_name'] == b['name']][0].get('item_offer_price')
                        }
                    item.append(obj)    
                else:
                    if [x for x in itemList if x['item_name'] == b['name']]:
                        categoryId = [x for x in itemList if x['item_name'] == b['name']][0].get('category_id')
                        print(categoryId)
                        nlist = [x for x in a['items'] if x['category_id'] == categoryId]
                        obj ={"name": translator.translate(b['name'], dest=lang).text,  "available": False, "similar-items": nlist}
                        item.append(obj)
                    else:
                        obj ={"name": translator.translate(b['name'], dest=lang).text, "available": False, "similar-items": nlist}
                        item.append(obj)
            # [x for x in myList if x.n == 30]
            prob = (itemNo/len(item_ids)) * 100
            objs = {
                'shopObj': a,
                'perc': prob,
                'items': item
            }
            shopItems.append(objs)   

        return jsonify({"result": True, "msg":"list stored for future","data":shopItems})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":data})

"""
------
User Profile edit
------
"""
@app.route('/profile/update', methods=['POST'])
def profile_update():
    try:
        data = request.get_json()
        print(request.data)
        id = data.get('id', '')
        name = data.get('user_name', '')
        email = data.get('user_email', '')
        adress = data.get('user_address', '')
        phone = data.get('user_phone', '')
        user = User.objects(user_id=id).first()
        user.user_name = name
        user.user_phone = phone
        user.user_email = email
        user.user_address = adress
        user.save()
        return jsonify({"result": True, "msg":"list stored for future","data":user})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":{}})

"""
------
Orders
-----
"""
@app.route('/orders/canceled', methods=['GET'])
def get_orders_canceled():
    try:
        orders = json.loads(Order.objects(order_status=2).to_json())
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": orders})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

@app.route('/orders/pending', methods=['GET'])
def get_orders_pending():
    try:
        orders = json.loads(Order.objects(order_status=0).to_json())
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": orders})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

@app.route('/orders/completed', methods=['GET'])
def get_orders_completed():
    try:
        orders = json.loads(Order.objects(order_status=1).to_json())
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": orders})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

@app.route('/order', methods=['GET'])
def get_orderbyId():
    try:
        id= request.args.get('id')
        order = json.loads(Order.objects(order_id=id).to_json())
        orderItems = json.loads(OrderItem.objects(order_id=id).to_json())
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": order, "items": orderItems})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

@app.route('/order/canceled', methods=['POST'])
def submit_orders_canceled():
    try:
        data = request.get_json()
        print(data)
        id = data.get('id', '')
        feedback = data.get('feedback', '')
        order = Order.objects(order_id=id).first()
        order.order_status = 2
        order.cancel_reason = feedback
        order.save()
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": order})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

@app.route('/order/return', methods=['POST'])
def submit_orders_retrn():
    try:
        data = request.get_json()
        print(data)
        id = data.get('id', '')
        feedback = data.get('feedback', '')
        order = Order.objects(order_id=id).first()
        order.order_status = 0
        order.return_reason = feedback
        order.save()
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": order})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

@app.route('/order/complete', methods=['POST'])
def submit_orders_complete():
    try:
        data = request.get_json()
        print(data)
        id = data.get('id', '')
        feedback = data.get('feedback', '')
        order = Order.objects(order_id=id).first()
        order.order_status = 1
        order.review_reason = feedback
        order.save()
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": order})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})


@app.route('/order/details', methods=['GET'])
def get_orderDetailsbyId():
    try:
        userId= request.args.get('userId')
        lang = request.args.get('lang')
        order = json.loads(Order.objects(user_id=userId).to_json())
        orderItems = json.loads(OrderItem.objects().to_json())
        itemList = json.loads(Item.objects().to_json())
        shopList = json.loads(Shop.objects().to_json())
        couponList = json.loads(Coupon.objects().to_json())
        orders =[]
        # print(orderItems)
        translator = Translator()
        for x in order:
            item = [] 
            for y in orderItems:
                if x['_id'] == y['order_id']:
                    y['item_name'] = translator.translate(y['item_name'], dest=lang).text
                    item.append(y)
            obj = {
                "orderId": x['_id'], "shopId": x['shop_id'], "shopName": [y for y in shopList if y['_id'] ==  x['shop_id']][0].get("shop_name"), "status": x["order_status"], 
                "payment": x["order_payment"], "couponId": x["coupon_id"], "items": item
            }
            orders.append(obj)
        return jsonify({"result":True,"msg":log_success_retrieved_category, "data": orders})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

"""
------
Coupouns
------
"""

@app.route('/get_coupons', methods=['GET'])
def get_coupons():
    try:
        data = request.get_json()
        id = data.get('id', '')
        coupons = json.loads(Coupon.objects().to_json())
        userCoupons = json.loads(UserCoupon.objects(user_id=id).to_json())
        otherCoupons = []
        for x in coupons:
            for y in userCoupons:
                if x['id'] != y['coupon_id']:
                    otherCoupons.append(x)

        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": otherCoupons})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

@app.route('/add_coupon', methods=['POST'])
def add_coupon_to_cart():
    try:
        data = request.get_json()
        id = data.get('id', '')
        coupon = json.loads(Coupon.objects(coupon_id=id).to_json())
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": coupon})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

"""
------
Coupouns
------
"""

@app.route('/get_offers', methods=['GET'])
def get_offers():
    try:
        id= request.args.get('id')
        lang = request.args.get('lang')
        print(id, lang)
        userobj = json.loads(User.objects(user_id=id).to_json())
        print(userobj[0])
        latitude = userobj[0].get('user_lat')
        longitude = userobj[0].get('user_long')
        print(latitude, longitude)
        storeList = json.loads(Shop.objects().to_json())
        array = []
        print(storeList, 'storelisr')
        for i in storeList:
            print(i)
            coords_1 = (latitude, longitude)
            coords_2 = (i['shop_lat'], i['shop_long'])
            dist = geopy.distance.geodesic(coords_1, coords_2).km
            print(dist)
            if (dist < 5):
                array.append(i)
        # shopList = json.loads(Shop.objects().to_json())
        itemList = json.loads(Item.objects().to_json())
        shopArray = []
        print(array)
        for x in array:
            print(x)
            obj = {
                'shopObj': x,
                "items": []
            }
            items = []
            for y in itemList:
                if x['_id'] == y['shop_id']:
                    if y['item_offer_price'] !=0:
                        items.append(y)
            obj = {
                'shopObj': x,
                "items": items
            }
            shopArray.append(obj)

        outputArray = []
        translator = Translator()
        for z in shopArray:
            if len(z['items']) > 0:
                item = []
                for y in z['items']:
                    item.append({ "name": translator.translate(y['item_name'], dest=lang).text, "price": y['item_price'],  "item_offer_price": y['item_offer_price']})
                onb = {
                    "item": item,
                     "shop": z['shopObj']
                }
                outputArray.append(onb)
                
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": outputArray})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})


"""
------
Near by shop
------
"""
@app.route('/get_nearbyshops', methods=['GET'])
def get_shops():
    try:
        address= request.args.get('address')
        print(address)
        URL = "https://maps.googleapis.com/maps/api/geocode/json"
        if (address != ""):
            location_detail = {'address':address, 'key': 'AIzaSyCT0BPMCFabWU1OIKiHxhe5kB5dDJfbdO0'}
            r = requests.get(url = URL, params = location_detail)
            data = r.json()
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            print(latitude, longitude)
            storeList = json.loads(Shop.objects().to_json())
            array = []
            print(storeList, 'storelisr')
            for i in storeList:
                print(i)
                coords_1 = (latitude, longitude)
                coords_2 = (i['shop_lat'], i['shop_long'])
                dist = geopy.distance.geodesic(coords_1, coords_2).km
                print(dist)
                if (dist < 5):
                    array.append(i)
        else:
            return jsonify({"result":False,"msg":"No Adress Input"})
        return jsonify({"result":True,"msg":log_success_retrieved_category,"data": array})
    except Exception as e:
        return jsonify({"result":False,"msg":"Error \n %s" % (e),"data":None})

"""
------
Coupouns
------
"""

@app.route('/checkout-final',methods=['POST'])
def checkout():
    return "true"


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


class JsonSerializable(object):
    def toJson(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()
class FileItem(JsonSerializable):
    def __init__(self, fname):
        self.fname = fname
