import logging
import unittest
from time import sleep
import requests
from parameterized import parameterized
from api.logingAPI import loginAPI
import random
from utils import assert_utils, read_imgVerify_data,read_register_data


class login(unittest.TestCase):
    phone1 = '13033447711'
    phone2 = '13033447712'
    phone3 = '13033447713'
    phone4 = '13033447714'
    pwd = 'test123'
    imgCode = '8888'
    smsCode = '666666'

    def setUp(self):
        self.login_api = loginAPI()
        self.session = requests.Session()
    def tearDown(self):
        self.session.close()

    @parameterized.expand(read_imgVerify_data("imgVerify.json"))
    def test01_get_img_code(self,type,status_code):
        #根据不同的type类型准备不同的参数数据
        r = ''
        if type =="float":
            r=str(random.random())
        elif type == "int":
            r=str(random.randint(10000000,90000000))
        elif type == 'char':
            r ="".join(random.sample("abcdefghigklmn",8))
        # 发送请求
        response = self.login_api.getImgCode(self.session,r)
        # 对响应结果进行断言
        self.assertEqual(status_code, response.status_code)

    '''
    #参数为随机小数时，获取图片验证码成功
    def test01_get_img_code_random_float(self):
        #定义参数(随机小数)
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)
    # 参数为随机整数时获取图片验证码成功
    def test02_get_img_code_random_int(self):
        #定义参数（随机整数）
        r = random.randint(10000000,90000000)
        #调用接口类中的发送图片验证码接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，并进行断言
        self.assertEqual(200, response.status_code)
    #参数为空时，获取图片验证码失败
    def test03_get_img_code_param_is_null(self):
        #定义参数（参数为空）
        #调用接口类中的发送图片验证码接口
        response = self.login_api.getImgCode(self.session,"")
        #接收接口的返回结果，并进行断言
        self.assertEqual(404, response.status_code)
    #参数为空时，获取图片验证码失败
    def test04_get_img_code_random_char(self):
        #定义参数（随机字母）
        r = random.sample("abcdefghigklmn",8)
        #调用接口类中的发送图片验证码接口
        response = self.login_api.getImgCode(self.session,''.join(r))
        #接收接口的返回结果，并进行断言
        self.assertEqual(400, response.status_code)
    '''

    #获取短信验证码成功--参数正确
    def test05_get_sms_code_success(self):
        #1、获取图片验证码
        #定义参数(随机小数)
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)

        # 2、获取短信验证码
        #定义参数（正确的手机号和验证码）
        #调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone1,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        self.assertEqual("短信发送成功",response.json().get("description"))
        assert_utils(self,response,200,200,"短信发送成功")
    #获取短信验证码失败--图片验证码错误
    def test06_get_sms_code_imgCode_error(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号，图片验证码错误）
        error_code = '1234'
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, error_code)
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")
    #获取短信验证码失败--图片验证码为空
    def test07_get_sms_code_imgCode_is_null(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号，图片验证码为空）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, '')
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")
    #获取短信验证码失败--手机号为空
    def test08_get_sms_code_phone_is_null(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（手机号为空，图片验证码正确）
        error_code = '1234'
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, '', self.imgCode)
        # 对收到的响应结果，进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(100,response.json().get("status"))
    #获取短信验证码失败--未调用获取图片验证码接口
    def test09_get_sms_code_no_img_verify(self):
        #1、未获取图片验证码
        #2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    @parameterized.expand(read_register_data("register.json"))
    def test10_get_img_code(self,phone,pwd,imgVerifyCode,phoneCode,dyServer,invite_phone,status_code,status,description):
        #1、获取图片验证码成功
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        #2、获取短信验证码成功
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, phone, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        #3、使用参数化的测试数据进行注册，并返回对应的结果
        #发送注册请求
        response = self.login_api.register(self.session, phone, pwd, imgVerifyCode, phoneCode, dyServer, invite_phone)
        logging.info("register response = {}".format(response.json()))
        # 对收到的响应进行断言
        assert_utils(self, response, status_code, status, description)

    '''
    #输入必填项，注册成功
    def test10_register_success_param_must(self):
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
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("短信发送成功", response.json().get("description"))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、成功注册--输入必填项
        #调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone1, self.pwd)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "注册成功")

    #输入所有项，注册成功
    def test11_register_success_param_all(self):
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
        response = self.login_api.getSmsCode(self.session, self.phone2, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("短信发送成功", response.json().get("description"))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、发送注册请求
        response = self.login_api.register(self.session,self.phone2, self.pwd,invite_phone="13012345678")
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "注册成功")

    #手机号已存在时，注册失败
    def test12_register_phone_is_exist(self):
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
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("短信发送成功", response.json().get("description"))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败--手机号已重复
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone1, self.pwd)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "手机已存在!")

    #注册失败，密码为空
    def test13_register_password_is_null(self):
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
        response = self.login_api.getSmsCode(self.session, self.phone3,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("短信发送成功", response.json().get("description"))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败--密码为空
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone3, '')
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "密码不能为空")

    #注册失败，图片验证码错误
    def test14_register_img_code_is_wrong(self):
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
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("短信发送成功", response.json().get("description"))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败--手机号已重复
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone4, self.pwd,'1234')
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "验证码错误!")

    #注册失败--短信验证码错误
    def test15_register_phone_is_exist(self):
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
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("短信发送成功", response.json().get("description"))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败--短信验证码错误
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone4, self.pwd,self.imgCode,'123456')
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "验证码错误")

    # 注册失败，不同意注册协议
    def test16_register_noagree_protocal(self):
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
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("短信发送成功", response.json().get("description"))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册失败--手机号已重复
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone4, self.pwd,dyServer = 'off')
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "请同意我们的条款")
    '''
    #登录成功
    def test17_login_success(self):
        #准备参数
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,self.phone1,self.pwd)
        #对接口进行断言
        assert_utils(self,response,200,200,"登录成功")

    #登录失败--用户名不存在
    def test18_login_phone_not_exist(self):
        #准备参数
        Wphone = '13000000000'
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,Wphone,self.pwd)
        #对接口进行断言
        assert_utils(self,response,200,100,"用户不存在")

    #登录失败--密码为空
    def test19_login_pwd_is_null(self):
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,self.phone1,'')
        #对接口进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    #登录失败--密码错误
    def test20_login_wrong_Pwd(self):
        wrong_pwd = 'error'
        #1、输入错误密码，提示错误一次
        response = self.login_api.login(self.session,self.phone1,wrong_pwd)
        #对接口进行断言
        assert_utils(self,response,200,100,"密码错误1次,达到3次将锁定账户")
        #2、输入错误密码，提示密码错误2次
        response = self.login_api.login(self.session,self.phone1,wrong_pwd)
        #对接口进行断言
        assert_utils(self,response,200,100,"密码错误2次,达到3次将锁定账户")
        #3、输入错误密码，提示错误三次被锁定
        response = self.login_api.login(self.session,self.phone1,wrong_pwd)
        #对接口进行断言
        assert_utils(self,response,200,100,"由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #4、输入正确密码，提示被锁定
        response = self.login_api.login(self.session,self.phone1,self.pwd)
        #对接口进行断言
        assert_utils(self,response,200,100,"由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #5、等待60s,再输入正确密码，提示登录成功
        sleep(60)
        response = self.login_api.login(self.session,self.phone1,self.pwd)
        #对接口进行断言
        assert_utils(self,response,200,200,"登录成功")






















