from flask import request, render_template, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
from models.cart import Cart
from models.user import User
from models.shop import Shop
from models.coupon import Coupon
from models.list import List
from models.item import Item
from models.corder import Corder

import pytesseract
import requests, os, sys
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO

# You have 50 free calls per day, after that you have to register somewhere
# around here probably https://cloud.google.com/speech-to-text/
GOOGLE_SPEECH_API_KEY = 'AIzaSyADxOB7Npq1-Q5cj5A2Zm-oKRIrzjnIbe0'

# NanoNets Model Details
model_id = os.environ.get('NANONETS_MODEL_ID')
api_key = os.environ.get('NANONETS_API_KEY')

"""
-----
OCR
-----
Convert an Image to text that we need to show in the UI
"""
@app.route('/predict', methods=['GET'])
def predict_ocr():
    """Generate Text which is in the image"""
    # image_url = request.args.post('image_url')
    # image = _get_image(image_url)
    # image.filter(ImageFilter.SHARPEN)
    # return pytesseract.image_to_string(image)
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
            extra_line = f'Your text: "{text}"'

            # Saving the file.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            return jsonify({"result":True,"msg":"Successfully Converted Speech to Text","command":extra_line})
    else:
        return jsonify({"result":False,"msg":"Invalid Method"})

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