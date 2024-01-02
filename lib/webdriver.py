import os
import subprocess
from .webelement import WebElement
from .errors import DriverServerStartException
import base64
from datetime import date
from .req import req
import atexit
import socket
import time
import signal


class WebDriver(object):
    def __init__(self, **args):
        """
        Initializes a new WebDriver instance.

        Args:
            **args (dict): Keyword arguments for configuration.
                'executablePath' (str): Path to the WebDriver executable.
        """
        self.host = 'http://127.0.0.1:4444'
        self.sessionId = ''
        if args.get('executablePath'):
            driverPath = args['executablePath']
        else:
            driverPath = os.path.join(os.getcwd(), 'chromedriver')
        try:
            self.ps = subprocess.Popen([driverPath, '--port=4444'], stdout=subprocess.DEVNULL)
            status = self.wait_for_webdriver('localhost', '4444')
            if not status:
                raise DriverServerStartException(
                    f"Could not start webdriver server: Error code: {self.ps.returncode}")

            # Close the server process on 'exit' signal
            atexit.register(self.handle_exit)
            signal.signal(signal.SIGINT, self.handle_exit)
            signal.signal(signal.SIGTERM, self.handle_exit)
            self.getSession()
            if (args.get('fullScreen') == True):
                self.fullScreen()
        except Exception as e:
            print(e)

    def wait_for_webdriver(self, host, port, timeout=60):
        """Wait for the webdriver to start"""
        start_time = time.time()
        end_time = start_time + timeout

        while time.time() < end_time:
            try:
                # Attempt to create a socket and connect to the specified host and port
                with socket.create_connection((host, port), timeout=1):
                    return True
            except (socket.error, socket.timeout):
                # Retry if the connection fails
                time.sleep(1)

        return False

    def handle_exit(self, *args):
        self.ps.kill()

    def getSession(self) -> None:
        """
        Establishes a new session with the WebDriver server.
        """
        data = {
            "capabilities": {
                "acceptInsecureCerts": True,
            },
        }
        res = req(url=f"{self.host}/session", method='post', json=data)
        self.sessionId = res.get('value').get('sessionId')

    def get(self, url: str) -> None:
        """
        Navigates to the specified URL in the current browser window.

        Args:
            url (str): The URL to navigate to.
        """
        req(url=f"{self.host}/session/{self.sessionId}/url",
            method='post', json={"url": url})

    def close(self) -> None:
        """
        Closes the current WebDriver session.
        """
        req(url=f"{self.host}/session/{self.sessionId}", method='delete')

    def fullScreen(self) -> None:
        """
        Maximizes the current browser window to full-screen.
        """
        res = req(f"{self.host}/session/{self.sessionId}/window/fullscreen",
                  method='post', json={}).get('value')
        req(url=f"{self.host}/session/{self.sessionId}/window/rect", method='post',
            json={"x": 0, "y": 0, "width": res["width"], "height": res["height"]})

    def windowHandles(self):
        """
        Returns a list of window handles for all open browser windows.
        """
        return req(f"{self.host}/session/{self.sessionId}/window/handles").get('value')

    def switchWindow(self, handle: str):
        """
        Switches focus to the specified browser window.

        Args:
            handle (str): The handle of the target window.
        """
        return req(f"{self.host}/session/{self.sessionId}/window", method='post', json={"handle": handle}).get('value')

    def newWindow(self):
        """
        Opens a new browser window and returns its handle.
        """
        return req(f"{self.host}/session/{self.sessionId}/window/new", method='post', json={}).get('value').get('handle')

    def closeCurrentWindow(self):
        """
        Closes the current browser window.
        """
        return req(f"{self.host}/session/{self.sessionId}/window", method='delete', json={})

    def getAllCookies(self):
        """
        Retrieves all cookies for the current browser session.
        """
        return req(f"{self.host}/session/{self.sessionId}/cookie",).get('value')

    def getCookie(self, name: str):
        """
        Retrieves the value of a specific cookie by name.

        Args:
            name (str): The name of the cookie.
        """
        return req(f"{self.host}/session/{self.sessionId}/cookie/{name}").get('value')

    def addCookie(self, options: dict):
        """
        Adds a new cookie to the current browser session.

        Args:
            options (dict): Cookie options (name, value, etc.).
        """
        return req(f"{self.host}/session/{self.sessionId}/cookie", method='post', json={'cookie': options})

    def delCookie(self, name: str):
        """
        Deletes a specific cookie by name.

        Args:
            name (str): The name of the cookie to delete.
        """
        return req(f"{self.host}/session/{self.sessionId}/cookie/{name}", method='delete')

    def delAllCookies(self):
        """
        Deletes all cookies for the current browser session.
        """
        return req(f"{self.host}/session/{self.sessionId}/cookie", method='delete')

    def takeScreenshot(self, path: str, fileName=f"{date.today()}.png"):
        """
        Take a screenshot of the current browser session.

        Args:
            path (str): The directory path where the screenshot will be saved.
            fileName (str): The name of the screenshot file.

        Raises:
            FileNotFoundError: If the specified path does not exist.
        """
        try:
            # Check if the path exists, create it if not
            if not os.path.exists(path):
                os.makedirs(path)

            res = req(
                f"{self.host}/session/{self.sessionId}/screenshot",).get('value')

            imgdata = base64.b64decode(res)
            with open(os.path.join(path, fileName+'.png'), 'wb') as f:
                f.write(imgdata)

        except Exception as e:
            print(e)

    def findElement(self, by: str, value):
        """
        Finds a single web element based on the specified strategy and value.

        Args:
            by (str): The strategy to locate the element (e.g., 'id', 'xpath').
            value: The value associated with the specified strategy.

        Returns:
            WebElement: An instance of the WebElement class representing the found element.
        """
        data = {
            "using": by,
            "value": value
        }
        res = req(f"{self.host}/session/{self.sessionId}/element",
                  method='post', json=data)
        return WebElement(self.sessionId, list(res.get('value').values())[0], self.host)

    def findElements(self, by: str, value):
        """
        Finds multiple web elements based on the specified strategy and value.

        Args:
            by (str): The strategy to locate the elements (e.g., 'id', 'xpath').
            value: The value associated with the specified strategy.

        Returns:
            list: A list of WebElement instances representing the found elements.
        """
        data = {
            "using": by,
            "value": value
        }
        res = req(
            f"{self.host}/session/{self.sessionId}/elements", method='post', json=data)
        elements = res.get('value')
        return [WebElement(self.sessionId, list(element.values())[0], self.host) for element in elements]

    def executeScript(self, script: str):
        """
        Execute a script in the browser.

        Args:
            script (str): The scri[pt that will run.
        """
        return req(f"{self.host}/session/{self.sessionId}/execute/sync", method='post', json={'script': script, 'args': []})
