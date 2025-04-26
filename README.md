# Travel PA (Personal Assistant)
Here is your own travel assistant which assists you in the following way: 
1. Searches and shortlists locations that can be good for you based on your preferences (trip description, number of people and other input)
2. Based on your selection from the provided shortlist, creates a detailed itinerary for each destination selected based on your preferences.
3. Searches for hotels (from Booking.com) and shows the available hotels based on our criteria including rating>7.5 and your criteria such as max budget limit.
4. The hotel searches redirect you to Booking.com page and the detailed itinerary can be downloaded as a PDF for future reference. 

Current functionality does not include hotel search and PDF itinerary download. 

GPT3.5-turbo is used to search for locations and to generate itinerary. 
I will soon add further details about installation and setup. 

Here are some details about Hotel Availability Checker

This Python script helps you search for hotel availability and prices across multiple booking platforms including RateHawk, Booking.com, and Expedia. It allows you to find hotels within your budget and compare prices across different platforms.

## Setup

1. Install Python 3.7 or higher if you haven't already
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Sign up for API keys from the following platforms:
   - RateHawk: https://ratehawk.com/
   - Booking.com: https://www.booking.com/affiliate-program/v2/index.html
   - Expedia: https://www.expedia.com/partner/

4. Update the API keys in `hotel_booking.py`:
   ```python
   self.ratehawk_api_key = "YOUR_RATEHAWK_API_KEY"
   self.booking_api_key = "YOUR_BOOKING_API_KEY" 
   self.expedia_api_key = "YOUR_EXPEDIA_API_KEY"
   ```

## Usage

```python
from hotel_booking import HotelSearcher

# Create a searcher instance
searcher = HotelSearcher()

# Search for hotels
results = searcher.search_hotels(
    location="Mumbai",  # City name
    check_in="2024-04-20",  # Check-in date (YYYY-MM-DD)
    check_out="2024-04-25",  # Check-out date (YYYY-MM-DD)
    budget_max=5000.0,  # Maximum price per night
    currency="INR"  # Currency code (default: INR)
)

# Print results
for hotel in results:
    print(f"\nHotel: {hotel['name']}")
    print(f"Price: {hotel['currency']} {hotel['price']}")
    print(f"Platform: {hotel['platform']}")
    print(f"Rating: {hotel['rating']}")
    print(f"Address: {hotel['address']}")
    print(f"Available Rooms: {hotel['available_rooms']}")
```

## Features

- Search across multiple booking platforms simultaneously
- Filter by location, dates, and maximum budget
- Compare prices in your preferred currency
- Get detailed hotel information including ratings and available rooms
- Results are sorted by price for easy comparison

## Note

You'll need to obtain API keys from each platform and may need to comply with their terms of service and usage limits. Some platforms may require business verification or paid subscriptions to access their APIs.

## Support

For any issues or questions, please open an issue on GitHub or contact the maintainers. 