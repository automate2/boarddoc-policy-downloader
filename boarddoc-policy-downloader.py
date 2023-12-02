import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from pathvalidate import ValidationError, validate_filename, sanitize_filename
from os.path import exists
import urllib.request

def save_file(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved file: {file_name}")

def process_policy_link(link):
    # 1A. Get the text of the link, which will be used as the file name
    policy_name = link.text.strip().replace('\n',' ')
    policy_name = sanitize_filename(policy_name)
    file_name = policy_name+".html"
    policy_exists = exists(file_name)
    if not policy_exists:
        # 2A. Click on the link to view the policy item
        try:
            link.click()
            print("clicking policy " + policy_name)
            time.sleep(1)
            # 3A. Get the inner text of the element with the ID 'view-policy-item' to use as the body of the file
            view_policy_item = driver.find_element(By.ID, 'view-policy-item')          
            content = view_policy_item.get_attribute('innerText')

            # Save the file with the name from 1A and content from 3A
            save_file(f"{file_name}", content)
            
            # find and save attachments
            attachments = driver.find_elements(By.XPATH, '//a[contains(@href, ".pdf") or contains(@href, ".doc")]')
            if len(attachments)>0:
                print("found attachment(s)")
                for file_link in attachments:
                    try:
                        url_path = file_link.get_attribute('href');
                        print("opening file at url:"+url_path)
                        split_path = url_path.split('/')
                        response = urllib.request.urlopen(url_path)
                        file_name_only = split_path[len(split_path)-1]
                        file_name_only = sanitize_filename(file_name_only)
                        file_name_only = file_name_only.replace("%20", " ")
                        print("saving file named "+file_name_only)
                        file = open(file_name_only, 'wb')
                        file.write(response.read())
                    except Exception as e: 
                        print(e)
        except:
            pass

def process_board_link(board_link):
    board_section = board_link.text.strip()
    board_link.click()
    print("getting policies for"+board_section)
    time.sleep(1);
    # 1. Identify all links with class "policy"
    policy_links = driver.find_elements(By.CLASS_NAME, 'policy')
    for policy_link in policy_links:
        # 2. Process each link
        process_policy_link(policy_link)

# This can be changed to be used on other board doc sites
url = 'http://www.boarddocs.com/wa/ksdwa/Board.nsf/Public'
driver = webdriver.Chrome()  # You need to have ChromeDriver installed and in your PATH
print("opening chrome")
time.sleep(3)
#wait = WebDriverWait(driver, 10)  # Adjust the waiting time as needed

# Navigate to the URL
driver.get(url)
print("opening ksd page")
time.sleep(6)
# this is the xpath to get the policies
policy_main = driver.find_element(By.XPATH, "//*[@id='ui-id-5']")
policy_main.click()
print("clicking policies")
time.sleep(6)

# find list of top category items
print("getting board menu items")
boardmenu_links = driver.find_elements(By.XPATH, "//a[@class='lefMenu' and @tabindex='-1']")
for cat_link in boardmenu_links:
    process_board_link(cat_link)

# Close the browser when done
driver.quit()
