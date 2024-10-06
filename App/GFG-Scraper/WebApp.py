import time
from bs4 import BeautifulSoup
from selenium import webdriver
from flask import Flask, jsonify
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
    time.sleep(5)  # Wait for the page to load

    try:
        div = driver.find_element("id", "potdTourStep1")
        inner_html = div.get_attribute("innerHTML")
        return {"inner_html": inner_html}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()


app = Flask(__name__)


def extract_data(html):
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    for element in soup.find_all(True):

        key = element.name

        if element.get("class"):
            key += f".{' '.join(element['class'])}"
        if element.get("id"):
            key += f"#{element['id']}"

        if key in data:
            counter = 1
            while f"{key}_{counter}" in data:
                counter += 1
            key = f"{key}_{counter}"

        data[key] = element.get_text(strip=True)

    return data


@app.route("/get-potd-content", methods=["GET"])
def fetch_potd_content():
    result = get_div_content()

    if "error" in result:
        return jsonify({"error": result["error"]}), 500

    extracted_data = extract_data(result["inner_html"])

    return jsonify(extracted_data)


if __name__ == "__main__":
    app.run(debug=True)
