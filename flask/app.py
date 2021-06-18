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

from routes import *

if __name__ == "__main__":
    app.run(debug=True)