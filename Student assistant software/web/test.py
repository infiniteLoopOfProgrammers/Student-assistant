import sys
import os

# Process the image here
result = 'This is the result of processing the image'

with open('output.txt', 'w') as f:
    f.write(result)

print(os.path.join(os.getcwd(), 'output.txt'))