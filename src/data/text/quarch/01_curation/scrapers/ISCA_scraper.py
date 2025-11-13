import os
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ACM_FOLDER_NAME = "ISCA/"


def download_pdf(url, folder_path, file_name):
    """
    Downloads a PDF from the given URL and saves it to the specified filename.
    """
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        # Open the file in binary write mode
        with open(folder_path + file_name, "wb") as file:
            # Write the content of the response to the file
            file.write(response.content)
        print(f"PDF downloaded successfully to {folder_path + file_name}")
    else:
        print(f"Error downloading PDF: {response.status_code}")


# Replace the path with your actual Chrome driver path
driver_path = "/Users/shreyasgrampurohit/Documents/College_Academia/ArchNet-HUVJR/ArchNet-Local/chromedriver-mac-arm64/chromedriver"

# Create a service object
service = Service(executable_path=driver_path)

# Create a Chrome webdriver instance
driver = webdriver.Chrome(service=service)

acm_url = "https://dl.acm.org"
driver.get(acm_url)
time.sleep(5)

# Accept the cookies
try:
    cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll")
        )
    )
    # Click the "I accept" button using JavaScript
    driver.execute_script("arguments[0].click();", cookies_button)
    print("Clicked the button: Use necessary cookies only")
except:
    print("Cookies button not found")

time.sleep(10)

conference = driver.find_element(By.LINK_TEXT, "Conferences")
driver.execute_script("arguments[0].click();", conference)
time.sleep(5)

ISCA = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.browse-link[href='/conference/isca']")
    )
)  # bas aise hi change karna hai
driver.execute_script("arguments[0].click();", ISCA)
time.sleep(5)

ViewAllProceedings = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
            "a[href='/conference/isca/proceedings'][title='View all Proceedings']",
        )
    )
)
driver.execute_script("arguments[0].click();", ViewAllProceedings)
time.sleep(5)

ViewAllAgain = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "span.show-more-items__btn-holder span.btn")
    )
)
driver.execute_script("arguments[0].click();", ViewAllAgain)
time.sleep(5)

try:
    proceedings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "conference__proceedings"))
    )
except:
    proceedings = []
    print("Proceedings not found")

print(f"Found {len(proceedings)} proceedings")

urls = {}
for proceeding in proceedings[:]:  # Number of proceedings to download
    anchor_element = proceeding.find_element(
        By.CSS_SELECTOR, "div.conference__title > a"
    )
    year = re.search(r"\d{2}", proceeding.text).group()
    if int(year) > 50:
        year = "19" + year
    else:
        year = "20" + year
    urls[year] = anchor_element.get_attribute("href")
print(urls)

for year in urls:
    url = urls[year]
    # Open the webpage in the browser window
    driver.get(url)
    time.sleep(5)

    # Identify sessions:
    try:
        sessions = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "a[title^='SESSION:']",
                )
            )
        )
    except:
        print("Sessions not found")
        sessions = []
        print(len(sessions), "Sessions")

    if len(sessions) == 0:
        print("Sessions not found. Executing direct PDF download.")
        try:
            show_all_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "showAllProceedings"))
            )

            print(
                f"Found Show All button. Its text is {show_all_button.text}. It should be clickable. Scrolling to it..."
            )

            # Scroll to the "Show All" button
            driver.execute_script("arguments[0].scrollIntoView();", show_all_button)

            print("Scrolled to Show All button. Is it visible?")

            # Click the "Show All" button using JavaScript
            driver.execute_script("arguments[0].click();", show_all_button)
            try:  # In case it doesn't work the first time (yes, that happens sometimes :/)
                driver.execute_script("arguments[0].click();", show_all_button)
            except:
                continue
            print("Clicked Show All button")
            time.sleep(20)
            print("Sleep over")

            # Wait for the results to load and then get the list of all the links
            try:
                results = WebDriverWait(driver, 10).until(  # by Aria label
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//a[@aria-label='PDF']")
                    )
                )
            except:
                print("Results not found")
        except:
            print("Show All button not found")
            # Get the list of all the links, no need to wait
            results = driver.find_elements(By.XPATH, "//a[@aria-label='PDF']")

        # Scroll to the bottom of the page to load all the results
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

        print(f"Found {len(results)} results")

        # Download the PDFs
        for i, result in enumerate(results):
            # Get the link to the PDF
            pdf_link = result.get_attribute("href")

            # Download the PDF
            download_pdf(pdf_link, ACM_FOLDER_NAME + str(year) + "/", str(i) + ".pdf")
            time.sleep(25)  # to avoid getting blocked
    else:
        print(len(sessions), "Sessions. Executing session-wise download.")
        pdf_count = 0
        for session_num in range(len(sessions)):
            session = driver.find_element(By.ID, f"heading{session_num+1}")
            print("Executing ", session.text)
            if session_num != 0:
                driver.execute_script("arguments[0].scrollIntoView();", session)
                time.sleep(5)

                try:
                    driver.execute_script("arguments[0].click();", session)
                    time.sleep(10)
                except:
                    print("Didn't click")
                    continue

            # Wait for the results to load and then get the list of all the links
            try:
                results = WebDriverWait(driver, 10).until(  # by Aria label
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//a[@aria-label='PDF']")
                    )
                )
            except:
                results = []
                print("Results not found for this session")

            print(f"Found {len(results[pdf_count:])} results for this session")

            # Download the PDFs
            for i, result in enumerate(results[pdf_count:]):
                # Get the link to the PDF
                pdf_link = result.get_attribute("href")

                # Download the PDF
                download_pdf(
                    pdf_link,
                    ACM_FOLDER_NAME
                    + str(year)
                    + "/"
                    + session.text[9:].replace("/", "_or_").replace(" ", "_")
                    + "/",
                    str(i) + ".pdf",
                )
                pdf_count += 1
                time.sleep(25)  # to avoid getting blocked
            session_close = driver.find_element(By.ID, f"heading{session_num+1}")
            driver.execute_script("arguments[0].click();", session_close)
            time.sleep(10)

# Close the browser window
driver.quit()
