import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# --- User Configuration ---
LOGIN_URL = ""
TARGET_CONSULATE = ""

# --- Script Logic ---
def check_visa_appointments_after_manual_login():
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
        driver.get(LOGIN_URL)
        print("Navigated to login page in the new browser window.")

        # Handle the initial pop-up if it appears
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()=\'OK\']"))
            ).click()
            print("Clicked OK on initial pop-up.")
        except:
            print("No initial pop-up found or clickable.")
            pass

        print("\n*** IMPORTANT: Please manually log in to the browser window that just opened. ***")
        print("*** After you have successfully logged in and are on the appointment scheduling page, ***")
        print("*** return to this console and press Enter to continue the script. ***\n")
        input("Press Enter to continue after manual login...")

        # After manual login, wait for the consulate dropdown to be present and visible
        print("Continuing script. Waiting for the consulate selection dropdown to appear...")
        consulate_dropdown = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "appointments_consulate_id"))
        )
        print("Consulate dropdown found.")

        select = Select(consulate_dropdown)
        select.select_by_visible_text(TARGET_CONSULATE)
        print(f"Selected consulate: {TARGET_CONSULATE}")

        # Click the \'Schedule Appointment\' button to trigger date loading
        retries = 5
        for i in range(retries):
            try:
                schedule_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@value=\'Schedule Appointment\']"))
                )
                schedule_button.click()
                print("Clicked \'Schedule Appointment\'.")
                break # Exit loop if click is successful
            except Exception as e:
                print(f"Attempt {i+1} failed to click \'Schedule Appointment\' button: {e}")
                if i < retries - 1:
                    print("Retrying in 10 seconds...")
                    time.sleep(10)
                else:
                    print("Max retries reached for clicking Schedule Appointment button.")
                    raise # Re-raise the exception if all retries fail

        # Check for available dates
        if "There are no appointments available at this location." in driver.page_source:
            print(f"No appointments available in {TARGET_CONSULATE} at this time.")
        else:
            print(f"Appointments might be available in {TARGET_CONSULATE}!")
            print("Please check the browser window for details.")

    except Exception as e:
        print(f"An error occurred during the process: {e}")
        print("Final page source at the time of error:")
        print(driver.page_source)
    finally:
        print("Closing browser.")
        driver.quit()

if __name__ == "__main__":
    check_visa_appointments_after_manual_login()


