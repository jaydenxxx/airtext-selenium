import time
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Base():
    def __init__(self):
        self.driver = None
        self.account = '18628309200'
        self.pwd = 'Aa123456'

    def _setUp(self):
        '''
        初始化Chrome driver
        :return:
        '''
        #driver = webdriver.Chrome()
        driver_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"  # chromedriver 路径
        broswer_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # 浏览器exe路径
        Options = ChromeOptions()
        Options.binary_location = broswer_path  # 浏览器路径，不指定的话会自动查找Chrome 路径，如果Chrome安装的话
        driver = Chrome(chrome_options=Options, executable_path=driver_path, port=9515)
        #窗口全屏
        driver.maximize_window()
        #设置隐性等待时间
        driver.implicitly_wait(30)
        self.driver = driver

    def login_crm(self):
        driver = self.driver
        driver.get('http://172.17.1.246:1007')
        time.sleep(0.5)
        driver.find_element_by_id("username").send_keys(self.account)
        driver.find_element_by_id("password").send_keys(self.pwd)
        driver.find_element_by_id("loginBtn").click()
        self.driver = driver

    def tearDown(self):
        self.driver.close()

    def _confirm(self, confirm_text):
        '''
        统一确认弹窗
        :return:
        '''
        driver = self.driver

    def _promot(self):
        '''
        统一提示弹窗
        :return:
        '''
        driver = self.driver
        driver.find_element_by_css_selector('#layui-layer2 > div.layui-layer-btn > a').click()


