from flask import Flask, request, jsonify, render_template
from search_locations import LocationSuggester
from openai_integration import generate_itinerary
from hotel_booking import HotelSearcher
import os
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
suggester = LocationSuggester()
hotel_searcher = HotelSearcher()

@app.route('/')
def index():
    return render_template('main_display.html')

@app.route('/api/suggest-locations', methods=['POST'])
def suggest_locations():
    try:
        form_data = request.json
        suggestions = suggester.suggest_locations(form_data)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/itinerary')
def itinerary():
    return render_template('itinerary.html')

@app.route('/api/generate-itinerary', methods=['POST'])
def generate_itinerary_endpoint():
    try:
        trip_data = request.json
        logger.info("Received trip data in API endpoint: %s", trip_data)
        result = generate_itinerary(trip_data)
        logger.info("Generated itinerary result: %s", result)
        return jsonify(result)
    except Exception as e:
        logger.error("Error in generate_itinerary_endpoint: %s", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')

@app.route('/api/search-hotels', methods=['POST'])
def search_hotels():
    try:
        data = request.json
        locations = data.get('locations', [])
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        budget = data.get('budget', 5000)  # Default budget of 5000 INR
        
        results = {}
        for location in locations:
            hotel_results = hotel_searcher.search_hotels(
                location=location,
                check_in=check_in,
                check_out=check_out,
                budget_max=budget
            )
            results[location] = hotel_results
        
        return jsonify({
            "status": "success",
            "results": results
        })
    except Exception as e:
        logger.error("Error searching hotels: %s", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 