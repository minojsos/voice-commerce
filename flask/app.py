from routes import *
from db import *

# This would usually come from your config file
DB_URI = "mongodb+srv://root:root@cluster0.vxgus.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

app.config["MONGODB_HOST"] = DB_URI

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)