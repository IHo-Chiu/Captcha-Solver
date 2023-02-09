
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random, string
import argparse
import os

url = "https://ebank.megabank.com.tw/nib/"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', default='images/')
    parser.add_argument('--num', default=100)
    args = parser.parse_args()
    
    folder = args.folder
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    
    options = Options()
    options.add_argument("--disable-notifications")

    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome.maximize_window()
    chrome.get(url)

    time.sleep(5)

    iteration = int(args.num)
    for i in range(iter):

        time.sleep(1)
        name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(20))
        path = os.path.join(folder, f'{name}.jpg')
        chrome.save_screenshot(path)

        refresh_button = chrome.find_element(By.CLASS_NAME, "refresh")
        refresh_button.click()

        if i % int(iteration/100) == 0:
            print(f'downloading ... {int(i/iteration*100)}%', end='\r')

    print('downloading ... done')
    
    

if __name__ == '__main__':
    main()