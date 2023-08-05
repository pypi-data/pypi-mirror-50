"""A simpler RESTful API for Comodo/Sectigo"""

__version__ = "0.4.0"

import jsend
import logging
import requests

logger = logging.getLogger(__name__)


class ComodoCA(object):
    """
    Top level class for the Comodo CA. Only very generic 'things' go here.
    """

    formats = {'AOL': 1,
               'Apache/ModSSL': 2,
               'Apache-SSL': 3,
               'C2Net Stronghold': 4,
               'Cisco 3000 Series VPN Concentrator': 33,
               'Citrix': 34,
               'Cobalt Raq': 5,
               'Covalent Server Software': 6,
               'IBM HTTP Server': 7,
               'IBM Internet Connection Server': 8,
               'iPlanet': 9,
               'Java Web Server (Javasoft / Sun)': 10,
               'Lotus Domino': 11,
               'Lotus Domino Go!': 12,
               'Microsoft IIS 1.x to 4.x': 13,
               'Microsoft IIS 5.x and later': 14,
               'Netscape Enterprise Server': 15,
               'Netscape FastTrac': 16,
               'Novell Web Server': 17,
               'Oracle': 18,
               'Quid Pro Quo': 19,
               'R3 SSL Server': 20,
               'Raven SSL': 21,
               'RedHat Linux': 22,
               'SAP Web Application Server': 23,
               'Tomcat': 24,
               'Website Professional': 25,
               'WebStar 4.x and later': 26,
               'WebTen (from Tenon)': 27,
               'Zeus Web Server': 28,
               'Ensim': 29,
               'Plesk': 30,
               'WHM/cPanel': 31,
               'H-Sphere': 32,
               'OTHER': -1,
               }

    format_type = [
        'x509',     # X509, Base64 encoded
        'x509CO',   # X509 Certificate only, Base64 encoded
        'x509IO',   # X509 Intermediates/root only, Base64 encoded
        'base64',   # PKCS#7 Base64 encoded
        'bin',      # PKCS#7 Bin encoded
        'x509IOR',  # X509 Intermediates/root only Reverse, Base64 encoded
    ]


