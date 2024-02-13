from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

url = 'https://www.partnerbase.com/invisionapp'

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the URL
driver.get(url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__nuxt"]/div/div[1]/nav/div/div[1]/a[2]')))
# Wait for the page to load and the table to be present


coci = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
time.sleep(2)
coci.click()
time.sleep(2)



# Find all rows in the table
while True:
    try:
        scrollable_container = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div[1]/nav/div/div[1]/a[2]')

        # Find the element you want to scroll to within the container
        element_to_scroll_to = driver.find_element(By.XPATH, '//*[@id="partners"]/section[2]/div[2]/div[2]/button[1]')
        # Scroll the container to make the element visible
        driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop;", scrollable_container, element_to_scroll_to)
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="partners"]/section[2]/div[2]/div[2]/button[1]')))
        # Perform any additional actions with the element
        element_to_scroll_to.click()
    except:
        break

time.sleep(5)
driver.execute_script("window.scrollTo(0, 0);")
driver.execute_script("window.scrollBy(0, 1100);")
time.sleep(5)
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="partners"]/section[2]/div[2]/table/tbody')))
rows = table.find_elements(By.CSS_SELECTOR, 'tr')
time.sleep(2)

info_list = []
# Iterate through each row and click the expand button
for row in rows:
    print(len(rows))
    company_name = row.find_element(By.CSS_SELECTOR, 'div.flex.flex-col').text
    partner_type = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text
    row.click()
    time.sleep(2)

    expanded_content = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@class="details-row details-row--active"]'))
    )

    employee_num = expanded_content.find_element(By.CSS_SELECTOR, 'p').text
    description = expanded_content.find_element(By.CSS_SELECTOR, 'div.flex.gap-20').text
    driver.execute_script("window.scrollBy(0, 500);")
    company_page = expanded_content.find_element(By.XPATH, '//a[@class="o-button__primary py-[12px]"]')
    company_page.send_keys(Keys.CONTROL + Keys.RETURN)
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    company_url = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__nuxt"]/div/div[1]/main/div/div[1]/section/div[3]/section[1]/div[2]/nav/div/a[1]'))).get_attribute('href')
    print(company_url)
    
    info_dict = {'Partner name': company_name.replace('View Company'),
                 'Partner URL': company_url,
                 'Number Employees': employee_num,
                 'Company Description': description,
                 'Partner Type (Technology or Channel)': partner_type
                 }
    driver.close()

    # Switch back to the original tab (if needed)
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(3)
    info_list.append(info_dict)

df = pd.DataFrame(info_list)
print(df)
df.to_excel('data.xlsx', index=False)

# Close the browser
driver.quit()

