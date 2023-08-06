print("You are using Greendeck Proxygrabber library!")

# your package information
name = "greendeck_proxygrabber"
__version__ = "0.0.5"
author = "Gagan Singh"
author_email = "gaganpreet.gs007@gmail.com"
url = ""

# import sub packages
from .src.proxygrabber.proxygrabber import ProxyGrabber
from .src.proxygrabber.country_proxy_grabber import proxy_scraper
from .src.proxygrabber.proxychecker import ProxyChecker