class ComodoTLSService(ComodoCA):
    """
    Class that encapsulates methods to use against Comodo SSL/TLS certificates
    """
    def __init__(self, **kwargs):
        """
        :param string api_url: The full URL for the API server
        :param string customer_login_uri: The URI for the customer login (if your login to the Comodo GUI is at
                https://hard.cert-manager.com/customer/foo/, your login URI is 'foo').
        :param string login: The login user
        :param string org_id: The organization ID
        :param string password: The API user's password
        :param bool client_cert_auth: Whether to use client certificate authentication
        :param string client_public_certificate: The path to the public key if using client cert auth
        :param string client_private_key: The path to the private key if using client cert auth
        """
        # Using get for consistency and to allow defaults to be easily set
        self.api_url = kwargs.get('api_url')
        self.customer_login_uri = kwargs.get('customer_login_uri')
        self.login = kwargs.get('login')
        self.org_id = kwargs.get('org_id')
        self.password = kwargs.get('password')
        self.client_cert_auth = kwargs.get('client_cert_auth')
        self.session = requests.Session()
        if self.client_cert_auth:
            self.client_public_certificate = kwargs.get('client_public_certificate')
            self.client_private_key = kwargs.get('client_private_key')
            self.session.cert = (self.client_public_certificate, self.client_private_key)
        self.headers = {
            'login': self.login,
            'password': self.password,
            'customerUri': self.customer_login_uri
        }
        self.session.headers.update(self.headers)

    def _create_url(self, suffix):
        """
        Create a URL from the API URL that the instance was initialized with.

        :param str suffix: The suffix of the URL you wish to create i.e. for https://example.com/foo the suffix would be /foo
        :return: The full URL
        :rtype: str
        """
        url = self.api_url + suffix
        logger.debug('URL created: %s', url)

        return url

    def _get(self, url):
        """
        GET a given URL

        :param str url: A URL
        :return: The requests session object

        """
        logger.debug('Performing a GET on url: %s', url)
        result = self.session.get(url)

        logger.debug('Result headers: %s', result.headers)
        logger.debug('Text result: %s', result.text)

        return result

    def get_cert_types(self):
        """
        Collect the certificate types that are available to the customer.

        :return: A list of dictionaries of certificate types
        :rtype: list
        """
        url = self._create_url('types')

        try:
            result = self._get(url)
        except ConnectionError:
            return jsend.error(f'A connection error to {self.api_url} occurred.')

        if result.status_code == 200:
            return jsend.success({'types': result.json()})
        else:
            return jsend.fail(result.json())

    def collect(self, cert_id, format_type):
        """
        Collect a certificate.

        :param int cert_id: The certificate ID
        :param str format_type: The format type to use: Allowed values: 'x509' - for X509, Base64 encoded, 'x509CO' - for X509 Certificate only, Base64 encoded, 'x509IO' - for X509 Intermediates/root only, Base64 encoded, 'base64' - for PKCS#7 Base64 encoded, 'bin' - for PKCS#7 Bin encoded, 'x509IOR' - for X509 Intermediates/root only Reverse, Base64 encoded
        :return: The certificate_id or the certificate depending on whether the certificate is ready (check status code)
        :rtype: dict
        """

        url = self._create_url('collect/{}/{}'.format(cert_id, format_type))

        logger.debug('Collecting certificate at URL: %s', url)

        try:
            result = self._get(url)
        except ConnectionError:
            return jsend.error(f'A connection error to {self.api_url} occurred.')

        logger.debug('Collection result code: %s', result.status_code)

        # The certificate is ready for collection
        if result.status_code == 200:
            return jsend.success({'certificate': result.content.decode(result.encoding),
                                  'certificate_status': 'issued',
                                  'certificate_id': cert_id})
        # The certificate is not ready for collection yet
        elif result.status_code == 400 and result.json()['code'] == 0:
            return jsend.fail({'certificate_id': cert_id, 'certificate': '', 'certificate_status': 'pending'})
        # Some error occurred
        else:
            return jsend.fail(result.json())

    def renew(self, cert_id):
        """
        Renew a certificate by ID.

        :param int cert_id: The certificate ID
        :return: The result of the operation, 'Successful' on success
        :rtype: dict
        """

        url = self._create_url('renewById/{}'.format(cert_id))

        try:
            result = self.session.post(url, json='')
        except ConnectionError:
            return jsend.error(f'A connection error to {self.api_url} occurred.')

        if result.status_code == 200:
            return jsend.success({'certificate_id': result.json()['sslId']})
        else:
            return jsend.fail(result.json())

    def revoke(self, cert_id, reason=''):
        """
        Revoke a certificate.

        :param int cert_id: The certificate ID
        :param str reason: Reason for revocation (up to 512 characters), can be blank: '', but must exist.
        :return: The result of the operation, 'Successful' on success
        :rtype: dict
        """
        url = self._create_url('revoke/{}'.format(cert_id))
        data = {'reason': reason}

        try:
            result = self.session.post(url, json=data)
        except ConnectionError:
            return jsend.error(f'A connection error to {self.api_url} occurred.')

        if result.status_code == 204:
            return jsend.success()
        else:
            return jsend.error(result.json()['description'])

    def submit(self, cert_type_name, csr, term, subject_alt_names=''):
        """
        Submit a certificate request to Comodo.

        :param string cert_type_name: The full cert type name (Example: 'PlatinumSSL Certificate') the supported
                                      certificate types for your account can be obtained with the
                                      get_cert_types() method.
        :param string csr: The Certificate Signing Request (CSR)
        :param int term: The length, in days, for the certificate to be issued
        :param string subject_alt_names: Subject Alternative Names separated by a ",".
        :return: The certificate_id and the normal status messages for errors.
        :rtype: dict
        """

        cert_types = self.get_cert_types()

        # If collection of cert types fails we simply pass the error back.
        if jsend.is_fail(cert_types) or jsend.is_error(cert_types):
            return cert_types

        # Find the certificate type ID
        for cert_type in cert_types['data']['types']:
            if cert_type['name'] == cert_type_name:
                cert_type_id = cert_type['id']

        url = self._create_url('enroll')
        data = {'orgId': self.org_id, 'csr': csr, 'subjAltNames': subject_alt_names, 'certType': cert_type_id,
                'numberServers': 1, 'serverType': -1, 'term': term, 'comments': 'Requested with comodo_proxy',
                'externalRequester': ''}
        try:
            result = self.session.post(url, json=data)
        except ConnectionError:
            return jsend.error(f'A connection error to {self.api_url} occurred.')

        if result.status_code == 200:
            return jsend.success({'certificate_id': result.json()['sslId']})
        # Anything else is an error
        else:
            return jsend.error(result.json()['description'])
