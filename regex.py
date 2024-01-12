# Lab 3   Problems 

# Q1) Extract email ids from twitter tweets  

Given a text block like a tweet - write a python function which will read that text and return email ids from the tweet


Try with 

text = "Welcome to the  phoenix tours and travels you can email your feedback here at phoenixcares@redwings.com or call us at 001-1234568"


import re
def findEmail(tweet):
    matches = re.findall(r'\b[A-Za-z0-9_.+%-]+@[A-Za-z0-9.-]+\.[a-z]{2,}\b', tweet) #Findall instead of search as search only returns once
    return matches

text = "Welcome to the  phoenix tours and travels you can email your feedback here at phoenixcares@redwings.com, plaksha@edu.co.in or call us at 001-1234568"
print(findEmail(text))
# Q2)  Phone number extraction

Extract ISD phone numbers in the format +91 9999998888. OR (+91) 99998888 OR 0091 99998888

from any given text 

Create your own text block and try this 


# Method1 brute force approach: giving putting condition on first two as +91 or (+91) or 0091 and then inside loop of rest as numbers
# re.findall(r'+91|(+91)|0091', text)
# match = re.findall(r'[+(0][0-9]{10}', number) Try using conditionals
def phoneNumberextract(number):
    match = re.findall(r'(?:\+91|0091|\(\+91\))([ ][0-9]{10})', number)
    return match
text = "Hello here is my number 00919458214608 0091 +91 (+91) 919458214608 +91 9999998888. OR (+91) 99998888 OR 0091 99998888"
print(phoneNumberextract(text))
# Q3  Password Strength Checker 

**Problem Statement**

Write a function that checks the strength of a password based on the following criteria: at least 10 characters long, contains both uppercase and lowercase letters, contains at least one digit, and contains at least one special character  (!@#$%^&*).
# Brute force appraoch of checking individual constraints.
def passStrengthChecker(text):
    if len(text)>=10 and re.search('[A-Z]', text) and re.search('[a-z]', text) and re.search('[0-9]', text) and re.search('[!@#$%^&*]', text):
        return "Strong Password"
    else:
        return "Bad Password"

text = "dDyhuj2dd!"
print(passStrengthChecker(text)) #re.search checks for bool values
## Q4)  Extracting Hashtags from Social Media Text

**Problem Statement**

Write a function that extracts all hashtags from a given social media text. 
Hashtags start with the '#' symbol and may contain alphanumeric characters, underscores, and hyphens.
def allhashes(text):
    hash = re.findall(r'#[A-Za-z_-]+', text)
    return hash

text = "Hope you all like my pic. #Travel #Tour #Future # Programming, #Wanderlust"
text2 = "NO hashes statement"
print("Number of hashes", len(allhashes(text)))
print(allhashes(text))
