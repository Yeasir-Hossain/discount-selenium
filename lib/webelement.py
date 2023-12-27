from .req import req

By = {
    'XPATH': 'xpath',
    'CLASS_NAME': 'css selector',
    'LINK': 'link text',
    'PARTIAL_LINK:': 'partial link text',
    'TAG': 'tag name'
}


class WebElement:
    def __init__(self, sessionId, elementId, host):
        """
        Initializes a WebElement instance.

        Args:
            sessionId (str): The session ID associated with the WebDriver session.
            elementId (str): The element ID associated with this WebElement.
            host (str): The host URL of the WebDriver server.
            headers (dict): HTTP headers to be included in the requests.
        """
        self.sessionId = sessionId
        self.elementId = elementId
        self.host = host

    def click(self) -> None:
        """
        Simulates a mouse click on the WebElement.
        """
        req(f"{self.host}/session/{self.sessionId}/element/{self.elementId}/click",
            method='post', json={})

    def sendKeys(self, value) -> None:
        """
        Enters the specified text into the WebElement.

        Args:
            value (str): The text to be entered into the WebElement.
        """
        req(f"{self.host}/session/{self.sessionId}/element/{self.elementId}/value", method='post',
            json={
                "text": value
            })

    def clear(self) -> None:
        """
        Clears the text content of the WebElement.
        """
        req(f"{self.host}/session/{self.sessionId}/element/{self.elementId}/clear",
            method='post', json={})

    def isSelected(self):
        """
        Checks if the WebElement is selected.

        Returns:
            dict: The server response indicating whether the element is selected.
        """
        return req(f"{self.host}/session/{self.sessionId}/element/{self.elementId}/selected")

    def isEnabled(self):
        """
        Checks if the WebElement is enabled.

        Returns:
            dict: The server response indicating whether the element is enabled.
        """
        return req(f"{self.host}/session/{self.sessionId}/element/{self.elementId}/enabled")

    def getAttribute(self, name):
        """
        Gets the value of the specified attribute of the WebElement.

        Args:
            name (str): The name of the attribute.

        Returns:
            dict: The server response containing the attribute value.
        """
        return req(f"{self.host}/session/{self.sessionId}/element/{self.elementId}/attribute/{name}")

    def getProperty(self, name):
        """
        Gets the value of the specified property of the WebElement.

        Args:
            name (str): The name of the property.

        Returns:
            dict: The server response containing the property value.
        """
        return req(f"{self.host}/session/{self.sessionId}/element/{self.elementId}/property/{name}")

    def getText(self):
        """
        Gets the text content of the WebElement.

        Returns:
            dict: The server response containing the text content.
        """
        return req(f"{self.host}/session/{self.sessionId}/element/{self.elementId}/text")

    def getTagName(self):
        """
        Gets the tag name of the WebElement.

        Returns:
            dict: The server response containing the tag name.
        """
        return req(f"{self.host}/session/{self.sessionId}/element/{self.elementId}/name")
