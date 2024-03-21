import random
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

# Function to read proxy list from file and get a random proxy
def get_random_url():
    with open('core/library.txt', 'r') as file:
        url = file.read().splitlines()

    return random.choice(url)

def generate_random_number():
    with open('core/random_delay_time.txt', 'r') as file:
        randNumber = file.read().splitlines()

    return random.choice(randNumber)

def get_random_proxy():
    # URL to fetch data from
    url = 'https://tq.lunaproxy.com/getflowip?neek=1219602&num=1&type=1&sep=1&regions=all&ip_si=2&level=1&sb='
    # Make a GET request to the URL
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Initialize an empty list to store lines
        lines = []
        
        # Read each line from the response content and store in the list
        for line_number, line in enumerate(response.iter_lines(), start=1):
            line = line.decode('utf-8')  # Decode bytes to string
            lines.append(line)
        
        # Split each line as needed
        split_lines = [line.split(',') for line in lines]
        
        return split_lines
    else:
        print(f"Failed to fetch data from URL. Status code: {response.status_code}")
        return []

def create_chrome_option_profile(agent, proxy, proxy_username, proxy_password):
    profile = webdriver.ChromeOptions()
    profile.add_argument('--disable-dev-shm-usage')
    profile.add_argument('--disable-extensions')
    profile.add_argument('--disable-gpu')
    profile.add_argument('--no-sandbox')
    # profile.add_argument('--headless')
    profile.page_load_strategy = 'none'
    profile.add_argument(f"--user-agent={agent}")

    # Set up SOCKS5 proxy
    f_proxy = f"{proxy}"
    profile.add_argument(f'--proxy-server=socks5://{f_proxy}')
    encoded_auth = f'{proxy_username}:{proxy_password}'
    profile.add_argument(f'--proxy-auth={encoded_auth}')

    return profile

# Function to make a request with a random user agent and proxy
def core_engine(iteration, proxy):
    user_agent  = get_random_user_agent()
    url         = get_random_url()
    
    options = create_chrome_option_profile(user_agent, proxy, "user-lu8652689", "6EIarx")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url) 

    # Implicit wait for elements to be found
    driver.implicitly_wait(30)

    # Wait for the page to be fully loaded
    wait = WebDriverWait(driver, 50)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))


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
    print(f"+ Sleep: {random_time_sleep} | PROXY: {proxy} | Delay Transition: {random_delay_scroll} | Time: {datetime.now()}")
    print(f"+=============================================================\n")
    
num_requests = int(input("Enter the visitor number: "))

# Make multiple requests
for iteration in range(1, num_requests + 1):
    core_engine(iteration, get_random_proxy()[0][0])
