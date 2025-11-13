import os
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ACM_FOLDER_NAME = "MICRO/"


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


# Replace the path with your actual absolute Chrome driver path
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


MICRO = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.browse-link[href='/conference/micro']")
    )
)
driver.execute_script("arguments[0].click();", MICRO)  # Clicks on MICRO conference
time.sleep(5)

ViewAllProceedings = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
            "a[href='/conference/micro/proceedings'][title='View all Proceedings']",
        )
    )
)
driver.execute_script(
    "arguments[0].click();", ViewAllProceedings
)  # Clicks on View All Proceedings
time.sleep(5)

ViewAllAgain = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "span.show-more-items__btn-holder span.btn")
    )
)
driver.execute_script(
    "arguments[0].click();", ViewAllAgain
)  # Clicks on View All Proceedings again
time.sleep(5)

try:
    proceedings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "conference__proceedings"))
    )  # Finds all proceedings of MICRO
except:
    proceedings = []
    print("Proceedings not found")

print(f"Found {len(proceedings)} proceedings")

urls = (
    {}
)  # Dictionary to store the URLs of all the proceedings. Key: proceeding number, Value: URL
for proceeding in proceedings:
    anchor_element = proceeding.find_element(
        By.CSS_SELECTOR, "div.conference__title > a"
    )
    # Find index of the last occurence of a colon
    colon_index = anchor_element.text.rfind(":")
    print(anchor_element.text)

    # identify the integer formed by the characters after the last colon
    proceeding_number = int(
        re.findall(r"\d+", anchor_element.text[colon_index + 1 :])[0]
    )  # +1 to skip the colon
    urls[proceeding_number] = anchor_element.get_attribute("href")
print(urls)
print(len(urls))

for proceeding_number in urls:
    url = urls[proceeding_number]
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
        )  # Finds all sessions of MICRO
    except:
        print(
            "Sessions not found"
        )  # If no sessions found, then sessions = []. This implies that the PDFs are directly stored in the proceedings page without any sessions.
        sessions = []
        print(len(sessions), "Sessions")

    if len(sessions) == 0:  # That is, if there are no sessions
        print("Sessions not found. Executing direct PDF download.")
        try:
            show_all_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "showAllProceedings"))
            )  # Wait for the "Show All" button to be clickable and scroll to it

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
            download_pdf(
                pdf_link,
                ACM_FOLDER_NAME + str(proceeding_number) + "/",
                str(i) + ".pdf",
            )
            time.sleep(20)  # to avoid getting blocked
    else:
        print(len(sessions), "Sessions. Executing session-wise download.")
        time.sleep(10)
        pdf_count = 0
        for session_num in range(len(sessions)):
            session = driver.find_element(By.ID, f"heading{session_num+1}")
            print("Executing ", session.text)
            if session_num != 0:  # The first session is already open usually.
                driver.execute_script("arguments[0].scrollIntoView();", session)
                time.sleep(5)

                try:
                    driver.execute_script("arguments[0].click();", session)
                    time.sleep(20)
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
                    + str(proceeding_number)
                    + "/"
                    + session.text[9:].replace("/", "_or_").replace(" ", "_")
                    + "/",
                    str(i) + ".pdf",
                )
                pdf_count += 1
                time.sleep(20)  # to avoid getting blocked
            session_close = driver.find_element(By.ID, f"heading{session_num+1}")
            driver.execute_script("arguments[0].click();", session_close)
            time.sleep(10)

# Close the browser window
driver.quit()
