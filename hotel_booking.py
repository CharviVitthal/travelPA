import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class HotelSearcher:
    def __init__(self):
        # Initialize API keys - you'll need to replace these with your actual API keys
        self.ratehawk_api_key = "YOUR_RATEHAWK_API_KEY"
        self.booking_api_key = "YOUR_BOOKING_API_KEY"
        self.expedia_api_key = "YOUR_EXPEDIA_API_KEY"

    def search_hotels(self, 
                     location: str,
                     check_in: str,
                     check_out: str,
                     budget_max: float,
                     currency: str = "INR") -> List[Dict]:
        """
        Search for hotels across multiple platforms
        
        Args:
            location: City or area name
            check_in: Check-in date in YYYY-MM-DD format
            check_out: Check-out date in YYYY-MM-DD format
            budget_max: Maximum price per night
            currency: Currency code (default INR)
            
        Returns:
            List of hotel options matching the criteria
        """
        results = []
        
        # Search across different platforms
        ratehawk_results = self._search_ratehawk(location, check_in, check_out, budget_max, currency)
        booking_results = self._search_booking(location, check_in, check_out, budget_max, currency)
        expedia_results = self._search_expedia(location, check_in, check_out, budget_max, currency)
        
        # Combine and sort results
        results.extend(ratehawk_results)
        results.extend(booking_results)
        results.extend(expedia_results)
        
        # Sort by price
        results.sort(key=lambda x: x['price'])
        
        return results

    def _search_ratehawk(self, location: str, check_in: str, check_out: str, 
                        budget_max: float, currency: str) -> List[Dict]:
        """Search hotels on RateHawk"""
        try:
            # RateHawk API endpoint
            url = "https://api.ratehawk.com/api/v1/hotels/search"
            
            headers = {
                "Authorization": f"Bearer {self.ratehawk_api_key}",
                "Content-Type": "application/json"
            }
            
            params = {
                "query": location,
                "check_in": check_in,
                "check_out": check_out,
                "currency": currency,
                "price_max": budget_max
            }
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return self._format_ratehawk_results(data)
            return []
            
        except Exception as e:
            print(f"Error searching RateHawk: {e}")
            return []

    def _search_booking(self, location: str, check_in: str, check_out: str,
                       budget_max: float, currency: str) -> List[Dict]:
        """Search hotels on Booking.com"""
        try:
            # Booking.com API endpoint
            url = "https://distribution-xml.booking.com/json/bookings"
            
            headers = {
                "Authorization": f"Basic {self.booking_api_key}",
                "Content-Type": "application/json"
            }
            
            params = {
                "city": location,
                "arrival_date": check_in,
                "departure_date": check_out,
                "currency": currency,
                "max_rate": budget_max
            }
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return self._format_booking_results(data)
            return []
            
        except Exception as e:
            print(f"Error searching Booking.com: {e}")
            return []

    def _search_expedia(self, location: str, check_in: str, check_out: str,
                       budget_max: float, currency: str) -> List[Dict]:
        """Search hotels on Expedia"""
        try:
            # Expedia API endpoint
            url = "https://api.ean.com/v3/properties/search"
            
            headers = {
                "Authorization": f"Bearer {self.expedia_api_key}",
                "Content-Type": "application/json"
            }
            
            params = {
                "location": location,
                "checkIn": check_in,
                "checkOut": check_out,
                "currency": currency,
                "maxPrice": budget_max
            }
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return self._format_expedia_results(data)
            return []
            
        except Exception as e:
            print(f"Error searching Expedia: {e}")
            return []

    def _format_ratehawk_results(self, data: Dict) -> List[Dict]:
        """Format RateHawk results into standard format"""
        formatted_results = []
        for hotel in data.get('hotels', []):
            formatted_results.append({
                'name': hotel.get('name'),
                'price': hotel.get('price'),
                'currency': hotel.get('currency'),
                'platform': 'RateHawk',
                'rating': hotel.get('rating'),
                'address': hotel.get('address'),
                'available_rooms': hotel.get('available_rooms', 0)
            })
        return formatted_results

    def _format_booking_results(self, data: Dict) -> List[Dict]:
        """Format Booking.com results into standard format"""
        formatted_results = []
        for hotel in data.get('hotels', []):
            formatted_results.append({
                'name': hotel.get('name'),
                'price': hotel.get('price'),
                'currency': hotel.get('currency'),
                'platform': 'Booking.com',
                'rating': hotel.get('rating'),
                'address': hotel.get('address'),
                'available_rooms': hotel.get('available_rooms', 0)
            })
        return formatted_results

    def _format_expedia_results(self, data: Dict) -> List[Dict]:
        """Format Expedia results into standard format"""
        formatted_results = []
        for hotel in data.get('hotels', []):
            formatted_results.append({
                'name': hotel.get('name'),
                'price': hotel.get('price'),
                'currency': hotel.get('currency'),
                'platform': 'Expedia',
                'rating': hotel.get('rating'),
                'address': hotel.get('address'),
                'available_rooms': hotel.get('available_rooms', 0)
            })
        return formatted_results

# Example usage
if __name__ == "__main__":
    searcher = HotelSearcher()
    
    # Example search parameters
    results = searcher.search_hotels(
        location="Mumbai",
        check_in="2024-04-20",
        check_out="2024-04-25",
        budget_max=5000.0  # Maximum price per night in INR
    )
    
    # Print results
    print(f"Found {len(results)} hotels matching your criteria:")
    for hotel in results:
        print(f"\nHotel: {hotel['name']}")
        print(f"Price: {hotel['currency']} {hotel['price']}")
        print(f"Platform: {hotel['platform']}")
        print(f"Rating: {hotel['rating']}")
        print(f"Address: {hotel['address']}")
        print(f"Available Rooms: {hotel['available_rooms']}")
