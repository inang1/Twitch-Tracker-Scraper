# Twitch Tracker Scraper

A webscraper to grab data from Twitch Tracker Stream page for any streamer and convert it to a dataframe and create a csv export.
Just supply the Twitch ID of the streamer and where you want the csv export of the dataframe to go.

Requires Selenium and pandas to be installed.

## How to Run:

```Python
  # Edit the following snippet of code at the bottom to have your desired streamer and export path
  # Be sure to keep the "r" in front of the 'ExportPath' to ensure Python reads the path correctly

  TwitchExporter = TwitchTrackerExport('StreamerID', r'ExportPath\csvName.csv')
```

To run, download the code, navigate to the directory within the command line, then run:

```
python scraper.py
```

## Things to Do
- Add Games column to the export
- Change code to match Python style guidelines
