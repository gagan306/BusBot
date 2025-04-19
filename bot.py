from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib  # For sending email notifications
from datetime import datetime

# Function to send an email if buses are not available
def send_email(subject, body):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Start TLS for security
    server.login(bhusalgagn612@gmail.com, gmailpassword)  # Use your email and an app password
    
    # Email content
    message = f'Subject: {subject}\n\n{body}'
    
    # Send the email
    server.sendmail(sender email, receiver email, message)
    print(f"Email sent: {subject}")  # Confirm email was sent
    
    # Quit the server
    server.quit()

# Function to check bus availability
def check_bus_availability():
    driver = webdriver.Chrome()  # Ensure chromedriver is installed and in PATH
    driver.get('https://bussewa.com')  # Visit the website

    try:
        # Wait until the page is fully loaded and the "From" dropdown is visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search_from_destination'))
        )

        # Use JavaScript to set the value of the "From" dropdown (Select2)
        driver.execute_script("""$('#search_from_destination').val('Kathmandu').trigger('change');""")

        # Wait for the "To" dropdown to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search_to'))
        )

        # Use JavaScript to set the value of the "To" dropdown (Select2)
        driver.execute_script("""$('#search_to').val('Butwal').trigger('change');""")

        # Wait for the custom Nepali date picker field to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'nepali-datepicker'))
        )

        # Set the date value using JavaScript (format: your custom date format)
        desired_date = '2081-06-18'  # Set your desired Nepali date here (Nepali calendar)

        # Use JavaScript to update the date picker value and trigger the necessary events
        driver.execute_script("""let dateField = document.querySelector('.nepali-datepicker.ndp-nepali-calendar');
                                 dateField.value = arguments[0];
                                 dateField.dispatchEvent(new Event('input'));""", desired_date)

        # Log the success to verify both dropdowns and the date have been filled
        print(f"Form filled with 'Kathmandu' as 'From', 'Butwal' as 'To', and Nepali date {desired_date}.")

        # Submit the form
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search')]"))
        )
        submit_button.click()
        print("Form submitted!")

        # Wait for the trip list container to load and check for availability
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'trip-list-container'))
        )
        
        # Check if there are any trips available by checking the 'trip-infos' class within the container
        trip_infos = driver.find_elements(By.CLASS_NAME, 'trip-infos')
        
        if not trip_infos:
            print("No buses available.")
            # Send an email notification saying no buses are available
            send_email(subject="No Bus Availability", body="No buses are available for your selected route and date.")
        else:
            print("Buses are available!")
            # Send an email notification saying buses are available
            send_email(subject="Bus Availability", body="Buses are available on your selected route and date. Check the website for more details.")

    except Exception as e:
        # Capture and print any exceptions
        print(f"An error occurred: {str(e)}")

    finally:
        time.sleep(5)  # Wait for 5 seconds to visually verify the result
        driver.quit()  # Close the browser

# Function to schedule the bus checks every 30 minutes between 6 AM and 10 PM
def schedule_bus_checks_30_minutes():
    while True:
        current_time = datetime.now().time()
        start_time = current_time.replace(hour=6, minute=0, second=0, microsecond=0)
        end_time = current_time.replace(hour=22, minute=30, second=0, microsecond=0)
        
        # Only run between 6 AM and 10 PM
        if start_time <= current_time <= end_time:
            print(f"Running check at {datetime.now()}")
            check_bus_availability()
        else:
            print(f"Current time {current_time} is outside the allowed range (6 AM - 10 PM).")

        # Wait for 30 minutes (1800 seconds) before running the check again
        time.sleep(1800)  # 1800 seconds = 30 minutes

# Start the scheduled checks
if __name__ == "__main__":
    schedule_bus_checks_30_minutes()
