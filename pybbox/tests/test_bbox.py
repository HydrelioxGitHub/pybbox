from unittest import TestCase
from pybbox import Bbox


class TestBbox(TestCase):
    def setUp(self):
        box = Bbox()
        remoteBox = Bbox("31.1.1.1")

    def test_check_authentication(self):
        box = Bbox()
        dec = box.check_authentication(box.AUTHENTICATION_ACCESS_NONE, box.AUTHENTICATION_ACCESS_NONE)
        self.fail()

    def test_get_bbox_info(self):
        self.fail()

    def test_build_url_request(self):
        box = Bbox()
        url = box.build_url_request("api_class", "api_method")
        self.assertEqual(url, "http://192.168.1.254/api/v1/api_class/api_method")

    def test_build_url_request_without_api_method(self):
        box = Bbox()
        url = box.build_url_request("api_class")
        self.assertEqual(url, "http://192.168.1.254/api/v1/api_class")

    def test_get_access_type_local(self):
        box = Bbox()
        self.assertEqual(box.get_access_type(), box.AUTHENTICATION_TYPE_LOCAL)

    def test_get_access_type_remote(self):
        remoteBox = Bbox("31.1.1.1")
        self.assertEqual(remoteBox.get_access_type(), remoteBox.AUTHENTICATION_TYPE_LOCAL)
