import os
import time
import smtplib
from datetime import datetime, time as dtime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def send_email(subject, body):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, GMAIL_PASSWORD)
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
    server.quit()

def check_bus_availability():
    driver = webdriver.Chrome()
    driver.get("https://bussewa.com")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search_from_destination")))
    driver.execute_script("$('#search_from_destination').val('Kathmandu').trigger('change');")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search_to")))
    driver.execute_script("$('#search_to').val('Butwal').trigger('change');")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nepali-datepicker")))
    desired_date = "2081-06-18"
    driver.execute_script(
        "let el = document.querySelector('.nepali-datepicker.ndp-nepali-calendar');"
        "el.value = arguments[0];"
        "el.dispatchEvent(new Event('input'));",
        desired_date
    )
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search')]"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "trip-list-container")))
    trips = driver.find_elements(By.CLASS_NAME, "trip-infos")
    subject = "Bus Availability" if trips else "No Bus Availability"
    body = "Buses are available on your selected route and date." if trips else "No buses are available for your selected route and date."
    send_email(subject, body)
    time.sleep(5)
    driver.quit()

def schedule_bus_checks_30_minutes():
    while True:
        now = datetime.now().time()
        if dtime(6, 0) <= now <= dtime(22, 30):
            check_bus_availability()
        time.sleep(1800)

if __name__ == "__main__":
    schedule_bus_checks_30_minutes()
