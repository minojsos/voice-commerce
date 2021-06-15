from flask import request, make_response, jsonify
from datetime import datetime as dt
from app import app
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

import requests, os, sys
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO

import json
import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from gtts import gTTS
import os
warnings.filterwarnings('ignore')

import speech_recognition as sr

import nltk
from nltk.stem import WordNetLemmatizer
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
            line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")

            if (flag == "name"):
                # This is the Name of the user
                return jsonify({"result":True,"msg":"","flag":"register-process","data":line})
            elif (flag == "email"):
                # This is the Email of the user
                return jsonify({"result":True,"msg":"","flag":"register-process","data":line})
            elif (flag == "phone"):
                # This is the Phone Number of the user
                return jsonify({"result":True,"msg":"","flag":"register-process","data":line})
            elif (flag == "address"):
                # This is the Address of the user
                return jsonify({"result":True,"msg":"","flag":"register-process","data":line})
            elif (flag == "save"):
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
            line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")
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
            line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")

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
            line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")

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
            line = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US")

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
                        cartitem = CartItem(cart_id=cart["cart_id"],item_id=item_jsn["item_id"])
                        if (cartitem is None):
                            # If Item is not in 
                            if (item_jsn["item_stock"] >= item_qty):
                                # Stock Available
                                # Add to Cart and Send Response Back to User
                                return jsonify({"result":True,"msg":"Item with name " + item_name + " and Quantity " + item_qty + " has been successfully added to your Cart!","flag":"search-success"})
                            else:
                                return jsonify({"result":False,"msg":"Item with name " + item_name + " has only " + str(item_jsn["item_stock"]) + " " + item_jsn["item_unit"] + "!","flag":"search-error"})
                        else:

                    else:
                        return jsonify({"result":False,"msg":"Invalid User ID","flag","search-error"})
                else:
                    return jsonify({"result":False, "msg":"Item with name " + item_name + " not found!","flag":"search-error"})
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
-----
Speech to Text - English
-----
Convert Speech to Text using Google Speech to Text
"""
@app.route('/speech/en', methods=["GET", "POST"])
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
            text = recognizer.recognize_google(
                audio_data, key=GOOGLE_SPEECH_API_KEY, language="en-US"
            )
            extra_line = text # Save the Txt in Extra Line

            # Saving the file.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Check what the command is
            if "create" in extra_line and "list" in extra_line:
                return jsonify({"result":True,"msg":"You can now create a list!","flag":"create-list"})
            elif ""
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
def get_all_shops():
    """Retrieve all shops from our database."""
    shops = Shop.query.all()

    return jsonify({"result":True,"msg":"Successfully Retrieved All Shops","data":shops})

@app.route('/shop/<int:shop_id>', methods=['GET'])
def get_shop(shop_id):
    """Retrieve the Shop with the Given Shop ID"""
    shop = Shop.query.get_or_404(shop_id)
    
    return jsonify({"result":True,"msg":"Successfully Retrieved Shop with Given ID","data":shop})

@app.route('/shop', methods=['POST'])
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
    new_shop = Shop(shop_name=shop_name, shop_phone=shop_phone, shop_address=shop_addr, shop_email=shop_email, shop_lat=shop_lat, shop_long=shop_long, shop_available=shop_available)
    db.session.add(new_shop)  # Adds new Shop record to database
    db.session.commit()  # Commits all changes

    return jsonify({"result":True,"msg":"Successfully Created New Shop"})

@app.route('/shop/<int:shop_id>',methods=['DELETE'])
def delete_shop(shop_id):
    """Delete a Shop given the ID of the Shop"""
    shop = Shop.query.get_or_404(shop_id)
    db.session.delete(shop)
    db.session.commit()

    return jsonify({"result":True,"msg":"Successfully Deleted Shop with the Given ID"})

"""
------
USER
------
"""
@app.route('/users', methods=['GET'])
def get_all_users():
    """Retrieve all Users from our database."""
    users = User.query.all()
    return jsonify({"result":True,"msg":"Successfully Retrieved All Users","data":users})

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve the User with the Given User ID"""
    user = User.query.get_or_404(user_id)
    return jsonify({"result":True,"msg":"Successfully Retrieved User with Given ID","data":user})

@app.route('/user', methods=['POST'])
def new_user():
    """ Add New User to our Database."""
    user_name = request.args.post('user_name')
    user_phone = request.args.post('user_phone')
    user_email = request.args.post('user_email')
    user_password = request.args.post('user_password')
    user_address = request.args.post('user_address')

    """Create a user via query string parameters."""
    new_user = User(user_name=user_name, user_phone=user_phone, user_email=user_email, user_password=user_password, user_address=user_address)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"result":True,"msg":"Successfully Created New User"})

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a User given the ID of the User"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"result":True,"msg":"Successfully Deleted User with the Given ID"})

"""
--------
COUPON
--------
"""
@app.route('/coupons', methods=['GET'])
def get_all_coupons():
    """Retrieve all Coupons from our database."""
    coupons = Coupon.query.all()
    return jsonify({"result":True,"msg":"Successfully Retrieved All Coupons","data":coupons})

@app.route('/coupon/<int:coupon_id>',methods=['GET'])
def get_coupon(coupon_id):
    """Retrieve a Coupon given the ID of the Coupon"""
    coupon = Coupon.query.get_or_404(coupon_id)
    return jsonify({"result":True,"msg":"Successfully Retrieved Coupon with Given ID","data":coupon})

@app.route('/coupon',methods=['POST'])
def new_coupon():
    """Add New Coupon to Our Database."""
    shop_id = request.args.post('shop_id')
    coupon_value = request.args.post('coupon_value')

    new_coupon = Coupon(shop_id=shop_id, coupon_value=coupon_value)
    db.session.add(new_coupon)
    db.session.commit()
    return jsonify({"result":True,"msg":"Successfully Created New Coupon"})

@app.route('/coupon/<int:coupon_id>', methods=['DELETE'])
def delete_coupon(coupon_id):
    """Delete a Coupon given the ID of the Coupon"""
    coupon = Coupon.query.get_or_404(coupon_id)
    db.session.delete(coupon)
    db.session.commit()
    return jsonify({"result":True,"msg":"Successfully Deleted Coupon with the Given ID"})

"""
-------
ITEM
-------
"""
@app.route('/items', methods=['GET'])
def get_all_items():
    """Retrieve all items from our database."""
    items = Item.query.all()
    return jsonify({"result":True,"msg":"Successfully Retrieved All Items","data":items})

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieve an item given the ID of the Item"""
    item = Item.query.get_or_404(item_id)
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

    new_item = Item(item_code=item_code, shop_id=shop_id, item_name=item_name, item_stock=item_stock, item_rate=item_rate, item_unit=item_unit)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"result":True,"msg":"Successfully Created New Item"})

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item given the ID of the Item"""
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"result":True,"msg":"Successfully Deleted Item with the Given ID"})

if __name__ == "__main__":
    app.run(debug=True, threaded=True)