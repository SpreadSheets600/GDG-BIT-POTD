from POTD import get_div_content
from flask import Flask, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)


def extract_data(html):
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    for element in soup.find_all(True):
        class_name = element.get("class", [])
        if class_name:
            class_name_str = " ".join(class_name)
            data[class_name_str] = element.get_text(strip=True)

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
