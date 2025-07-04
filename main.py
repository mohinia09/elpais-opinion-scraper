# Import necessary modules from Selenium

import os
import time
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


# Setup Chrome
options = Options()
#options.add_argument('--headless')  # Chrome runs in background

# Point to the ChromeDriver executable
chromedriver_path = shutil.which("chromedriver")
if chromedriver_path is None:
    raise Exception("chromedriver not found in PATH")

# Start driver
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

def save_article_image(article, idx):
    # Try to extract image element
    ext="jpg"
    src=None
    try:
        img = article.find_element(By.CSS_SELECTOR, "img")
        src = img.get_attribute("src")
    except NoSuchElementException:
        src=None
        print("No cover image found.")
    #save image to images/ folder
    if src and src.startswith("http"):
        filename = f"images/article_{idx}.{ext}"
        response = requests.get(src, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
                print(f"Image saved: {filename}")
        else:
            print(f"Failed to download image: {src} (status {response.status_code})")


def new_article_fetch():
    #image directory
    os.makedirs("images", exist_ok=True)
    try:
        # Fetch the top 5 article from <articles> tag
        articles = driver.find_elements(By.CSS_SELECTOR, "article.c.c-d")

        # Fallback: If above doesn't work, try a more generic selector
        if len(articles) < 5:
            articles = driver.find_elements(By.TAG_NAME, "articles.c")

        if len(articles) ==0:
            raise Exception("No articles found.")

        top_titles = []
        for idx, article in enumerate(articles[:5]):
            #Scroll into view
            driver.execute_script("arguments[0].scrollIntoView(true);", article)
            time.sleep(0.1)  # let the browser reflow
            content = article.text.strip()
            # Print the content
            print("\n", "Article ", idx)
            print(content)

            #Save associated image if found
            save_article_image(article, idx)

            #Save article titles
            try:
                title = article.find_element(By.XPATH, ".//h2").text.strip()
            except NoSuchElementException:
                title = ""
            top_titles.append(title)

            # Mark test as passed
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": '
                '{"status":"passed","reason": "Top 5 articles fetched successfully"}}'
            )

    except Exception as e:
        # Mark test as failed with reason
        driver.execute_script(
            f'''browserstack_executor: {{
                "action": "setSessionStatus",
                "arguments": {{
                    "status": "failed",
                    "reason": "{str(e)}"
                }}
            }}'''
        )
        raise

try:
    # Step 1: Go to El País Opinion section
    driver.get("https://elpais.com/opinion/")
    time.sleep(3)
    # accept cookie
    # accept_cookies(driver)
    new_article_fetch()

finally:
    driver.quit()
