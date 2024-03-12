import random

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from datetime import datetime


def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

# Function to read proxy list from file and get a random proxy
def get_random_url():
    with open('core/library.txt', 'r') as file:
        proxies = file.read().splitlines()

    return random.choice(proxies)

def generate_random_number():
    with open('core/random_delay_time.txt', 'r') as file:
        randNumber = file.read().splitlines()

    return random.choice(randNumber)

# Function to make a request with a random user agent and proxy
def core_engine(iteration):
    user_agent  = get_random_user_agent()
    url         = get_random_url()

    headers = {
        'User-Agent': user_agent
    }
    
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.page_load_strategy = 'none'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url) 

    sleep(5)
    random_time_sleep = int(generate_random_number())
    sleep(random_time_sleep)
    random_delay_scroll = int(generate_random_number()) * 0.01

    # # Function to perform smooth scroll
    def smooth_scroll():
        # Get the height of the document
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        
        # Set the initial position and step size for scrolling
        position = 0
        step = 50
        
        # Scroll to the bottom gradually
        while position < scroll_height:
            # Check if scrolled to the bottom
            if position >= scroll_height:
                break

            driver.execute_script(f"window.scrollTo(0, {position});")
            position += step

            sleep(random_delay_scroll)  # Adjust sleep time for desired smoothness

    smooth_scroll()

    print(f"+=============================================================")
    print(f"+ Iteration {iteration} success with AGENT: {user_agent}")
    print(f"+ Destination Address: {url}")
    print(f"+ Sleep: {random_time_sleep} | Delay Transition: {random_delay_scroll} | Time: {datetime.now()}")
    print(f"+=============================================================\n")
    
num_requests = int(input("Enter the visitor number: "))

# Make multiple requests
for iteration in range(1, num_requests + 1):
    core_engine(iteration)
