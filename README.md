A webscraper to grab data from Twitch Tracker Stream page for any streamer and convert it to a dataframe.
Just supply the Twitch ID of the streamer and the number of pages to iterate through.

Things to do:
- Implement pagination (currently only scrapes the first page)
- Create a function to find number of pages (remove numPages as an input)
- Create a TwitchExport class to make the scraper object oriented (then make initLists function obsolete)
- Add Games column to the export
