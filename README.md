# WebDriver API Wrapper

The **WebDriver API Wrapper** is a Python library designed to provide a simplified interface for interacting with web browsers using the WebDriver protocol. The project aims to encapsulate the functionalities of Selenium WebDriver by utilizing HTTP requests to a WebDriver server.

## Features

1. **Initialization and Configuration:**
   - Initialize a new WebDriver instance with optional configurations.
   - Specify the path to the WebDriver executable or use the default path (chromedriver).

2. **Session Management:**
   - Establish a new session with the WebDriver server.
   - Close the current WebDriver session.

3. **Navigation:**
   - Navigate to a specified URL.
   - Retrieve a list of window handles for all open browser windows.
   - Switch focus to a specified browser window.
   - Open a new browser window.

4. **Window Handling:**
   - Close the current browser window.

5. **Cookie Management:**
   - Retrieve all cookies for the current browser session.
   - Retrieve the value of a specific cookie by name.
   - Add a new cookie to the current browser session.
   - Delete a specific cookie by name.
   - Delete all cookies for the current browser session.

6. **Screenshot Capture:**
   - Capture a screenshot of the current browser session.
   - Save the screenshot to a specified directory with an optional file name.

7. **Element Location:**
   - Find a single web element based on the specified strategy and value.
   - Find multiple web elements based on the specified strategy and value.

8. **Script Execution:**
   - Execute a script in the browser.


# Example Usage
```
driver = WebDriver(executablePath='path/to/chromedriver')
driver.get('https://example.com')
element = driver.findElement('id', 'username')
element.sendKeys('user123')
driver.takeScreenshot('screenshots', 'example_screenshot')
driver.close()

```


# Contribution

Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request.