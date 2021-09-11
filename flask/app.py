from routes import *
# from db import *
from flask_mongoengine import MongoEngine

db = MongoEngine()

# This would usually come from your config file
DB_URI = "mongodb+srv://root:root@cluster0.vxgus.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

app.config["MONGODB_HOST"] = DB_URI
app.config['MONGODB_SETTINGS'] = {
    'alias': 'default',
    'db': 'myFirstDatabase',
    'host': 'mongodb+srv://root:root@cluster0.vxgus.mongodb.net',
    'port': 27017
}

# app.config['MONGODB_SETTINGS'] = {'default':{'NAME':'myFirstDatabase'}, 'alias':'default'}

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)