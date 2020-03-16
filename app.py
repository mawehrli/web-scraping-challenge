# Import necessary libraries
# Reference 12.3 exercises 7 - 10
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask
app = Flask(__name__)

# Establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define mars_db
mars_db = mongo.db.mars

# Drop existing data
mars_db.drop()

# Route to render index.html template using data from Mongo
@app.route('/')
def index():
    # Find record from the mongo database
    destination_data = mars_db.find_one()

    # Return template and Mars data
    return render_template("index.html", mars=destination_data)

# Create route for scrape function
@app.route('/scrape')
def scrape():

    # Run the scrape function
    mars = scrape_mars.scrape()

    # Insert data into Mars database
    mars_db.insert_one(mars)

    # Redirect to home page
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
