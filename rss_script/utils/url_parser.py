from urllib.parse import urlparse, urlunparse


def remove_query_params(url: str) -> str:
    """
    Removes the query parameters from a URL

    Args:
        url: The URL remove the query parameters from

    Returns:
        The URL with the query parameters removed
    """
    parsed_url = urlparse(url)
    cleaned_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, None, None, None))
    return cleaned_url
