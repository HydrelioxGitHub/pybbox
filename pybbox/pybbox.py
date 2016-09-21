import netaddr as net
import logging
import requests
from boxApiCall import BoxApiCall
from bboxConstant import BboxConstant
from bboxAuth import BboxAuth
from bboxApiURL import BboxAPIUrl


class Bbox:
    """
    Class to interact with Bouygues Bbox Modem Routeur
    API Reference used for this : https://api.bbox.fr/doc/apirouter/
    """

    def __init__(self, ip=BboxConstant.DEFAULT_LOCAL_IP):
        """
        Initiate a Bbox instance with a default local ip (192.168.1.254)
        :param ip: ip of the bow
        """
        self.ip = ip
        if net.IPAddress(self.ip).is_private():
            self.authentication_type = BboxConstant.AUTHENTICATION_TYPE_LOCAL
        else:
            self.authentication_type = BboxConstant.AUTHENTICATION_TYPE_REMOTE
        self.authenticated = False

    @property
    def get_access_type(self):
        """
        Return if the access is made on the local network or remotely
        :return: AUTHENTICATION_TYPE_LOCAL or AUTHENTICATION_TYPE_REMOTE
        """
        return self.authentication_type

    """
    USEFUL FUNCTIONS
    """

    """
    DEVICE API
    """

    def get_bbox_info(self):
        """

        """
        auth = BboxAuth(BboxConstant.AUTHENTICATION_LEVEL_PUBLIC, BboxConstant.AUTHENTICATION_LEVEL_PRIVATE, self.authenticated, self.authentication_type)
        api_url = BboxAPIUrl(BboxConstant.API_DEVICE, None, self.ip)
        api = BoxApiCall(api_url, BboxConstant.HTTP_METHOD_GET, None, auth)
        return api.execute_api_request()

    """
    LAN API
    """

    def get_all_connected_devices(self):
        """
        Get all info about devices connected to the box
        :return: a list with all devices data
        """
        auth = BboxAuth(BboxConstant.AUTHENTICATION_LEVEL_PUBLIC, BboxConstant.AUTHENTICATION_LEVEL_PRIVATE, self.authenticated, self.authentication_type)
        api_url = BboxAPIUrl(BboxConstant.API_HOSTS, None, self.ip)
        api = BoxApiCall(api_url, BboxConstant.HTTP_METHOD_GET, None, auth)
        return api.execute_api_request()["hosts"]["list"]

    def is_device_connected(self, ip):
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

    def get_xdsl_info(self):
        """
        Get all info about the xdsl connection
        :return: a list with all devices data
        """
        auth = BboxAuth(BboxConstant.AUTHENTICATION_LEVEL_PUBLIC, BboxConstant.AUTHENTICATION_LEVEL_PRIVATE, self.authenticated, self.authentication_type)
        api_url = BboxAPIUrl(BboxConstant.API_WAN, "xdsl", self.ip)
        api = BoxApiCall(api_url, BboxConstant.HTTP_METHOD_GET, None, auth)
        return api.execute_api_request()["wan"]["xdsl"]

    def is_bbox_connected(self):
        """
        :return: True is the box has an xdsl connection
        """
        xdsl_info = self.get_xdsl_info()
        return xdsl_info["state"] == "Connected"

    def get_up_bitrates(self):
        """
        :return: the upload bitrates of the xdsl connectionbitrates in Mbps
        """
        xdsl_info = self.get_xdsl_info()
        return xdsl_info["up"]["bitrates"] / 1000

    def get_down_bitrates(self):
        """
        :return: the download bitrates of the xdsl connectionbitrates in Mbps
        """
        xdsl_info = self.get_xdsl_info()
        return xdsl_info["down"]["bitrates"] / 1000
