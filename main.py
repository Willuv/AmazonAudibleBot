from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

#create an options instance
options = Options()

# disable auto close
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)

#set headless mode to true and set the window size
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')


#chromedriver currently doesn't have matching version for chrome
#SSL error will occur at the moment
web = 'https://www.audible.com/search'
path = "C:/Users/Uvlin/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Initialize the WebDriver with the service
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service,options=options)

# Open the website
driver.get(web)
# driver.maximize_window()

#find where all the books are stored
container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
#get each book and store them in a list
products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

#lists for audio book information
book_title = []
book_author = []
book_length = []


#loop through the list of audiobooks and obtain the specific info
for product in products:
    book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
    book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
    book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

driver.quit

#create the DataFrame
df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length':book_length})
df_books.to_csv('books.csv', index=False)