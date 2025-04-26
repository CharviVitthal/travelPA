import os
from openai import OpenAI
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_itinerary(trip_data):
    """
    Generate detailed travel itineraries for each selected destination.
    
    Args:
        trip_data (dict): Contains trip details including:
            - startDate: Start date of the trip
            - endDate: End date of the trip
            - preferences: Additional preferences
            - selectedDestinations: List of selected destinations with their details
    
    Returns:
        dict: Generated itineraries with day-by-day breakdown for each destination
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Calculate number of days
    start_date = datetime.strptime(trip_data['startDate'], '%Y-%m-%d')
    end_date = datetime.strptime(trip_data['endDate'], '%Y-%m-%d')
    num_days = (end_date - start_date).days + 1
    
    # Generate itinerary for each destination
    itineraries = {}
    
    for destination in trip_data['selectedDestinations']:
        location = destination['location']
        highlights = destination['highlights']
        
        # Create the prompt for this destination
        prompt = f"""Create a detailed travel itinerary for a {num_days}-day trip to {location}.
        
        Trip Details:
        - Start Date: {trip_data['startDate']}
        - End Date: {trip_data['endDate']}
        - Additional Preferences: {trip_data['preferences']}
        - Destination Highlights: {highlights}
        
        Please provide a day-by-day breakdown including:
        1. Morning activities
        2. Afternoon activities
        3. Evening activities
        4. Recommended restaurants
        5. Transportation details
        6. Estimated costs for each day
        7. Any special considerations based on the preferences
        
        Format the response in a structured way that can be easily displayed on a webpage."""
        
        logger.info(f"Generating itinerary for {location}")
        logger.info(f"Prompt: {prompt}")
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional travel planner. Create detailed, practical, and engaging travel itineraries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            itineraries[location] = response.choices[0].message.content
            logger.info(f"Generated itinerary for {location}")
            
        except Exception as e:
            logger.error(f"Error generating itinerary for {location}: {str(e)}")
            itineraries[location] = f"Error generating itinerary: {str(e)}"
    
    return {
        "status": "success",
        "itineraries": itineraries
    } 