# Import necessary modules from Selenium

import os
import re
import time
import shutil
import requests
from selenium import webdriver
from collections import Counter
from selenium.webdriver.common.by import By
#from google.cloud import translate_v2 as translate
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Setup Translate client
#translate_client = translate.Client()
translated_titles = []

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
    """
    Saves the image from a given article element to a local 'image' folder.

    Args:
        article (WebElement): The article element containing the image tag.
        idx (int): The index used to uniquely name the saved image file.

    Returns:
        None
    """

    # Try to extract image
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


def fetch_articles():
    """
    Fetches and prints top 5 article elements from the currently loaded webpage. Also,
    saves the title of elements to a list.

    Returns:
        None
    """

    #image directory
    os.makedirs("images", exist_ok=True)
    try:
        # Fetch the top 5 article from <articles> tag
        articles = driver.find_elements(By.CSS_SELECTOR, "article.c.c-d")

        # Fallback: If above doesn't work, try a more generic selector
        if len(articles) < 5:
            articles = driver.find_elements(By.TAG_NAME, "articles.c-d")

        if len(articles) ==0:
            raise Exception("No articles found.")

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

            #Get article titles
            try:
                title = article.find_element(By.XPATH, ".//h2").text.strip()
            except NoSuchElementException:
                title = ""

            # Translate to English
            #result = translate_client.translate(title, target_language="en")
            #translated = result["translatedText"]
            print("Title: ", title)

            #Save title to list
            translated_titles.append(title)

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
    # Go to El País Opinion section
    driver.get("https://elpais.com/opinion/")
    time.sleep(3)

    fetch_articles()

    # Count word frequency
    all_words = [word for title in translated_titles for word in re.findall(r'\b\w+\b', title.lower())]
    word_freq = Counter(all_words)

    # Print word frequency
    print("\n Word Frequency:")
    for word, count in word_freq.most_common():
        print(f"- {word}: {count}")

finally:
    driver.quit()
