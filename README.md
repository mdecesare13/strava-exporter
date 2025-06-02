# Strava Activity Exporter

This script exports your Strava activities to a CSV file with the following columns:
- Date
- Activity Type (run, bike, swim, etc.)
- Distance (miles)
- Pace/Mile
- Time
- Heart Rate Average (if available)

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Strava API credentials:
```
STRAVA_CLIENT_ID=your_client_id_here
STRAVA_CLIENT_SECRET=your_client_secret_here
STRAVA_REFRESH_TOKEN=your_refresh_token_here
```

To get these credentials:
1. Go to https://www.strava.com/settings/api
2. Create an API application to get your Client ID and Client Secret
3. Follow the OAuth flow to get your refresh token

3. Run the script:
```bash
python3 export_strava.py
```

The script will create a file called `strava_activities.csv` in the current directory containing all your activities.

## Note
The `.env` file containing your Strava API credentials is excluded from Git for security reasons. Make sure to keep your credentials safe and never commit them to version control. 