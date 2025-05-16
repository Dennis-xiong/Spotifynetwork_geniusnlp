# Spotify Music Analysis

This project collects and analyzes data for 1000 Western artists from the Spotify API.

## Setup

1. **Install required packages**:
   ```
   pip install spotipy pandas matplotlib
   ```

2. **Get Spotify API Credentials**:
   - Create a Spotify Developer account at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new application to get your Client ID and Client Secret
   - Run the setup script:
     ```
     python setup_credentials.py
     ```
   - Enter your Client ID and Client Secret when prompted

## Usage

### Collecting Artist Data

Run the data collection script:
```
python spotify_artist_collector.py
```

This will:
- Connect to the Spotify API
- Search for Western artists
- Collect detailed information about 1000 artists
- Save the data to CSV and JSON files

The script may take some time to run due to API rate limits and the need to filter for Western artists.

### Analyzing the Data

Open the Jupyter notebook to analyze the collected data:
```
jupyter notebook collect_and_analysis.ipynb
```

The notebook includes:
- Basic statistics about the artists
- Distribution of popularity and followers
- Genre analysis
- Correlation between popularity and followers
- Lists of top artists by popularity and followers

## Files

- `setup_credentials.py`: Script to set up Spotify API credentials
- `spotify_artist_collector.py`: Script to collect artist data from Spotify
- `collect_and_analysis.ipynb`: Jupyter notebook for data analysis
- `western_artists.csv`: CSV file with collected artist data (created after running the collector)
- `western_artists.json`: JSON file with collected artist data (created after running the collector)

## Notes

- The data collection process respects Spotify API rate limits
- Progress is saved periodically during collection
- Western artists are identified based on their genres
- The analysis focuses on popularity, followers, and genres

## Requirements

- Python 3.6+
- spotipy
- pandas
- matplotlib
- Jupyter Notebook (for analysis)
