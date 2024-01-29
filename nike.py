from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import datetime
import time

# Create a new instance of the Chrome driver
print("start time = ", datetime.datetime.now())
print('timestamp = ', datetime.datetime.now().timestamp())
driver = webdriver.Chrome()
driver.maximize_window()


# Open the URL in the Chrome browser
# url = 'https://www.adidas.com/us/fleece-hoodie/S97480.html'
# url = 'https://www.adidas.com/us/ultraboost-1.0-shoes/HQ4200.html'

driver.get(url)

# open reviw accordian
button_xpath = '/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div[1]/div[3]/section[1]/div/div/button'  # Replace with the actual XPath of your button

button = driver.find_element("xpath", button_xpath)
button.click()

flag = True
load_more_button_click_count = 0
time.sleep(10)
while flag:
    try:
        button = driver.find_element(By.CLASS_NAME, 'read-more-button___Ndo_p')
        if button:
            button.click()
            load_more_button_click_count = load_more_button_click_count + 1
            print(f'Load more button click count = {load_more_button_click_count}')
            time.sleep(5)
    except Exception as e:
        # print("Exception occured")
        flag = False

        
# get all review container innerHTML
review_container = 'ratings-reviews-layout___1a6RC'
container = driver.find_element(By.CLASS_NAME, review_container)


# source HTML OF comments container

source = container.get_attribute("innerHTML")
soup = BeautifulSoup(source, 'html.parser')
all_comment_divs = soup.select('.review___KFNQH')
# print(len(all_comment_divs))
all_data = []
for comment in all_comment_divs:
    user = comment.select('.user-name___2Ra0t')
    # print(f"username = {user[0].contents}")
    review_title_and_date = comment.select('.review-title___lx1nb')
    review_title = review_title_and_date[0].select('.title___2hZnM')
    # print(f"review title = {review_title[0].contents}")
    review_date = review_title_and_date[0].select('.date___1Ikvn')
    # print(f"review date = {review_date[0].contents}")
    review_description = comment.select('.text___uiKSX')
    # print(f"review text = {review_description[0].contents}")

    comment_star_div = comment.select('.gl-star-rating__mask')
    rating = 0
    for star_div in comment_star_div:
        rating_style_width = star_div['style']
        if rating_style_width == 'width: 88%;':
            rating = rating + 1
        else:
            break
    all_data.append({
        "username": user[0].contents[0],
        "date": review_date[0].contents[0],
        "title": review_title[0].contents[0],
        "description": review_description[0].contents[0],
        "rating": rating
    })

# print(all_data)

with open('output_rating_score.txt', "+a") as file:
    file.write(str(all_data)) 
# time.sleep(30)
driver.quit()
print("end time = ", datetime.datetime.now())
print('timestamp = ', datetime.datetime.now().timestamp())