#coding: utf-8
from hashlib import sha1
from hmac import new as hmac
from xml.etree import ElementTree
import math
import os
import random
import requests
import datetime


URL = 'https://www.phpcaptcha.org/try-securimage/'
SECRET = 'UA-372036-5'


class RequestTimeout(Exception):
    pass

class InvalidResponse(Exception):
    pass

class Pula_Captcha(object):

    """
    def __init__(self, proxy_address=None, proxy_port=None, timeout=None):
        """
        SINESP only accepts national web requests. If you don't have a valid
        Brazilian IP address you could use a web proxy (SOCKS5).
        """
        self._proxies = None
        if proxy_address and proxy_port:
            self._proxies = {"https": "https://%s:%s" % (
                proxy_address, proxy_port)}

        # Read and store XML template for our HTTP request body.
        body_file = open(os.path.join(os.path.dirname(__file__), 'body.xml'))
        self._body_template = body_file.read()
        body_file.close()
        self._timeout = timeout


    def _token(self, plate):
        """Generates SHA1 token as HEX based on specified and secret key."""
        plate_and_secret = '%s%s' % (plate, SECRET)
        plate_and_secret = bytes(plate_and_secret.encode('utf-8'))
        plate = plate.encode('utf-8')
        hmac_key = hmac(plate_and_secret)
        return hmac_key.hexdigest()


    def _rand_coordinate(self, radius=2000):
        """Generates random seed for latitude and longitude coordinates."""
        seed = radius/111000.0 * math.sqrt(random.random())
        seed = seed * math.sin(2 * 3.141592654 * random.random())
        return seed


    def _rand_latitude(self):
        """Generates random latitude."""
        return '%.7f' % (self._rand_coordinate() - 38.5290245)


    def _rand_longitude(self):
        """Generates random longitude."""
        return '%.7f' % (self._rand_coordinate() - 3.7506985)

    def _date(self):
        """Returns the current date formatted as yyyy-MM-dd HH:mm:ss"""
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    def _body(self, plate):
        """Populate XML request body with specific data."""
        token = self._token(plate)
        latitude = self._rand_latitude()
        longitude = self._rand_longitude()
        date = self._date()
        return self._body_template % (latitude, token, longitude, date)

    def _captcha_cookie(self):
        """Performs a captcha request and return the cookie."""
        cookies = requests.get('https://www.phpcaptcha.org/try-securimage/', proxies=self._proxies, verify=False).cookies
        jsessionid = cookies.get('JSESSIONID')
        return {'JSESSIONID': jsessionid}


    def _request(self, plate):
        """Performs an HTTP request with a given content."""
        url = ('https://www.phpcaptcha.org/try-securimage/')
        data = self._body(plate)
        cookies = self._captcha_cookie()
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Cache-Control': 'no-cache',
            'Content-Length': '661',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'sinespcidadao.sinesp.gov.br',
            'User-Agent': 'SinespCidadao / 3.0.2.1 CFNetwork / 758.2.8 Darwin / 15.0.0',
            'Connection':'close',
        }
        return requests.post(url, data, headers, proxies=self._proxies, cookies=cookies, verify=False, timeout=self._timeout)


    def _parse(self, response):
        """Parses XML result from HTTP response."""
        body_tag = '{http://schemas.xmlsoap.org/soap/envelope/}Body'
        response_tag = ('{ct_captcha0}')
        return_tag = 'return'

        try:
            xml = response.decode('latin-1').encode('utf-8')
            xml = ElementTree.fromstring(xml)
            elements = xml.find(body_tag).find(response_tag).find(return_tag)
        except:
            raise InvalidResponse('Could not parse request response.')

        elements = dict(((element.tag, element.text) for element in elements))

        elements = dict(
            return_code=elements.get('codigoRetorno'),
            return_message=elements.get('mensagemRetorno'),
            status_code=elements.get('codigoSituacao'),
			status_captcha.get('letras')
        )

        return elements
