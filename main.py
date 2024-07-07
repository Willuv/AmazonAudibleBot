from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

#create an options instance
options = Options()

#set headless mode to true and set the window size
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')

#When chromedrive is updated this will be removed
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--disable-site-isolation-trials')
options.add_argument('--ignore-certificate-errors')

#chromedriver currently doesn't have matching version for chrome
#SSL error will occur at the moment
web = 'https://www.audible.com/adblbestsellers?ref_pageloadid=not_applicable&ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=334a4a9c-12d2-4c3f-aee6-ae0cbc6a1eb0&pf_rd_r=7S6T2VVAHDM6FNBNG8T6&pageLoadId=99Ge0Cf9WFHw2hLq&creativeId=7ba42fdf-1145-4990-b754-d2de428ba482'
path = "C:/Users/Uvlin/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Initialize the WebDriver with the service
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service,options=options)
driver.set_page_load_timeout(30)

# Open the website
driver.get(web)

#pagination
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME,'li')
last_page = int(pages[-2].text.strip())

#current page index
current_page = 1

#lists for audio book information
book_title = []
book_author = []
book_length = []

while current_page <= last_page:
    time.sleep(2)
    #find where all the books are stored
    container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
    #get each book and store them in a list
    products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')


    #loop through the list of audiobooks and obtain the specific info
    for product in products:
        try:
            title = product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text
            author = product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text
            length = product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text
            
            book_title.append(title)
            book_author.append(author)
            book_length.append(length)
        except Exception as e:
            print(f"Error processing product: {e}")

    current_page = current_page + 1

    try:
        #find where the button for the next page is and click it 
        next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

#create the DataFrame
df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length':book_length})
df_books.to_csv('books.csv', index=False)