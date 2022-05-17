from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

def loadPage(StreamerID):
        url = 'https://twitchtracker.com/' + str(StreamerID) + '/streams'
        options = Options()
        options.headless = True
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

def scrape_data(driver, datetimes, durations, avgCCV, maxCCV, followers, views, titles):
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

def combineData(datetimes, durations, avgCCV, maxCCV, followers, views, titles):
    data = list(zip(datetimes, durations, avgCCV, maxCCV, followers, views, titles))
    df = pd.DataFrame(data, columns = ['DateTime', 'Duration (hr)', 'avgCCV', 'maxCCV', 'Followers', 'Views', 'Titles'])
    return(df)

def main(StreamerID, numPages):
    driver = loadPage(StreamerID)
    datetimes, durations, avgCCV, maxCCV, followers, views, titles = initLists()
    datetimes, durations, avgCCV, maxCCV, followers, views, titles = scrape_data(driver, datetimes, durations, avgCCV, maxCCV, followers, views, titles)
    df = combineData(datetimes, durations, avgCCV, maxCCV, followers, views, titles)
    df.to_csv(r"C:\Users\Isabella\Documents\Projects\Twitch Tracker Scraper\TwitchTrackerExport.csv")
    return df

df = main('iankung', 9)
