from PIL import Image
from in3110_instapy.io import read_image, write_image
from in3110_instapy.python_filters import python_color2gray

# Load the image
filename = "/home/jobbe/IN3110-eyyubg/assignment3/test/rain.jpg"
image = read_image(filename)

# Convert the image to grayscale
gray_image = python_color2gray(image)

# Save the grayscale image
write_image(gray_image, "rain_grayscale2.jpg")