import re
import urllib
import requests

def raise_detailed_error(request_object):
    """Get details on http errors.

    Args:
        request_object (json): Json response data.

    Raises:
        requests.exceptions.HTTPError: HTTP error
    """
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)
    except requests.exceptions.Timeout as error:
        raise requests.exceptions.Timeout("The request timed out")
    except requests.exceptions.ConnectionError as error:
        raise requests.exceptions.ConnectionError(error, request_object.text)

def clean_event_data(data):
    """Cleaning missing data from event API.

    Args:
        data (dict): json data of the event.

    Returns:
        dict: the cleaned data.
    """
    if 'currentScore' in data:
        pass
    else: 
        data['currentScore'] = 0
    
    if 'description' in data:
        pass
    else: 
        data['description'] = "No Description"
    
    if 'node' in data:
        pass
    else: 
        data['node'] = "No Data"
    return data


def encode_identifier(identifier, is_unique=False):
    """
    Encode an identifier for use in URLs.

    Args:
        identifier (str): The identifier to be encoded.
        is_unique (bool, optional): Whether to use a unique identifier format. Defaults to False.

    Returns:
        str: The encoded identifier.
    """
    if is_unique:
        parts = identifier.split("/")
        identifier = "/".join(parts[-3:]) if len(parts) >= 3 else parts[-1]
    else:
        identifier = identifier.replace(" and ", " & ")
        identifier = re.sub(r'\s*\(.*?\)', '', identifier)

    return urllib.parse.quote(identifier,safe="&")
