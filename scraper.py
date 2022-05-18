from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

class TwitchTrackerExport:

    def __init__(self, StreamerID, ExportPath):
        self.ExportPath = str(ExportPath)
        self.StreamerID = StreamerID
        self.datetimes = []
        self.durations = []
        self.avgCCV = []
        self.maxCCV = []
        self.followers = []
        self.views = []
        self.titles = []

        # Load page
        self.url = 'https://twitchtracker.com/' + str(StreamerID) + '/streams'
        options = Options()
        options.headless = False
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.driver.get(self.url)

        # Get number of pages to iterate through
        links = self.driver.find_elements(By.XPATH, "//ul[@class='pagination']/li/a")
        self.numPages = int(links[-1].text)-1

        # Sets CurrentPage to 1
        self.currentPage = 1

    def nextPage(self):
        # Find all pagination links
        next = str(self.currentPage + 1)
        nextXPATH = "//ul[@class='pagination']/li/a[text() =" + next + "]"

        element = self.driver.find_element(By.XPATH, nextXPATH)

        # Scrolls to the bottom of the page so button is in view then clicks
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element.click()

        self.currentPage += 1

    def scrapeData(self):
        # Grab the number of streams on the page
        streamsXPATH = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr"
        numStreams = int(len(self.driver.find_elements(By.XPATH, streamsXPATH))) + 1

        # Loops through each stream getting the XPATH for each item
        # Then appends the data to the corresponding list
        for _ in range(1, numStreams):
            datetimexpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr["+ str(_) + "]/td[1]/a/span"
            self.datetimes.append(self.driver.find_element(by = By.XPATH, value = datetimexpath).text)

            durationxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_) +"]/td[2]/span"
            self.durations.append(self.driver.find_element(by = By.XPATH, value = durationxpath).text)

            avgCCVxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_) + "]/td[3]/span"
            self.avgCCV.append(self.driver.find_element(by = By.XPATH, value = avgCCVxpath).text)

            maxCCVxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_) + "]/td[4]/span"
            self.maxCCV.append(self.driver.find_element(by = By.XPATH, value = maxCCVxpath).text)

            followersxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_) + "]/td[5]/span"
            self.followers.append(self.driver.find_element(by = By.XPATH, value = followersxpath).text)

            viewsxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_)+ "]/td[6]/span"
            self.views.append(self.driver.find_element(by = By.XPATH, value = viewsxpath).text)

            titlexpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr["+str(_)+"]/td[7]"
            self.titles.append(self.driver.find_element(by = By.XPATH, value = titlexpath).text)

    def combineData(self):
        # Remove hrs text from durations
        self.durations = [i.strip(' hrs') for i in self.durations]

        # Compile data and convert to dataframe
        data = list(zip(self.datetimes, self.durations, self.avgCCV, self.maxCCV, self.followers, self.views, self.titles))
        df = pd.DataFrame(data, columns = ['DateTime', 'Duration (hrs)', 'avgCCV', 'maxCCV', 'Followers', 'Views', 'Title'])

        # Convert DateTime column to datetime object and parse
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['Date'] = df['DateTime'].dt.strftime('%m/%d/%Y')
        df['Time'] = df['DateTime'].dt.strftime('%H:%M:%S')

        # Convert Date and Time columns to dt objects
        df['Date'] = pd.to_datetime(df['Date'])
        df['Time'] = pd.to_datetime(df['Time'])
        df['Time'] = df['Time'].dt.time

        # Add Day of Week column
        df['Day'] = df['Date'].dt.strftime('%A')

        # Drop original DateTime column from the dataframe
        df = df.drop('DateTime', axis = 1)

        # Fill in blanks with 0s
        df.replace("", 0)

        # Reorder columns
        df = df[['Date', 'Time', 'Day', "Duration (hrs)", 'avgCCV', 'maxCCV', 'Followers', 'Views', 'Title']]

        # Export df to csv
        df.to_csv(self.ExportPath)
        return(df)

    def main(self):
        # Scrapes the first page
        self.scrapeData()

        # Loop to go through the rest of the pages and scrape
        for _ in range(self.numPages):
            self.nextPage()
            self.scrapeData()

        # Ends the driver
        self.driver.close()
        self.driver.quit()

        # Create the dataframe
        df = self.combineData()
        return(df)

TwitchExporter = TwitchTrackerExport('iankung', r"C:\Users\Isabella\Documents\Projects\Twitch Tracker Scraper\TwitchTrackerExport.csv")
df = TwitchExporter.main()
print(df)
