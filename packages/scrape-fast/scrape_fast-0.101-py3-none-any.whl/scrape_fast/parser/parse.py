

def get_element_content(soup, tag, output='t', key=None, attribute=None):
    """
    Extract text from html element
    :param soup: BeautifulSoup object
    :param tag: String with html tag name
    :param output: String defining returned format, t if text, k for key defined by key param
    :param key: Key for element attribute
    :param attribute: dictionary with html attribute info
    :return: String content of element or None if does not find it
    """
    if attribute is None:
        attribute = {}
    element = soup.find(tag, attribute)
    if element:
        return define_output(element, output, key)
    return None


def define_output(element, output, key=None):
    """
    Defines get_element_content output
    :param element: soup html tag
    :param output: String defining returned format
    :param key: Key for element attribute
    :return: Element content or None
    """
    options = {
        't': element.text.strip(),
        'k': element[key] if element.has_attr(key) else None
    }
    return options[output]