class Airticket(Base):
    def __init__(self, OrderId, Type=1):
        super(Airticket, self).__init__()
        self.OrderId = OrderId
        self.Type = Type

    def __HandOperationOrderInfo(self):
        '''
        手动出票出票
        :return:
        '''
        driver = self.driver
        time.sleep(1)
        #出票处理页面url
        HandOperationOrderInfo_link = 'http://172.17.1.246:1007/OutOrderInfo/WaitOutOrder?orderID=%s' % (self.OrderId)
        driver.get(HandOperationOrderInfo_link)
        time.sleep(1)
        driver.find_element_by_css_selector('#success > p > label > input[type="radio"]').click()

        passger_group = driver.find_element_by_css_selector('#success > div:nth-child(3)')
        passger_num = len(passger_group.find_elements_by_css_selector('div[class="form-group"]'))
        # 单乘机人票号回填
        if passger_num == 1:
            #填票号
            driver.find_element_by_css_selector('#success > div:nth-child(3) > div > div > input').send_keys('000-1234569870')
        #多乘机人票号回填
        else:
            for i in range(1, passger_num+1):
                driver.find_element_by_css_selector('#success > div:nth-child(3) > div:nth-child(%s) > div > input' % (i)).send_keys(
                    '000-1234569870')
        # 采票订单
        driver.find_element_by_id('orderID').send_keys('312312asd')
        # 支付账号
        driver.find_element_by_id('payAccount').send_keys('shanglv51@163.com')
        # 订单金额
        driver.find_element_by_id('orderAmount').send_keys('666')
        #提交
        driver.find_element_by_id('submit').click()
        #确认提交
        driver.find_element_by_class_name('layui-layer-btn0').click()

    def __InvalidRefundOrder(self):
        '''
        退票
        :return:
        '''
        driver = self.driver
        #退票处理页面URL
        HandOperationOrderInfo_link = 'http://172.17.1.246:1007/InvalidRefundTicketOrder/InvalidRefundOrderHandle?orderID=%s&pageType=0' % (self.OrderId)
        driver.get(HandOperationOrderInfo_link)
        time.sleep(1)
        #退票成功
        if self.Type == 301:
            #成功radio选择
            driver.find_element_by_css_selector('#pass > p > label > input[type="radio"]').click()
            #提交
            driver.find_element_by_id('submit').click()
            #
            confirm = driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-content').text
            assert confirm == "确认审核通过？"
            #确认提交
            driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-btn > a.layui-layer-btn0').click()
            time.sleep(2)
            success_confirm = driver.find_element_by_css_selector('#layui-layer3 > div.layui-layer-content').text
            assert "操作成功" in success_confirm
            time.sleep(1)
            driver.find_element_by_css_selector('#layui-layer3 > div.layui-layer-btn > a').click()
            time.sleep(1.5)
            '''退款审核页面'''
            CheckMoney_Link = 'http://172.17.1.246:1007/InvalidRefundTicketOrder/InvalidRefundOrderHandle?orderID=%s&pageType=1' % (self.OrderId)
            driver.get(CheckMoney_Link)
            time.sleep(1)
            #退款审核确认radio
            driver.find_element_by_css_selector('#refund > div.text-center.bg-info > label > input[type="radio"]').click()
            #提交
            driver.find_element_by_id('submit').click()
            #退款确认
            driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-btn > a.layui-layer-btn0').click()
        #驳回退票
        if self.Type == 302:
            #选择驳回radio
            driver.find_element_by_css_selector('#reject > div.text-center.bg-info > label > input[type="radio"]').click()
            #填备注
            driver.find_element_by_css_selector('#reject > div:nth-child(3) > div > div > textarea').send_keys('这是备注！')
            #驳回提交
            driver.find_element_by_id('submit').click()
            # 驳回确认
            driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-btn > a.layui-layer-btn0').click()

    def __AirTicketChangedOrder(self):
        '''
        改签审核
        :return:
        '''
        driver = self.driver
        time.sleep(1)
        #改签处理页面URL
        HandOperationOrderInfo_link = 'http://172.17.1.246:1007/AirTicketChangedOrderHandleTicketOrder/AirTicketChangedOrderHandle?orderID=%s&pageType=0' % (self.OrderId)
        driver.get(HandOperationOrderInfo_link)
        time.sleep(1)
        #改签成功
        if self.Type == 201:
            driver.find_element_by_id('auditmoney').click()
            time.sleep(0.5)
            alert_content = driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-content').text
            #改签价格审核符合
            if "价格相符,请继续审核！" in alert_content:
                driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-btn > a').click()
                #审核通过radio
                driver.find_element_by_css_selector('#passs > p > label > input[type="radio"]').click()
                #提交改签审核
                driver.find_element_by_id('submit').click()
                #操作成功content
                time.sleep(1)
                confirm_content = driver.find_element_by_css_selector('#layui-layer2 > div.layui-layer-content').text
                assert "操作成功" in confirm_content
                #操作成功确认
                driver.find_element_by_css_selector('#layui-layer2 > div.layui-layer-btn > a').click()
                time.sleep(1)
            #需要补差价
            else:
                #补差提示确认
                driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-btn > a').click()
                #补差radio
                driver.find_element_by_css_selector('#sub > div.text-center.bg-info > label > input[type="radio"]').click()
                #授信代扣radio
                driver.find_element_by_css_selector('#sub > div.body-content > p:nth-child(2) > label.col-sm-4 > input[type="radio"]').click()
                #提交
                driver.find_element_by_id('submit').click()
                # 等待提交后弹窗提示，操作成功content
                # WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, '#layui-layer2 > div.layui-layer-content')))
                confirm_content = driver.find_element_by_css_selector('#layui-layer2 > div.layui-layer-content').text
                assert "用户差补支付成功，请继续审核" in confirm_content
                # 提交确认
                driver.find_element_by_css_selector('#layui-layer2 > div.layui-layer-btn > a').click()
                self.__AirTicketChangedOrder()
            time.sleep(1)
            #改签金额审核页面URL
            ChangeCheck_Link = 'http://172.17.1.246:1007/AirTicketChangedOrderHandleTicketOrder/AirTicketChangedOrderHandle?orderID=%s&pageType=1' % (
            self.OrderId)
            driver.get(ChangeCheck_Link)
            #改签完成radio
            driver.find_element_by_css_selector('#refund > div.text-center.bg-info > label > input[type="radio"]').click()
            #提交
            driver.find_element_by_id('submit').click()
            # 操作成功content
            confirm_content = driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-content').text
            assert "操作成功" in confirm_content
        #驳回改签
        elif self.Type == 202:
            #驳回radio按钮
            driver.find_element_by_css_selector('#reject > div.text-center.bg-info > label > input[type="radio"]').click()
            #改签驳回备注
            driver.find_element_by_css_selector('#changeRemark3001').send_keys("改签驳回备注！")
            #驳回提交
            driver.find_element_by_id('submit').click()
            #驳回确认
            driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-btn > a.layui-layer-btn0').click()
            #弹窗内容
            confirm_content = driver.find_element_by_css_selector('#layui-layer1 > div.layui-layer-content').text
            assert "操作成功" in confirm_content

    def main(self):
        type = self.Type
        self._setUp()
        self.login_crm()
        #手动出票
        if list(str(type))[0] == "1":
            self.__HandOperationOrderInfo()
        #改签
        elif list(str(type))[0] == "2":
            self.__AirTicketChangedOrder()
        #退票
        elif list(str(type))[0] == "3":
            self.__InvalidRefundOrder()

if __name__ == '__main__':
    '''
    type
    1   -   手动出票
    201 -   改签成功
    202 -   改签失败
    301 -   退票成功
    302 -   退票失败
    '''
    seleniumObj = Airticket(OrderId='1807091537007340a0100237377', Type=1)
    seleniumObj.main()