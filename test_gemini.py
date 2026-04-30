import google.generativeai as genai
import sys

print(dir(genai))
print("GenerativeModel __init__ flags:")
import inspect
print(inspect.signature(genai.GenerativeModel.__init__))
