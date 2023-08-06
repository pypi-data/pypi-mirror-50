#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Signs a URL using a URL signing secret """

import hashlib
import hmac
import base64
import re

from urllib.parse import urlparse, quote_plus

GOOGLE_MAPS_API_KEY = "AIzaSyAofozPey7CK3iThCxs0-1bdTdVly1QBGw"
GOOGLE_MAPS_SECRET_KEY = "76XgR6vY7puGmmytCWb-t6uC18E="

def sign_url(input_url=None, secret=None):
    """ Sign a request URL with a URL signing secret.

    Usage:
    from urlsigner import sign_url

    signed_url = sign_url(input_url=my_url, secret=SECRET)

    Args:
    input_url - The URL to sign
    secret    - Your URL signing secret

    Returns:
    The signed request URL
    """

    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, url_to_sign.encode(), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode()


def get_center_from_address(address):
    center = quote_plus(re.sub(' +', ' ', address).strip())
    return center


def get_google_map_url(address="", gps_coordinates="", sizes=(300, 180), zoom=15):
    """
    Return an url to be called to get the static map (png) from the google API from an address or cgp coordinates.
    It uses GPS coordinate if available, otherwise the address will be used.
    """
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    href_base_url = "https://www.google.com/maps/search"
    try:
        if gps_coordinates and len(gps_coordinates) > 2:
            center = ",".join(re.split(';|:|,', gps_coordinates.replace(' ', ''))) + "&zoom=%d" % zoom
        else:
            center = get_center_from_address(address)
    except:
        center = get_center_from_address(address)
    # &maptype=hybrid | satellite |
    marker = "markers=color:red|%s" % center
    url = "%s?center=%s&%s&size=%dx%s&key=%s" % (base_url, center, marker, sizes[0], sizes[1], GOOGLE_MAPS_API_KEY)
    return sign_url(url, GOOGLE_MAPS_SECRET_KEY)
