import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# --- User Configuration ---
VISA_APPOINTMENT_URL = ""
USER_EMAIL = ""
USER_PASSWORD = ""
TARGET_CONSULATE = ""

# --- Script Logic ---
def check_visa_appointments():
    print("Starting visa appointment check...")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run in headless mode (no browser UI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Add a user-agent to make the request look more like a real browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(VISA_APPOINTMENT_URL)
        print("Navigated to login page.")

        # Handle the initial pop-up if it appears
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()=\'OK\']"))
            ).click()
            print("Clicked OK on initial pop-up.")
        except:
            print("No initial pop-up found or clickable.")
            pass

        # Attempt Login
        print("Attempting to log in...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_email"))
        ).send_keys(USER_EMAIL)
        driver.find_element(By.ID, "user_password").send_keys(USER_PASSWORD)
        
        # Handle the policy confirmation checkbox click
        try:
            # Try clicking the div that intercepts the click
            policy_div = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, \'icheckbox\') and .//input[@name=\'policy_confirmed\']]"))
            )
            policy_div.click()
            print("Clicked policy confirmation div.")
        except Exception as e:
            print(f"Could not click policy confirmation div, trying JavaScript: {e}")
            # Fallback to JavaScript click if direct click fails
            driver.execute_script("document.querySelector(\'input[name=\'policy_confirmed\']\').click();")
            print("Clicked policy confirmation checkbox using JavaScript.")

        driver.find_element(By.NAME, "commit").click()
        print("Login credentials submitted.")

        # After login, wait for the URL to change to the schedule page or dashboard
        WebDriverWait(driver, 20).until(
            EC.url_contains("/schedule/") or EC.url_contains("/dashboard/")
        )
        print("Successfully logged in and redirected.")

        # Navigate directly to the appointment page again to ensure correct URL
        # This is a workaround for potential redirects or session issues after login
        driver.get(VISA_APPOINTMENT_URL)
        print("Navigated to appointment scheduling page.")

        # Select the consulate location
        try:
            consulate_dropdown = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "appointments_consulate_id"))
            )
            select = Select(consulate_dropdown)
            select.select_by_visible_text(TARGET_CONSULATE)
            print(f"Selected consulate: {TARGET_CONSULATE}")
        except Exception as e:
            print(f"Error selecting consulate: {e}")
            print("Current page source after login and navigation:")
            print(driver.page_source)
            raise # Re-raise the exception to stop execution and show the error

        # Click the \'Schedule Appointment\' button to trigger date loading
        # This might be the step that sometimes returns \'System is busy\'
        try:
            schedule_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value=\'Schedule Appointment\']"))
            )
            schedule_button.click()
            print("Clicked \'Schedule Appointment\'.")
        except Exception as e:
            print(f"Error clicking \'Schedule Appointment\' button: {e}")
            print("Current page source after consulate selection:")
            print(driver.page_source)
            raise # Re-raise the exception

        # Check for available dates
        # Look for the specific text indicating no appointments
        if "There are no appointments available at this location." in driver.page_source:
            print(f"No appointments available in {TARGET_CONSULATE} at this time.")
        else:
            print(f"Appointments might be available in {TARGET_CONSULATE}!")
            print("Please check the browser window for details.")
            # You might want to add more sophisticated parsing here
            # For example, looking for specific date elements or calendar tables
            # print(driver.page_source) # Uncomment to see the full page source

    except Exception as e:
        print(f"An error occurred during the process: {e}")
        print("Final page source at the time of error:")
        print(driver.page_source)
    finally:
        print("Closing browser.")
        driver.quit()

if __name__ == "__main__":
    check_visa_appointments()


