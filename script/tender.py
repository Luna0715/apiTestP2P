import logging
import unittest

import requests

from api.logingAPI import loginAPI
from api.tenderAPI import tenderAPI
from utils import assert_utils
from utils import request_third_api

class tender(unittest.TestCase):
    tender_id = "968"
    phone = "13112345676"
    pwd = "test123"
    def setUp(self):
        self.tender_api = tenderAPI()
        #实例化一个请求连接
        self.session = requests.Session()
        #登录
        self.login_api = loginAPI()
        response = self.login_api.login(self.session,self.phone,self.pwd)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")

    def tearDown(self):
        self.session.close()
    def test01_get_loaninfo(self):
        #发送获取请求
        response = self.tender_api.get_loaninfo(self.session,self.tender_id )
        logging.info("get_tender response = {}".format(response.json()))
        #断言
        assert_utils(self,response,200,200,"OK")
    def test02_tender(self):
        response = self.tender_api.tender(self.session,self.tender_id,'50')
        logging.info("tender response = {}".format(response.json()))
        #断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        #需要进入到第三方的认证
        #1、提取form表单数据，提取请求信息
        form_data = response.json().get("description").get("form")
        #2、发起第三方请求
        response = request_third_api(form_data= form_data)
        logging.info("tender response = {}".format(response.text))
        self.assertEqual("InitiativeTender OK",response.text)

    def test03_tenderlist(self):
        status = "tender"
        response = self.tender_api.get_tenderlist(self.session,status)
        logging.info("tenderlist response = {}".format(response.json()))
        self.assertEqual(200,response.status_code)










