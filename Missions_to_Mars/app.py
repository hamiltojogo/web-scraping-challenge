from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()

    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():

    #run scrape function
    mars_facts = scarpe_mars.scrape()

    #update database
    mongo.db.collection.update({}, mars_facts, upsert=True)

    #back to home page
    return redirect('/')





if __name__ == "__main__":
    app.run(debug=True)

