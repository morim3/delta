import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from slack_sdk import WebClient
from selenium.webdriver.chrome.options import Options
import datetime

url = "https://dk.ncors.com/dlt/ncors/login.asp"
username = ""  
password = ""
line_token = ""  


def send_line(message):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_token}'}
    data = {'message': f'message: {message}'}
    requests.post(line_notify_api, headers = headers, data = data)


free_slots = {}

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
while True:
    try:

        driver.get(url)
        wait = WebDriverWait(driver, 1)

        driver.find_element(By.NAME, "USERID").send_keys(username)
        driver.find_element(By.NAME, "USERPASSWD").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='ログイン']").click()
        driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='　ＯＫ　']").click()

        time.sleep(2)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, "html.parser")
        reservation_table = soup.find("table", {"class": "Reservation"})

        rows = reservation_table.find_all("tr")

        new_free_slots = {}
        for i in range(1, len(rows)):
            cells = rows[i].find_all("td")
            for j in range(1, len(cells)):
                cell = cells[j]
                if "class" in cell.attrs and cell["class"][0] == "Free":
                    date = rows[i].find("td").text.strip()
                    time_slot = rows[0].find_all("th")[j].text.strip()
                    slot_key = f"{date}, {time_slot}"

                    if slot_key not in free_slots:
                        new_free_slots[slot_key] = True
                        # if date is 1 day after today, use emoji
                        today = datetime.date.today()
                        resev_date = datetime.date(2023, int(date[:2]), int(date[3:5]))
                        if (resev_date - today).days <= 2:
                            message = chr(0x203C) + f"{date}, {time_slot}"
                        elif (resev_date - today).days <= 5:
                            message = chr(0x2757) + f"{date}, {time_slot}"
                        else:
                            message = f"{date}, {time_slot}"

                        send_line(message)

                    else:
                        new_free_slots[slot_key] = free_slots[slot_key]

        free_slots = new_free_slots

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    time.sleep(60 * 5)

driver.quit()
