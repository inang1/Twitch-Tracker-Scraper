from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import datetime as dt

def loadPage(StreamerID):
        url = 'https://twitchtracker.com/' + str(StreamerID) + '/streams'
        options = Options()
        options.headless = False
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        return(driver)

def initLists():
    datetimes = []
    durations = []
    avgCCV = []
    maxCCV = []
    followers = []
    views = []
    titles = []
    return(datetimes, durations, avgCCV, maxCCV, followers, views, titles)

def scrapeData(driver, datetimes, durations, avgCCV, maxCCV, followers, views, titles):
    # For loop goes 20 times, corresponding to the number of streams per page
    # It gets the xpath of each stream and appends them to the corresponding list
    for _ in range(1, 21):
        datetimexpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr["+ str(_) + "]/td[1]/a/span"
        datetimes.append(driver.find_element(by = By.XPATH, value = datetimexpath).text)

        durationxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_) +"]/td[2]/span"
        durations.append(driver.find_element(by = By.XPATH, value = durationxpath).text)

        avgCCVxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_) + "]/td[3]/span"
        avgCCV.append(driver.find_element(by = By.XPATH, value = avgCCVxpath).text)

        maxCCVxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_) + "]/td[4]/span"
        maxCCV.append(driver.find_element(by = By.XPATH, value = maxCCVxpath).text)

        followersxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_) + "]/td[5]/span"
        followers.append(driver.find_element(by = By.XPATH, value = followersxpath).text)

        viewsxpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr[" + str(_)+ "]/td[6]/span"
        views.append(driver.find_element(by = By.XPATH, value = viewsxpath).text)

        titlexpath = "/html/body/div[2]/div[4]/div[5]/div[2]/table/tbody/tr["+str(_)+"]/td[7]"
        titles.append(driver.find_element(by = By.XPATH, value = titlexpath).text)

    return(datetimes, durations, avgCCV, maxCCV, followers, views, titles)

def nextPage(driver, CurrentPage):
    nextpageXPATH = "/html/body/div[2]/div[4]/div[5]/div[2]/div/ul/li[" + str(CurrentPage + 1) + "]/a"
    link = driver.find_element(By.XPATH, value = nextpageXPATH)
    href = link.get_attribute('href')
    href.click()


def combineData(datetimes, durations, avgCCV, maxCCV, followers, views, titles):
    # Remove hrs text from durations
    durations = [i.strip(' hrs') for i in durations]

    # Compile data and convert to dataframe
    data = list(zip(datetimes, durations, avgCCV, maxCCV, followers, views, titles))
    df = pd.DataFrame(data, columns = ['DateTime', 'Duration (hrs)', 'avgCCV', 'maxCCV', 'Followers', 'Views', 'Title'])

    # Convert DateTime column to datetime object and parse
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    df['Date'] = df['DateTime'].dt.strftime('%m/%d/%Y')
    df['Time'] = df['DateTime'].dt.strftime('%H:%M%:%S')

    # Convert Date and Time columns to dt objects
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = pd.to_datetime(df['Time'])

    # Remove dates from Time column
    df['Time'] = df['Time'].dt.time

    # Add Day of Week column
    df['Day'] = df['Date'].dt.strftime('%A')

    # Drop original DateTime column from the dataframe
    df = df.drop('DateTime', axis = 1)

    # Fill in blanks with 0s
    df.replace("", 0)

    # Reorder DataFrame
    df = df[['Date', 'Time', 'Duration (hrs)', 'avgCCV', 'maxCCV', 'Followers', 'Views', 'Title']]

    # Export df to csv
    df.to_csv(r"C:\Users\Isabella\Documents\Projects\Twitch Tracker Scraper\TwitchTrackerExport.csv")
    return(df)

def main(StreamerID, numPages):
    driver = loadPage(StreamerID)
    datetimes, durations, avgCCV, maxCCV, followers, views, titles = initLists()
    datetimes, durations, avgCCV, maxCCV, followers, views, titles = scrapeData(driver, datetimes, durations, avgCCV, maxCCV, followers, views, titles)
    df = combineData(datetimes, durations, avgCCV, maxCCV, followers, views, titles)
    return df

df = main('iankung', 9)
print(df)
