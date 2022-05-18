# Twitch Tracker Scraper

A webscraper to grab data from Twitch Tracker Stream page for any streamer and convert it to a dataframe.
Just supply the Twitch ID of the streamer and where you want the csv export of the dataframe to go.

Requires Selenium to be installed

Example:

```
  # Creates an instance of the Twitch Exporter then runs main()
  # Be sure to keep the "r" in front of the 'ExportPath' to ensure Python reads 
  
  TwitchExporter = TwitchTrackerExport('StreamerID', r'ExportPath')
  df = TwitchExporter.main()
  print(df)
```

## Things to Do
- Add Games column to the export
