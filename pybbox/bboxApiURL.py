from bboxConstant import BboxConstant
import netaddr as net


class BboxAPIUrl:
    """
    Used to handle API url
    """

    API_PREFIX = "api/v1"

    def __init__(self, api_class, api_method, ip=BboxConstant.DEFAULT_LOCAL_IP):
        """
        :param api_class: string
        :param api_method: string
        :param ip: string
        :return:
        """

        self.api_class = api_class
        self.api_method = api_method
        self.ip = ip
        self.url = self.build_url_request()

    def get_api_class(self):
        return self.api_class

    def get_api_method(self):
        return self.api_method

    def get_ip(self):
        return self.ip

    def get_url(self):
        return self.url

    def build_url_request(self):
        """
        Build the url to use for making a call to the Bbox API
        :return: url string
        """
        # Check if the ip is LAN or WAN
        if net.IPAddress(self.ip).is_private():
            url = "http://{}".format(self.ip)
        else:
            url = "https://{}:{}".format(self.ip,
                                         BboxConstant.DEFAULT_REMOTE_PORT)

        if self.api_class is None:
            url = "{}/{}".format(url, self.API_PREFIX)
        else:
            url = "{}/{}/{}".format(url, self.API_PREFIX, self.api_class)

        if self.api_method is None:
            return url
        else:
            return "{}/{}".format(url, self.api_method)
