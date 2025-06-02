import os
from datetime import datetime, timedelta
import pandas as pd
from stravalib import Client
from dotenv import load_dotenv

def calculate_pace(time_in_seconds, distance_miles):
    if distance_miles == 0 or time_in_seconds == 0:
        return "0:00"
    
    minutes_per_mile = (time_in_seconds / 60) / distance_miles
    minutes = int(minutes_per_mile)
    seconds = int((minutes_per_mile - minutes) * 60)
    return f"{minutes}:{seconds:02d}"

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours}:{minutes:02d}:{secs:02d}"

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize Strava client
    client = Client()
    
    # Get refresh token from environment
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    
    # Refresh access token
    token_response = client.refresh_access_token(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )
    
    # Update access token
    client.access_token = token_response['access_token']
    
    # Get all activities
    activities = []
    for activity in client.get_activities():
        # Extract relevant data
        date = activity.start_date_local.strftime('%Y-%m-%d')
        activity_type = activity.type
        
        # Get distance in miles
        distance_miles = float(activity.distance.num) * 0.000621371 if activity.distance else 0
        
        # Get time in seconds
        time_seconds = activity.moving_time.total_seconds() if activity.moving_time else 0
        time = format_time(int(time_seconds))
        
        # Calculate pace based on total time and distance
        pace = calculate_pace(time_seconds, distance_miles) if distance_miles > 0 else "N/A"
        
        # Get heart rate if available
        heart_rate = activity.average_heartrate if activity.average_heartrate else "N/A"
        
        activities.append({
            'Date': date,
            'Activity': activity_type,
            'Distance (miles)': round(distance_miles, 2),
            'Pace/Mile': pace,
            'Time': time,
            'Heart Rate Avg': heart_rate
        })
    
    # Create DataFrame and export to CSV
    df = pd.DataFrame(activities)
    output_file = 'strava_activities.csv'
    df.to_csv(output_file, index=False)
    print(f"Exported {len(activities)} activities to {output_file}")

if __name__ == "__main__":
    main() 