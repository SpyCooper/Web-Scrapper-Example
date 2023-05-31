# Web Scrapper Example
**NOTE: To run the program, you need to make a folder called 'categories' in the same location as crawler.py

## Project description
This is a program the goes through https://books.toscrape.com/ and finds all the books in every category and writes each books information into it's category's file.

The .txt files in the CategoriesExample folder on here are the results from me running the program that should show up in the categories folder after running crawler.py.

## To run the program
You only need to make sure the crawler.py program is downloaded and that a folder names categories folder is made (using the name 'categories').

The crawler.py then needs to be run with python. For windows, I used the powershell command 'python crawler.py' and then type 'y' when asked and the program will run.

All .txt will be created if they are not in the categories folder. If the .txt are in there, they will be overwritten when the crawler.py is run.
