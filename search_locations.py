import os
from openai import OpenAI
from datetime import datetime
import json

class LocationSuggester:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def suggest_locations(self, form_data):
        """
        Analyze trip details and suggest locations using OpenAI
        
        Args:
            form_data: Dictionary containing trip details
            
        Returns:
            Dictionary containing suggested locations and details
        """
        # Prepare the prompt for OpenAI
        prompt = self._create_prompt(form_data)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a travel planning expert. Analyze the trip details and suggest 
                    suitable locations. Consider the following:
                    1. Current location and preferred type of trip
                    2. Number of days and people
                    3. Budget constraints
                    4. Season and weather conditions
                    5. Accessibility and travel time
                    
                    Format your response as a JSON object with the following structure:
                    {
                        "suggestions": [
                            {
                                "location": "Location name",
                                "description": "Brief description of why this location is suitable",
                                "travel_time": "Estimated travel time from current location",
                                "best_season": "Best time to visit",
                                "estimated_cost": "Estimated cost per person",
                                "highlights": ["Highlight 1", "Highlight 2", "Highlight 3"]
                            }
                        ],
                        "summary": "Overall summary of suggestions"
                    }"""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse the response
            suggestions = json.loads(response.choices[0].message.content)
            return suggestions
            
        except Exception as e:
            print(f"Error getting suggestions: {e}")
            return {"error": str(e)}
    
    def _create_prompt(self, form_data):
        """Create a detailed prompt from form data"""
        prompt = f"""Please suggest travel locations based on the following details:
        
        Trip Duration: """
        
        if form_data['tripType'] == 'days':
            prompt += f"{form_data['numberOfDays']} days"
        else:
            start_date = datetime.strptime(form_data['startDate'], '%Y-%m-%d')
            end_date = datetime.strptime(form_data['endDate'], '%Y-%m-%d')
            duration = (end_date - start_date).days
            prompt += f"{duration} days from {form_data['startDate']} to {form_data['endDate']}"
            
        prompt += f"""
        Number of People: {form_data['numberOfPeople']}
        Trip Description: {form_data['tripDescription']}
        
        Please suggest suitable locations considering the above details. Focus on locations that would be appropriate for the given duration and group size."""
        
        return prompt

# Example usage
if __name__ == "__main__":
    # Test the suggester
    suggester = LocationSuggester()
    test_data = {
        "tripType": "days",
        "numberOfDays": "3",
        "numberOfPeople": "4",
        "tripDescription": "I am currently in Bengaluru, Karnataka and I want to go to a beach for the weekend."
    }
    suggestions = suggester.suggest_locations(test_data)
    print(json.dumps(suggestions, indent=2))
