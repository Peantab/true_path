# -*- coding: utf-8 -*-
import true_path
import re  # For regex
import requests  # For checking certificate
from bs4 import BeautifulSoup
import os
import inspect  # For getting module's location

error = "\033[91mERROR\033[0m"


def safe_url(address, verbose=False):
    """
    Tests whether URL itself looks safe.

    :param address: the whole address copy-pasted, along with a protocol.
    :param verbose: if set to True, additional message about check
    is being printed on standard out.
    :return: boolean – True means the address looks safe
    """
    tester = re.compile(
        r"^https://[.0-9A-Za-z]+(/[#0-9A-Za-z.,\-_~!?$%&'()*+;=:@]*)*$")
    # r for raw string notation (not escaping /)
    # weird symbols only after / after domain
    match = tester.fullmatch(address)
    if match is not None:
        result = True
    else:
        result = False
    if verbose:
        print("***Safe URL check: " + print_result(result) + "***")
        print("The path is considered safe if it begins with \"https://\""
              " denoting a secured connection, does not contain tricky"
              " characters (no greek letters similar to latin,"
              " no unicode characters, no control sequences) "
              "and only contains @ after slash after domain address.")

    return result


def safe_certificate(address, verbose=False):
    """
    Tests whether website has a valid SSL certificate.

    :param address: the whole address copy-pasted, along with a protocol.
    :param verbose: if set to True, additional message about check
    is being printed on standard out.
    :return: boolean – True means the certificate seems OK (which guarantees
    nothing nowadays), False means either the test failed
    or could not have been performed.
    """
    ssl_declared = re.match("^https://", address)
    if ssl_declared is None:
        result = False
    else:
        try:
            requests.get(address)
            result = True
        except requests.exceptions.SSLError:
            result = False

    if verbose:
        print("***Certificate check: " + print_result(result) + "***")
        print("Checks whether a website declares using HTTPS and whether it "
              "indeed present a valid SSL certificate.")
        print("If you believe that this test definitely should have passed "
              "but it didn't (or the opposite), please update "
              "your Requests library.")

    return result


def popular_site(address, verbose=False):
    """
    Checks whether the page is popular enough (in Bing's view)
    It's unlikely your bank's login page if you are the first person ever
    to visit it.

    :param address: the whole address copy-pasted, along with a protocol.
    :param verbose: if set to True, additional message about check
    is being printed on standard out.
    :return: boolean – True means the page was high enough on Bing's result
    page, False means either the test failed or could not have been performed.
    False negative also possible if one page is available from different URLs.
    """

    try:
        requested = requests.get(address)
    except requests.exceptions.MissingSchema:
        print(error + ": Invalid address – it was supposed to be in form "
                      "protocol://www.domain.tld/something")
        return False

    # Get title of the website
    title = BeautifulSoup(requested.text, 'html.parser').title.string
    title = title.lower()

    # Get addresses of 5 first search results of title in Bing
    bing_request = requests.get("http://www.bing.com/search",
                                params={"q": title})
    binged = BeautifulSoup(bing_request.text, 'html.parser')
    binged = binged.find_all("li", "b_algo")
    binged = binged[:5]
    binged = list(map(lambda x: x.a.get("href"), binged))

    # Cut the address so it was only a domain address.
    address_cut = re.match("^https://.*?/", address)
    try:
        address_cut = address_cut.group()[:-1]
    except AttributeError:  # Given address has no slash after domain address
        address_cut = address+"/"  # ...so we match against it all + "/"
        # for protection against TLDs being a prefix of popular domain.
    address_re = re.compile("^"+address_cut)

    # Check whether given address is on a list
    result = False
    for link in binged:
        if address_re.match(link) is not None:
            result = True
            break

    if verbose:
        print("***Popularity check: " + print_result(result) + "***")
        print("Checks whether the page is popular enough (in Bing's view)."
              "It's unlikely your bank's login page if you are the first"
              " person ever to visit it.")
        print("False negative is possible if one page is available"
              "from different URLs.")

    return result


def google_safe_browsing(address, verbose=False):
    """
    Check whether the page is not on one of the Google's unsafe pages lists
    via Google Safe Browsing API.

    :param address: the whole address copy-pasted, along with a protocol.
    :param verbose: if set to True, additional message about check
    is being printed on standard out.
    :return: boolean - it's True if and only if the page is NOT on a Google's
    blacklist
    """
    # Get the key
    api = "https://safebrowsing.googleapis.com/v4/"
    google_api_key = None
    try:
        with open(os.path.join(os.path.dirname(inspect.getfile(true_path)),
                               "api_key")) as key_source:
            google_api_key = key_source.read()
    except FileNotFoundError:
        pass

    if google_api_key is None:
        print(error + ": Valid Google Safe Search API key required in file "
              "api_key in folder where package's python files are located.")
        return False

    # Get and process available threat lists
    threat_lists = requests.get(api+"threatLists",
                                params={"key": google_api_key})
    # Inform if checking is impossible
    if threat_lists.status_code != 200:
        print(error + " – invalid response's status code: ",
              str(threat_lists.status_code))
        return False
    threat_lists = threat_lists.json()['threatLists']
    threat_types = frozenset(map(lambda x: x['threatType'], threat_lists))
    threat_platform_types = frozenset(map(lambda x: x['platformType'],
                                          threat_lists))

    # Prepare a request
    request_data = {'client':
                    {'clientId': 'truepathpt', 'clientVersion': '0.1.0'},
                    'threatInfo':
                        {'threatTypes': list(threat_types),
                         'platformTypes': list(threat_platform_types),
                         'threatEntryTypes': ['URL'],
                         'threatEntries':
                             [{'url': address}]}}
    response = requests.post(api+"threatMatches:find",
                             params={"key": google_api_key}, json=request_data)

    # Analyze a response
    if response.status_code != 200:
        print(error + " – invalid response's status code: ",
              str(response.status_code))
        return False
    result = True if len(response.json()) == 0 else False

    if verbose:
        print("***Google Safe Browsing check: " + print_result(result) + "***")
        print("Check whether the page is not on one of the Google's unsafe "
              "pages lists via Google Safe Search API")
        print("It's passed if and only if the page is NOT on a Google's "
              "blacklist (if check fails to complete, it's considered "
              "a failure")

    return result


def suite(address, verbose=False):
    """
    Simply runs remaining checks, with `verbose` set to False
    :param address: will be provided to other checks as an `address` parameter.
    :param verbose: Short or long output version
    :return: If any check fails, the return value will be False.
    """
    safe_url_result = safe_url(address, verbose)
    safe_certificate_result = safe_certificate(address, verbose)
    popular_site_result = popular_site(address, verbose)
    google_safe_browsing_result = google_safe_browsing(address, verbose)

    if not verbose:
        print("Safe URL check: " + print_result(safe_url_result))
        print("Certificate check: " + print_result(safe_certificate_result))
        print("Popularity check: " + print_result(popular_site_result))
        print("Google Safe Browsing check: " +
              print_result(google_safe_browsing_result))

    return safe_url_result and safe_certificate_result \
        and popular_site_result and google_safe_browsing_result


def print_result(x):
    return "\033[94mPassed\033[0m" if x else "\033[91mFAILED\033[0m"
