from datetime import datetime, timezone
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

def calculate_percentage_time(start:str,end:str) -> float:
    """Calculate time percentage base on start, end time.

    Args:
        start (string): Start timestamp string.
        end (string): End timestamp string.

    Returns:
        float: calculated percentage completed.
    """
    target_time = datetime.fromisoformat(end.replace("Z", "+00:00"))
    # Current time in UTC
    current_time = datetime.now(timezone.utc)
    # Calculate percentage
    start_time = datetime.fromisoformat(start.replace("Z", "+00:00"))  # Arbitrary start point
    elapsed_time = (current_time - start_time).total_seconds()
    total_time = (target_time - start_time).total_seconds()
    percentage_completed = (elapsed_time / total_time)
    return percentage_completed

def format_timedelta(delta, day=True):
    """
    Extract hours, minutes, and optionally days from a timedelta object.

    Args:
        delta (timedelta): Time period.
        day (bool, optional): Whether to include days in the output. Defaults to True.

    Returns:
        str: Formatted time message.
    """
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(abs(total_seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes = divmod(remainder, 60)[0]
    message = (
        f"{days}d, {hours}h, {minutes}m"
        if day else
        f"{hours}h:{minutes}m"
    )

    return message + " ago" if total_seconds < 0 else message