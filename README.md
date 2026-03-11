# Tennis Court Reservation Automation

## Overview

This project automates the reservation of tennis courts using **Selenium**, **Behave (BDD)**, and **Allure reporting**.
The automation navigates through the reservation website, selects a desired court and time slot, fills out reservation details, and submits the booking.

The goal of the project is to demonstrate **test automation framework design**, including:

* Behavior Driven Development (BDD) using Behave
* Selenium UI automation
* Structured test execution
* Test reporting with Allure
* Configurable reservation parameters

---

# Tech Stack

* Python 3.x
* Selenium
* Behave (BDD Framework)
* Allure-Behave (Reporting)
* WebDriver Manager

---

## 1. Install dependencies

Install all required packages using:

```
pip install -r requirements.txt
```

Example dependencies include:

```
selenium
behave
allure-behave
webdriver-manager
```

---

# Project Structure

```
project-root
│
├── tests
│   ├── features
│   │   └── tennis_court_reservation.feature
│   │
│   ├── steps
│   │   └── tennis_court_reservation_steps.py
├── config.json
├── requirements.txt
└── README.md
```

### Description

**config.json**

* Defines reservation parameters such as:

  * desired court
  * time slot
  * event name
  * execution toggle

Example:

```
{
  "execute": true,
  "court_name": "HPTC - Court 01",
  "time_slot": "7:30 AM - 9:00 AM",
  "event_name": "Rodrigo Avila Merchan"
}
```

**tests/features/**

* Contains Gherkin feature files describing test scenarios.

**tests/features/steps/**

* Contains step definitions implementing automation logic.

---

# Running the Tests

Execute the automation using the following command:

```
behave -f allure_behave.formatter:AllureFormatter -o allure-results ./tests/features
```

This will:

* Execute all Behave feature files
* Generate Allure-compatible test results

---

# Test Reporting

This project uses **Allure reporting** for detailed execution reports.

## Generate the report

After running tests:

```
allure serve allure-results
```

This will open an interactive report in your browser.

The report includes:

* Test execution status
* Step-by-step logs
* Failures and stack traces
* Execution timeline

---

# Assertions

Assertions are implemented inside **step definitions** to validate expected behavior.

Assertions verify:

* UI elements are present
* Elements are clickable
* Reservation confirmation is successful

If an assertion fails, the test scenario is marked as **failed**.

---

# Configuration Driven Execution

Reservation parameters are defined in the **config.json** file to avoid modifying the test code.

The automation reads values such as:

* court name
* time slot
* event name

This allows users to configure reservations **without editing the test scripts**.

---

# Challenges Faced

## 1. UI Changes

The reservation system UI changed during development, requiring updates to element locators and interaction logic.

To address this:

* Stable attributes such as `data-qa-id` were used whenever available.
* XPath locators were minimized.

---

## 2. Dynamic Elements

Many elements were dynamically loaded via JavaScript.

Solutions:

* Explicit waits (`WebDriverWait`)
* `element_to_be_clickable`

---

## 3. reCAPTCHA Verification

The reservation system occasionally triggered **reCAPTCHA validation failures** when requests were submitted too quickly.

Mitigation approaches included:

* Adding small delays before submitting reservations
* Ensuring user interaction occurred before final submission

---

# Author

Rodrigo Avila Merchan
