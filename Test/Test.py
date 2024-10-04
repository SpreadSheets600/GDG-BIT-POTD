import requests
from bs4 import BeautifulSoup

# URL of the GeeksforGeeks Problem of the Day page
url = "https://www.geeksforgeeks.org/problem-of-the-day"

# Fetch the page content
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all divs with the specified attribute
divs = soup.find_all("div")

# Print the entire div(s)
if divs:
    for div in divs:
        print(div.prettify())

    with open("output.html", "w") as file:
        file.write(str(divs))
else:
    print("No divs found with the attribute 'bis_skin_checked=\"1\"'.")
