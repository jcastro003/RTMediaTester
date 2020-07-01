import os
import urllib.request
import urllib
import urllib.error
import urllib.response

def internet_on():
    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        x = 'True'
    except urllib.error.URLError as err: 
        x = 'False'

    return x


print (internet_on())



