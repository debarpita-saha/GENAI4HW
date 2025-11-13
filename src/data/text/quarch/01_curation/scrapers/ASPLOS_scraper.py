import os
import re
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ACM_FOLDER_NAME = "ASPLOS/"


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
driver_path = "/Users/aadyapipersenia/Desktop/chromedriver-mac-arm64/chromedriver"

# Create a service object
service = Service(executable_path=driver_path)

# Create a Chrome webdriver instance
driver = webdriver.Chrome(service=service)

# login_url = "https://guides.library.harvard.edu/cs/articles"
# driver.get(login_url)
# time.sleep(5)

# # Click on the ACM link
# acm_link = driver.find_element(By.LINK_TEXT, "ACM Digital Library")

# driver.execute_script("arguments[0].click();", acm_link)
# time.sleep(45)

temp_url = "https://dl.acm.org"
driver.get(temp_url)
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

ASPLOS = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.browse-link[href='/conference/asplos']")
    )
)  # bas aise hi change karna hai
driver.execute_script("arguments[0].click();", ASPLOS)
time.sleep(5)

ViewAllProceedings = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
            "a[href='/conference/asplos/proceedings'][title='View all Proceedings']",
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
for n, proceeding in enumerate(proceedings):  # Number of proceedings to download
    anchor_element = proceeding.find_element(
        By.CSS_SELECTOR, "div.conference__title > a"
    )
    print(proceeding.text)
    # year = re.search(r"\d{2}", proceeding.text).group()
    year = str(28 - n - 5)  # subract proceedings[x:] , n - x
    if int(year) < 10 and int(year) > 0:
        year = "200" + year
    elif int(year) == 0:
        year = "2000"
    elif int(year) < 0:
        year = str(2000 + int(year))
    else:
        year = "20" + year
    # year = str(2000 + (28 - n - 5)) if n > 23 else str(1900 + (28 - n - 5))
    urls[year] = anchor_element.get_attribute("href")
print(urls)


for year in urls:
    url = urls[year]
    # Open the webpage in the browser window
    driver.get(url)
    time.sleep(5)

    # Accept the cookies
    # try:
    #     cookies_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable(
    #             (By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll")
    #         )
    #     )
    #     # Click the "I accept" button using JavaScript
    #     driver.execute_script("arguments[0].click();", cookies_button)
    #     print("Clicked the button: Use necessary cookies only")
    # except:
    #     print("Cookies button not found")

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
            try:
                driver.execute_script("arguments[0].click();", show_all_button)
            except:
                continue
            print("Clicked Show All button")
            time.sleep(20)
            print("Sleep over")

            # Scroll to the bottom of the page to load all the results
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        except:
            print("Show All button not found. Skipping...")
        # Wait for the results to load and then get the list of all the links
        try:
            results = WebDriverWait(driver, 10).until(  # by Aria label
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[@aria-label='PDF']")
                )
            )
        except:
            print("Results not found")

        print(f"Found {len(results)} results")

        # Download the PDFs
        for i, result in enumerate(results):
            # Get the link to the PDF
            pdf_link = result.get_attribute("href")

            # Download the PDF
            download_pdf(pdf_link, ACM_FOLDER_NAME + str(year) + "/", str(i) + ".pdf")
            time.sleep(30)  # to avoid getting blocked
    else:
        print(len(sessions), "Sessions. Executing session-wise download.")
        pdf_count = 0
        for session_num in range(len(sessions)):
            session_id = (
                f"heading{session_num+1}"  # Start with "heading" as the base ID
            )

            # Find the session element using either "heading" or "sec" ID
            session = None
            try:
                session = driver.find_element(By.ID, session_id)
            except NoSuchElementException:
                session_id = (
                    f"sec{session_num+1}"  # Fallback to "sec" ID if "heading" not found
                )
                try:
                    session = driver.find_element(By.ID, session_id)
                except NoSuchElementException:
                    print(f"Session element not found for {session_id}")
                    continue

            # session = driver.find_element(By.ID, f"heading{session_num+2}")
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
                    ACM_FOLDER_NAME + str(year) + "/" + session.text[9:] + "/",
                    str(i) + ".pdf",
                )
                pdf_count += 1
                time.sleep(30)  # to avoid getting blocked
            # session_close = driver.find_element(By.ID, f"heading{session_num+2}")
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.ID, session_id)
            )
            time.sleep(10)

# Close the browser window
driver.quit()
