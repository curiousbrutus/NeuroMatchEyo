#import the module
import requests

# grabbing the content of https://en.wikipedia.org/wiki/URL
resp = requests.get("https://en.wikipedia.org/wiki/Medes")

# get() method returns a response object
print(resp.text)