from flask import request, render_template, make_responsem jsonify
from datetime import datetime as dt
from flask import current_app as app
from models import db
from models.cart import Cart
from models.user import User
from models.shop import Shop
from models.coupon import Coupon
from models.list import List
from models.item import Item
from models.corder import Corder

import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO

"""
-----
OCR
-----
Convert an Image to text that we need to show in the UI
"""
@app.route('/predict', methods=['GET'])
def predict_ocr():
    """Generate Text which is in the image"""
    image_url = request.args.post('image_url')
    image = _get_image(image_url)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)

def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))

"""
------
SHOP
------
"""
@app.route('/shops', methods=['GET'])
def get_all_shops():
    """Retrieve all shops from our database."""
    shops = Shop.query.all()

@app.route('/shop/<int:shop_id>', methods=['GET'])
def get_shop(shop_id):
    """Retrieve the Shop with the Given Shop ID"""
    shop = Shop.query.get_or_404(shop_id)

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

@app.route('/shop/<int:shop_id>',methods=['DELETE'])
def delete_shop(shop_id):
    """Delete a Shop given the ID of the Shop"""
    shop = Shop.query.get_or_404(shop_id)
    db.session.delete(shop)
    db.session.commit()

"""
------
USER
------
"""
@app.route('/users', methods=['GET'])
def get_all_users():
    """Retrieve all Users from our database."""
    users = User.query.all()

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve the User with the Given User ID"""
    user = User.query.get_or_404(user_id)

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

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a User given the ID of the User"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

"""
--------
COUPON
--------
"""
@app.route('/coupons', methods=['GET'])
def get_all_coupons():
    """Retrieve all Coupons from our database."""
    coupons = Coupon.query.all()

@app.route('/coupon/<int:coupon_id>',methods=['GET'])
def get_coupon(coupon_id):
    """Retrieve a Coupon given the ID of the Coupon"""
    coupon = Coupon.query.get_or_404(coupon_id)

@app.route('/coupon',methods=['POST'])
def new_coupon():
    """Add New Coupon to Our Database."""
    shop_id = request.args.post('shop_id')
    coupon_value = request.args.post('coupon_value')

    new_coupon = Coupon(shop_id=shop_id, coupon_value=coupon_value)
    db.session.add(new_coupon)
    db.session.commit()

@app.route('/coupon/<int:coupon_id>', methods=['DELETE'])
def delete_coupon(coupon_id):
    """Delete a Coupon given the ID of the Coupon"""
    coupon = Coupon.query.get_or_404(coupon_id)
    db.session.delete(coupon)
    db.session.commit()

"""
-------
ITEM
-------
"""
@app.route('/items', methods=['GET'])
def get_all_items():
    """Retrieve all items from our database."""
    items = Item.query.all()

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieve an item given the ID of the Item"""
    item = Item.query.get_or_404(item_id)

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

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item given the ID of the Item"""
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()