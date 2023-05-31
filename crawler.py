from bs4 import BeautifulSoup
import requests

def findlinks():
    # gets the home page html for Books To Scrape
    homepage = requests.get('https://books.toscrape.com/').text
    soup = BeautifulSoup(homepage, 'lxml')

    # Finds the list of categories on the left side
    categories_list = soup.find('ul', class_='nav nav-list')
    categories = categories_list.find_all('li')
    
    # Sets the total books found to 0, this is used to match the total books on the website
    bookCount = 0

    # goes through every category in the list of categories
    for category in categories:
        # gets the name of every category and the link to each category
        category_page = category.find('a').get('href')
        category_page = 'https://books.toscrape.com/' + category_page

        # finds the category name and reduces it to a name that can be used for a file
        category_name = category.text.strip().replace('  ', '')

        # since the all books page is a category, it skips it
        if 'Books\n' not in category_name:
            # opens a file that it can read and write the books into with the name of the category in the categories folder
            with open(f'categories/{category_name}.txt', 'w', encoding="utf-8") as f:
                f.write('')
            f = open(f'categories/{category_name}.txt', 'r+', encoding="utf-8")

            # sets the total number of books in the category to 1
            book_index = 1

            # gets the html of the first category page
            category_html = requests.get(category_page).text
            soup2 = BeautifulSoup(category_html, 'lxml')

            # finds the list containing all the books on that page
            booksOnPage = soup2.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

            # goes through every book on the page
            for book in booksOnPage:
                # finds the name, price, availability, and link for the books on the page
                book_name = book.find('h3').text.replace('  ', '')
                book_name = book.article.h3.a['title']
                availability = book.find('p', class_='instock availability').text
                price = book.find('p', class_='price_color').text
                more_info = book.article.h3.a['href']
                more_info = 'https://books.toscrape.com/catalogue/' + more_info[9:]

                # writes the data for each book into the category file
                f.write(f'- {book_index} - \n')
                f.write(f'Book Name: {book_name.strip()}\n')
                f.write(f'Price: ${price[2:].strip()}\n')
                f.write(f'Availability: {availability.strip()}\n')
                f.write(f'Link: {more_info}\n')

                # increments the books in the category for each book
                book_index+=1

                #increments the total amount of books found
                bookCount+=1
            
            # checks to see if there is additional pages in the category
            pages = soup2.find('ul', class_='pager')
            if pages != None:
                # finds the link to the next page and the total number of pages
                page = pages.find_all('li')
                pageLim = page[0].text.strip()[-1]
                nextPage = page[1].a['href']
                nextPageLink = category_page[:-10] + nextPage
                pageLimNum = int(pageLim)

                # goes through until it hits 1 over the maximum number of pages for the category
                for pageNum in range(2, pageLimNum+1):
                    # gets the html for the next page
                    nextPageHTML = requests.get(nextPageLink).text
                    soup3 = BeautifulSoup(nextPageHTML, 'lxml')
                    pages = soup3.find('ul', class_='pager')

                    # finds all the books on the current page
                    booksOnPage = soup3.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
                    for book in booksOnPage:
                        # finds the name, price, availability, and link for the books on the page
                        book_name = book.find('h3').text.replace('  ', '')
                        book_name = book.article.h3.a['title']
                        availability = book.find('p', class_='instock availability').text
                        price = book.find('p', class_='price_color').text
                        more_info = book.article.h3.a['href']
                        more_info = 'https://books.toscrape.com/catalogue/' + more_info[9:]
                        
                        # writes the data for each book into the category file
                        f.write(f'- {book_index} - \n')
                        f.write(f'Book Name: {book_name.strip()}\n')
                        f.write(f'Price: ${price[2:].strip()}\n')
                        f.write(f'Availability: {availability.strip()}\n')
                        f.write(f'Link: {more_info}\n')

                        
                        # increments the books in the category for each book
                        book_index+=1

                        #increments the total amount of books found
                        bookCount+=1

                    # checks to see if it is on the last page
                    if len(pages) != None and pageNum != pageLimNum:
                        # gets the link ot the next page
                        page = pages.find_all('li')
                        nextPage = page[-1].a['href']
                        nextPageLink = category_page[:-10] + nextPage

            # prints that it completed the current category
            print('Completed', category_name, 'books...')
                        
            # closes the category text file
            f.close()
    
    # prints information about the run
    # the total number of books equals 1000, the amount of books on the website
    print('We found a total of', bookCount, 'books!')
    print('All books are in their respective files in the categories folder.')


# ---------------------------------- Main function ----------------------------------

# asks when to start the crawl
start = False
while start == False:
    input = input('Begin crawling (y/n)? ')
    if input == 'y':
        start = True

print('Beginning crawl...')
print('----------------------------------')

# runs the function to get the book links
findlinks()

print('Ending program...')
print('----------------------------------')