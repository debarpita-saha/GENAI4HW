# Data Curation

[TODO: ALL FUTURE DOCUMENTATION DURING SUMMER 2024]

## Using Scrapers
Follow the steps below in order to programmatically download the PDFs:
1. Set up conda environment.
2. Download chrome webdriver corresponding to your Chrome version from the link: https://chromedriver.chromium.org/downloads
3. Move the webdriver to your desired location and paste its absolute path in the 'driver_path' variable of the python file corresponding to the conference you are interested in.
4. Run the python file and observe the PDFs being downloaded one by one!
The PDFs will be downloaded in a new folder at the same level as that of the python file.

> **Note:** This will download only those papers permitted to your IP address. In case of unreliable internet connectivity or any anomalies on the website, you might need to manually adjust the location of a few PDFs being downloaded (in case of proceedings where papers are segregated based on sessions).
