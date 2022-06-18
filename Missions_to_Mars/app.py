# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_DB")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    all_scraped_info = mongo.db.all_scraped_info.find_one()
    return render_template("index.html", all_scraped_info=all_scraped_info)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    all_scraped_info = scrape_mars.scrape_info()
   
   # Insert the record
    mongo.db.all_scraped_info.update_one({}, {"$set": all_scraped_info}, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)