from POTD import *

result = get_div_content("potdTourStep1")

if "error" in result:
    print(f"An error occurred: {result['error']}")
else:
    print("Contents of div:")
    print(result["class"])
    print("\nFull inner content:")
    print(result["inner_html"])
