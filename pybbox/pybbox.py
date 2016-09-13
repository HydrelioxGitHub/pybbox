import netaddr as net
import logging
import requests


class Bbox:
    """
    Class to interact with Bouygues Bbox Modem Routeur
    API Reference used for this : https://api.bbox.fr/doc/apirouter/
    """

    DEFAULT_LOCAL_IP = "192.168.1.254"
    API_PREFIX = "api/v1"
    API_DEVICE = "device"
    API_HOSTS = "hosts"
    API_WAN = "wan"
    AUTHENTICATION_TYPE_LOCAL = 0
    AUTHENTICATION_TYPE_REMOTE = 1
    AUTHENTICATION_ACCESS_PUBLIC = 2
    AUTHENTICATION_ACCESS_PRIVATE = 1
    AUTHENTICATION_ACCESS_NONE = 0

    def __init__(self, ip=DEFAULT_LOCAL_IP):
        """
        Initiate a Bbox instance with a default local ip (192.168.1.254
        :param ip: ip of the bow
        """
        self.ip = ip
        if net.IPAddress(self.ip).is_private():
            self.authentication_type = self.AUTHENTICATION_TYPE_LOCAL
        else:
            self.authentication_type = self.AUTHENTICATION_TYPE_REMOTE
        self.authenticated = False

    @property
    def get_access_type (self):
        """
        Return if the access is made on the local network or remotely
        :return: AUTHENTICATION_TYPE_LOCAL or AUTHENTICATION_TYPE_REMOTE
        """
        return self.authentication_type

    """
    USEFUL FUNCTIONS
    """

    def build_url_request(self, api_class, api_method = None):
        """
        Build the url to use for making a call to the Bbox API
        :param api_class: name of the api type (device,  lan, general ...)
        :param api_method: name of the API method to call
        :return: url string
        """
        if api_method is None :
            return "http://{}/{}/{}".format(self.DEFAULT_LOCAL_IP,
                                         self.API_PREFIX, api_class)
        else :
            return "http://{}/{}/{}/{}".format(self.DEFAULT_LOCAL_IP,
                                         self.API_PREFIX, api_class,
                                         api_method)

    def check_authentication(local_access, remote_access):
        """
        Check if the level of authentication if enough to call the API
        Method used as a decorator
        :param local_access: level of auth needed to call the API on the
        local network (public, private, none)
        :param remote_access:level of auth needed to call the API on the
        wan network (public, private, none)
        """
        def dec(wrapped):
            def inner(*args, **kwargs):
                if args[0].authentication_type == args[0].AUTHENTICATION_TYPE_LOCAL:
                    access_type = local_access
                else:
                    access_type = remote_access

                if access_type == args[0].AUTHENTICATION_ACCESS_NONE:
                    logging.error("This API can't be reached througth this "
                                  "access")
                elif access_type == args[0].AUTHENTICATION_ACCESS_PRIVATE:
                    if args[0].authenticated:
                        return wrapped(*args, **kwargs)
                    else:
                        logging.error("You must be authenticated if you want "
                                      "to access this API")
                elif access_type == args[0].AUTHENTICATION_ACCESS_PUBLIC:
                    return wrapped(*args, **kwargs)
            return inner
        return dec

    def __make_API_request (self, url, json = None, cookie = None) :
        """
        Execute an API call
        """
        resp = requests.get(url)
        if resp.status_code != 200:
             # This means something went wrong.
            raise Exception('Error {} with request {}'.format(
                resp.status_code, url))
        return resp.json()[0]

    """
    DEVICE API
    """

    @check_authentication(AUTHENTICATION_ACCESS_PUBLIC,
                          AUTHENTICATION_ACCESS_PRIVATE)
    def get_bbox_info(self):
        """

        """
        url = self.build_url_request(self.API_DEVICE, None)
        return self.__make_API_request(url)

    """
    LAN API
    """

    @check_authentication(AUTHENTICATION_ACCESS_PUBLIC,
                          AUTHENTICATION_ACCESS_PRIVATE)
    def get_all_connected_devices(self):
        """
        Get all info about devices connected to the box
        :return: a list with all devices data
        """
        url = self.build_url_request(self.API_HOSTS, None)
        return self.__make_API_request(url)["hosts"]["list"]

    def is_device_connected (self, ip):
        """
        Check if a device identified by it IP is connected to the box
        :param ip: IP of the device
        :return: True is the device is connected, False if it's not
        """
        all_devices = self.get_all_connected_devices()
        for device in all_devices:
            if ip == device['ipaddress']:
                return device['active'] == 1
        return False

    """
    WAN API
    """

    @check_authentication(AUTHENTICATION_ACCESS_PUBLIC,
                          AUTHENTICATION_ACCESS_PRIVATE)
    def get_xdsl_info(self):
        """
        Get all info about the xdsl connection
        :return: a list with all devices data
        """
        url = self.build_url_request(self.API_WAN, "xdsl")
        return self.__make_API_request(url)["wan"]["xdsl"]

    def is_bbox_connected(self):
        """
        :return: True is the box has an xdsl connection
        """
        xdsl_info = self.get_xdsl_info()
        return xdsl_info["state"] == "Connected"

    def get_up_bitrates (self):
        """
        :return: the upload bitrates of the xdsl connectionbitrates in Mbps
        """
        xdsl_info = self.get_xdsl_info()
        return xdsl_info["up"]["bitrates"]/1000

    def get_down_bitrates (self):
        """
        :return: the download bitrates of the xdsl connectionbitrates in Mbps
        """
        xdsl_info = self.get_xdsl_info()
        return xdsl_info["down"]["bitrates"]/1000