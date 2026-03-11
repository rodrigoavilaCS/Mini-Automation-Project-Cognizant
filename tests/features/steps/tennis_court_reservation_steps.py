from asyncio import wait
from multiprocessing import context

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime, timedelta
import json

@given('I am on the quick reservation page and logged in with valid credentials')
def step_on_quick_reservation_page(context):
    """
    Set up the browser and navigate to the quick reservation page for tennis court reservations
    and log in with valid credentials
    """
    # Set up Chrome options
    chrome_options = Options()
    #Primarliy used to prevent detection as a bot, but also helps with potential pop-up blockers and other automation-related issues
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Incognito mode to avoid potential caching issues
    chrome_options.add_argument("--incognito")
    
    # Initialize the webdriver
    context.driver = webdriver.Chrome(options=chrome_options)
    context.driver.maximize_window()
    context.wait = WebDriverWait(context.driver, 10)
    
    
    try:
        # Navigate to the quick reservation page
        context.driver.get("https://anc.apm.activecommunities.com/planoparksandrec/reservation/landing/quick?groupId=20")
        
        # Wait for the main content to load
        context.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "reservation-quick__main"))
        )
        
        # Verify we're on the correct page
        assert "quick" in context.driver.current_url.lower()
        
        # Click the login button to open the login form
        login_link = context.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "reservation-quick__signin-now-link"))
        )
        login_link.click()
        
        # Find and fill in login credentials
        username_field = context.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter your Email address']"))
        )
        password_field = context.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Password Required']"))
        )
        
        # Gather credentials from config file
        with open('config.json') as config_file:
            config = json.load(config_file)
            # Enter credentials
            username_field.send_keys(config["email"])
            password_field.send_keys(config["password"])

        # Click login button
        login_button = context.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()
    except TimeoutException:
        raise Exception("Failed to load the quick reservation page")


@when('I select a date and desired time slot for desired tennis court')
def step_select_date_and_time(context):
    """
    Select two days ahead and time slot for the tennis court reservation
    """
    try:
        # Wait for date picker to be available
        date_picker = context.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Date picker, current date']"))
        )
        date_picker.click()
        
        # Calculate date 2 days from today
        target_date = (datetime.today() + timedelta(days=2)).strftime("%b %d, %Y").replace(" 0", " ")

        date_cell = context.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@aria-label,'{target_date}')]")
            )
        )
        date_cell.click()
        
        # Fill out event name field
        event_name_field = context.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@data-qa-id="quick-reservation-eventType-name"]'))
        )
        event_name_field.clear()
        event_name_field.click()
        
        with open('config.json') as config_file:
            config = json.load(config_file)
            # Enter full name as event name
            event_name_field.send_keys(config["event_name"])
            
            # Click on desired court and time slot
            slot = context.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH, 
                        f"//div[contains(@aria-label,'{config['court_name']}') and contains(@aria-label,'{config['time_slot']}') and not(contains(@class,'disabled'))]"
                    )
                )
            )
            slot.click()
    except TimeoutException:
        raise Exception("Failed to select date and time slot")

@when('I confirm the booking reservation')
def step_confirm_reservation_details(context):
    """
    Review and confirm the reservation details
    """
    try:
        # Confirm the selection
        confirm_button = context.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-qa-id="quick-reservation-ok-button"]')
            )
        )
        confirm_button.click()
            
        # Click the reserve button to proceed
        reserve_button = context.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa-id="quick-reservation-reserve-button"]'))
        )
        reserve_button.click()
        
        # Wait for waiver popup to be visible
        context.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "waiver-panel"))
        )
        
        # Click the OK button on the waiver popup to confirm reservation
        waiver_ok_button = context.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='OK']]"))
        )
        waiver_ok_button.click()
        
    except TimeoutException:
        raise Exception("Failed to confirm reservation details")

@then('I should see a confirmation message with reservation details')
def step_verify_confirmation_message(context):
    """
    Verify that a confirmation message is displayed with the reservation details
    """
    try:
        # Wait for the confirmation message to be visible
        confirmation_message = context.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "confirmation-message"))
        )
        
        # Verify the confirmation message contains expected text
        assert "Your reservation is confirmed" in confirmation_message.text
        print("Reservation confirmed with details: " + confirmation_message.text)
        
    except TimeoutException:
        raise Exception("Failed to see confirmation message with reservation details")
    
def after_scenario(context, scenario):
    """
    Clean up after each scenario
    """
    if hasattr(context, 'driver'):
        context.driver.quit()