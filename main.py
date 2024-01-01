import os
from time import sleep
from lib.webdriver import WebDriver
from lib.webelement import By


def main():
    url = 'https://www.google.com/'
    driver = WebDriver(executablePath=os.path.join(
        os.getcwd(), 'chromedriver'))
    try:
        driver.get(url)
        sleep(10)
        element = driver.findElement(By['XPATH'], '//input[@name="q"]')
        element.sendKeys('Raiyaan Yeasin')
        driver.addCookie({})
        driver.switchWindow('parent')
        driver.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
