import netaddr as net
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
        self.bbox_url = BboxAPIUrl(None, None, ip)
        self.bbox_auth = BboxAuth(None, None, False, self.bbox_url.authentication_type)

    @property
    def get_access_type(self):
        """
        Return if the access is made on the local network or remotely
        :return: AUTHENTICATION_TYPE_LOCAL or AUTHENTICATION_TYPE_REMOTE
        """
        return self.bbox_url.authentication_type

    """
    USEFUL FUNCTIONS
    """

    """
    DEVICE API
    """

    def get_bbox_info(self):
        """

        """
        self.bbox_auth.set_access(BboxConstant.AUTHENTICATION_LEVEL_PUBLIC, BboxConstant.AUTHENTICATION_LEVEL_PRIVATE)
        self.bbox_url.set_api_name(BboxConstant.API_DEVICE, None)
        api = BoxApiCall(self.bbox_url, BboxConstant.HTTP_METHOD_GET, None,
                         self.bbox_auth)
        resp = api.execute_api_request()
        return resp.json()[0]

    def set_display_luminosity(self, luminosity):
        """
        :param luminosity: int must be between 0 (light off) and 100
        """

        if (luminosity < 0) or (luminosity > 100):
            raise ValueError("Luminosity must be between 0 and 100")
        self.bbox_auth.set_access(BboxConstant.AUTHENTICATION_LEVEL_PRIVATE,
                                  BboxConstant.AUTHENTICATION_LEVEL_PRIVATE)
        self.bbox_url.set_api_name(BboxConstant.API_DEVICE, "display")
        data = {'luminosity': luminosity}
        api = BoxApiCall(self.bbox_url, BboxConstant.HTTP_METHOD_PUT, data,
                         self.bbox_auth)
        response = api.execute_api_request()
        return response

    """
    LAN API
    """

    def get_all_connected_devices(self):
        """
        Get all info about devices connected to the box
        :return: a list with all devices data
        """
        self.bbox_auth.set_access(BboxConstant.AUTHENTICATION_LEVEL_PUBLIC, BboxConstant.AUTHENTICATION_LEVEL_PRIVATE)
        self.bbox_url.set_api_name(BboxConstant.API_HOSTS, None)
        api = BoxApiCall(self.bbox_url, BboxConstant.HTTP_METHOD_GET, None,
                         self.bbox_auth)
        resp = api.execute_api_request()
        return resp.json()[0]["hosts"]["list"]

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
    USER ACCOUNT
    """

    def login(self, password):
        """

        :param password:
        :return:
        """
        self.bbox_auth.set_access(BboxConstant.AUTHENTICATION_LEVEL_PUBLIC, BboxConstant.AUTHENTICATION_LEVEL_PUBLIC)
        self.bbox_url.set_api_name("login", None)
        data = {'password': password}
        api = BoxApiCall(self.bbox_url, BboxConstant.HTTP_METHOD_POST, data,
                         self.bbox_auth)
        response = api.execute_api_request()
        if response.status_code == 200:
            self.bbox_auth.set_cookie_id(response.cookies["BBOX_ID"])
        return self.bbox_auth.is_authentified()

    def logout(self):
        """
        :return:
        """
        self.bbox_auth.set_access(BboxConstant.AUTHENTICATION_LEVEL_PUBLIC, BboxConstant.AUTHENTICATION_LEVEL_PUBLIC)
        self.bbox_url.set_api_name("logout", None)
        api = BoxApiCall(self.bbox_url, BboxConstant.HTTP_METHOD_POST, None,
                         self.bbox_auth)
        response = api.execute_api_request()
        if response.status_code == 200:
            self.bbox_auth.set_cookie_id(None)
        return not self.bbox_auth.is_authentified()

    """
    WAN API
    """

    def get_xdsl_info(self):
        """
        Get all info about the xdsl connection
        :return: a list with all devices data
        """
        self.bbox_auth.set_access(BboxConstant.AUTHENTICATION_LEVEL_PUBLIC, BboxConstant.AUTHENTICATION_LEVEL_PRIVATE)
        self.bbox_url.set_api_name(BboxConstant.API_WAN, "xdsl")
        api = BoxApiCall(self.bbox_url, BboxConstant.HTTP_METHOD_GET, None,
                         self.bbox_auth)
        resp = api.execute_api_request()
        return resp.json()[0]["wan"]["xdsl"]

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
