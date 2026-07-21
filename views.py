"""
Refresh a GitHub profile page in the browser.

Install: pip install selenium
Run:     python demo.py
"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PROFILE_URL = "https://github.com/aashishbagmar"
REFRESH_COUNT = 1000
DELAY_SECONDS = 0.34  # pause between refreshes
HEADLESS = False  # set True to hide the browser window


def main() -> None:
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(PROFILE_URL)
        print(f"Opened {PROFILE_URL}")

        for i in range(1, REFRESH_COUNT + 1):
            if i > 1:
                driver.refresh()

            print(f"Refresh {i}/{REFRESH_COUNT}")

            if i < REFRESH_COUNT and DELAY_SECONDS > 0:
                time.sleep(DELAY_SECONDS)

        print("Done.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
