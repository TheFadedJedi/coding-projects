#Combining two or more strings
str1="Hello"
str2=" World"
result=(str1+str2)
print(result)
#Repeating a string multiple times
text="Repeat me "
result=(text*3)
print(result)
#Finding the length of a string.
text = "This is a sample string."
length = len(text)
print(length)
#Accessing individual characters by their index.
text = "Python"
first_char = text[0] 
print(first_char)
#Extracting a portion of a string.
text = "Python is great"
substring = text[7:9] 
print(substring)
#Using negative indices to access characters from the end.
text = "Python is fun"
last_char = text[-1] 
print(last_char)
#Utilizing built-in string methods for various operations like converting case, finding and replacing substrings, etc.
text = "Python is cool"
uppercase_text = text.upper() # Convert to uppercase
lowercase_text = text.lower() # Convert to lowercase
replaced_text = text.replace("cool", "awesome") # Replace "cool" with "awesome"
print(uppercase_text) # Output: "PYTHON IS COOL"
print(lowercase_text) # Output: "python is cool"
print(replaced_text) # Output: "Python is awesome"1
