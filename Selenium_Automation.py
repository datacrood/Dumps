import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.safari.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Constants
URL = 'https://omms.nic.in/'
STATES = ["Andhra Pradesh", "Bihar", "Haryana", "Maharashtra", "Rajasthan"]
YEAR = "2008"

def setup_driver():
    service = Service()
    driver = webdriver.Safari(service=service)
    driver.set_window_size(1920, 1080)
    return driver

def navigate_to_road_wise_progress(driver):
    driver.get(URL)
    progress_monitoring = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Progress Monitoring ')]"))
    )
    time.sleep(2)
    progress_monitoring.click()

    road_wise_progress = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Road wise progress of Work')]"))
    )
    time.sleep(2)
    road_wise_progress.click()

def select_year_and_view(driver, year):
    year_dropdown = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "YearList_RoadWiseProgressDetails"))
    )
    year_select = Select(year_dropdown)
    time.sleep(1)
    year_select.select_by_value(year)
    time.sleep(1)

    view_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnViewRoadWiseProgressWork"))
    )
    time.sleep(1)
    view_button.click()
    time.sleep(2)

def get_iframe_src(driver):
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    return iframe.get_attribute('src')

def clean_number(value):
    return re.sub(r'[^\d.]', '', value)

def scrape_state_data(driver, state, src):
    driver.get(src)
    time.sleep(2)

    state_link = WebDriverWait(driver, 8).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{state}')]"))
    )
    time.sleep(1)
    state_link.click()
    time.sleep(2)

    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table[.//div[contains(text(), 'District Name')]]"))
    )

    soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
    rows = soup.find_all('tr')

    state_data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 5:
            district = cols[1].text.strip()
            if district.lower() in ['total', 'sr.no.', 'district name'] or not district:
                continue
            total_works = clean_number(cols[2].text.strip())
            road_length = clean_number(cols[3].text.strip())
            sanction_cost = clean_number(cols[4].text.strip())
            state_data.append([state, district, total_works, road_length, sanction_cost])
    
    return state_data

def clean_dataframe(df):
    df['Total No of Works'] = pd.to_numeric(df['Total No of Works'], errors='coerce')
    df = df[~df['Total No of Works'].isna()]
    df['Total No of Works'] = df['Total No of Works'].astype(int)
    df['Road Length'] = df['Road Length'].astype(float)
    df['Sanction Cost'] = df['Sanction Cost'].astype(float)
    return df

def main():
    driver = setup_driver()
    navigate_to_road_wise_progress(driver)
    select_year_and_view(driver, YEAR)
    src = get_iframe_src(driver)

    all_data = []
    for state in STATES:
        try:
            state_data = scrape_state_data(driver, state, src)
            all_data.extend(state_data)
        except Exception as e:
            print(f"An error occurred while processing {state}: {e}")

    df = pd.DataFrame(all_data, columns=['State', 'District', 'Total No of Works', 'Road Length', 'Sanction Cost'])
    clean_df = clean_dataframe(df)
    clean_df.to_csv('output.csv', index=False)

    driver.quit()

if __name__ == "__main__":
    main()