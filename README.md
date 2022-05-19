# Twitch Tracker Scraper

A webscraper to grab data from Twitch Tracker Stream page for any streamer and convert it to a dataframe.
Just supply the Twitch ID of the streamer and where you want the csv export of the dataframe to go.

Requires Selenium and pandas to be installed

Example:

```
  # Create an instance of the Twitch Exporter then run main()
  # Be sure to keep the "r" in front of the 'ExportPath' to ensure Python reads the path correctly

  TwitchExporter = TwitchTrackerExport('StreamerID', r'ExportPath')
  df = TwitchExporter.main()
  print(df)
```

## Things to Do
- Add Games column to the export
