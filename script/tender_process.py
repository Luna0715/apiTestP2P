import unittest

import app

from api.logingAPI import loginAPI
from api.tenderAPI import tenderAPI
from api.trustAPI import trustAPI
import requests
import random
import logging
from utils import assert_utils, request_third_api,DButils


#注册 登录  激活  充值   展示投标页 投标  获取我的投标列表


class tender_process(unittest.TestCase):
    phone = "13112345672"
    tender_id = 968
    imVerifyCode = 8888
    pwd = "test123"

    @classmethod
    def setUpClass(cls):
        cls.login_api = loginAPI()
        cls.tender_api = tenderAPI()
        cls.trust_api = trustAPI()
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        sql1 = "delete from mb_member_register_log where phone in ('13033447711','13033447712','13033447713','13033447714','13033447715','13112345672');"
        DButils.delete(app.DB_MEMBER,sql1)
        logging.info("delete sql = {}".format(sql1))
        sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13033447711','13033447712','13033447713','13033447714','13033447715','13112345672');"
        DButils.delete(app.DB_MEMBER,sql2)
        logging.info("delete sq2 = {}".format(sql2))
        sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13033447711','13033447712','13033447713','13033447714','13033447715','13112345672');"
        DButils.delete(app.DB_MEMBER,sql3)
        logging.info("delete sq2 = {}".format(sql3))
        sql4 = "delete from mb_member WHERE phone in ('13033447711','13033447712','13033447713','13033447714','13033447715','13112345672');"
        DButils.delete(app.DB_MEMBER,sql4)
        logging.info("delete sq2 = {}".format(sql4))

    #注册
    def test01_register_success_param_must(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone, self.imVerifyCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("短信发送成功", response.json().get("description"))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、成功注册--输入必填项
        #调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone, self.pwd)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "注册成功")

    #登录成功
    def test02_login_success(self):
        #准备参数
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,self.phone,self.pwd)
        #对接口进行断言
        assert_utils(self,response,200,200,"登录成功")

    # 开户请求
    def test03_trust_request(self):
        # 2、发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info("trust register response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 3、发送第三方的开户请求
        form_data = response.json().get("description").get("form")
        logging.info("form response = {}".format(form_data))
        # 调用第三方接口的请求方法
        response = request_third_api(form_data)
        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)

    # 充值成功
    def test04_recharge(self):
        # 2、获取充值验证码
        r = random.random()
        response = self.trust_api.get_recharge_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 3、发送充值请求
        response = self.trust_api.recharge(self.session, '10000')
        logging.info("recharge response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 4、发送第三方充值请求
        # 获取响应中form表单的数据，并提取为后续第三方请求的参数
        form_data = response.json().get("description").get("form")
        logging.info("form response = {}".format(form_data))
        # 调用第三方请求的接口
        response = request_third_api(form_data)
        logging.info('third recharge response={}'.format(response.text))
        # 断言response是否正确
        self.assertEqual("NetSave OK", response.text)

    #获取详情页
    def test05_get_loaninfo(self):
        #发送获取请求
        response = self.tender_api.get_loaninfo(self.session,self.tender_id)
        logging.info("get_tender response = {}".format(response.json()))
        #断言
        assert_utils(self,response,200,200,"OK")

    # 投资
    def test06_tender(self):
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

    # 我的投资列表
    def test07_tenderlist(self):
        status = "tender"
        response = self.tender_api.get_tenderlist(self.session,status)
        logging.info("tenderlist response = {}".format(response.json()))
        self.assertEqual(200,response.status_code)
