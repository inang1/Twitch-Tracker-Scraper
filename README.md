A webscraper to grab data from Twitch Tracker Stream page for any streamer and convert it to a dataframe.
Just supply the Twitch ID of the streamer and the number of pages to iterate through.

Things to do:
- Implement pagination (currently only scrapes the first page)
- Clean up the DateTime column in the dataframe to separate the two for easier parsing
- Clean the Duration column to remove the "hrs" from each
- Clean the Views column so that 0 is in place of the blanks
