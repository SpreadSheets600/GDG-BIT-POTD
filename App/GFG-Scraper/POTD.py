import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def init_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_div_content():
    url = "https://www.geeksforgeeks.org/problem-of-the-day/"
    driver = init_driver()

    driver.get(url)
    time.sleep(5)

    try:
        div = driver.find_element("id", "potdTourStep1")
        inner_html = div.get_attribute("innerHTML")

        soup = BeautifulSoup(inner_html, "html.parser")
        data = {}

        for element in soup.find_all(True):
            class_name = element.get("class", [])
            if class_name:
                class_name_str = " ".join(class_name)
                data[class_name_str] = element.get_text(strip=True)

        return data

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()
