from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# import the scraper module
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Setup route
@app.route("/")
def index():
    
    # find one document from our mongo db and return it.
    mars_info = mongo.db.mars_info.find_one()
    
    # pass that mars_info to render_template 
    return render_template("index.html", mars_info=mars_info)

# set our path to /scrape
@app.route("/scrape")
def scraper():
    # create a mars_info database
    mars_info = mongo.db.mars_info 
    
    # call the scrape function in scrape_mars file. This will scrape and save to mongo.
    mars_info_data = scrape_mars.scrape()
    
    # update mars_info with the data that is being scraped.
    mars_info.update_many({}, {"$set": mars_info_data}, upsert=True)
    
    # return a message to the page that it was successful.
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
#=====================================================================================================
