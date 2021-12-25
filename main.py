import pdb, random, re, time, threading
import pytesseract
from selenium import webdriver
from PIL import Image
 
ids = ['学号1', '学号2']
pws = ['密码1', '密码2']
am_sub = False
pm_sub = False
options = webdriver.ChromeOptions()
options.add_argument('--headless')
 
 
def sleepRand(sec=2, bas=0):
    time.sleep(bas + random.random()*sec)
 
def logLine(msg):
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} {msg}")
 
class subTpThread(threading.Thread):
    def __init__(self, act, pwd):
        super(subTpThread, self).__init__()
        self.act = act
        self.pwd = pwd
        self.drv = webdriver.Chrome(options=options)
 
    def run(self):
        logLine(f"启动 {self.act} 填报线程")
        sleepRand(len(ids))
        tp_str = "%4.1f" % (35.9+random.random()*0.5)
        self.drv = webdriver.Chrome(options=options)
        self.drv.get("https://workflow.sues.edu.cn/default/work/shgcd/jkxxcj/jkxxcj.jsp")
        for i in range(5):
            self.drv.find_element_by_xpath("//img[@class='codeImg fill_form_other']").screenshot(f"{self.act}.png")
            cd = re.match('\d*', pytesseract.image_to_string(Image.open(f"{self.act}.png"))).group()
            self.drv.find_element_by_id('username').send_keys(self.act)
            self.drv.find_element_by_id('password').send_keys(self.pwd)
            self.drv.find_element_by_id('authcode').send_keys(cd)
            sleepRand(1,1)
            self.drv.find_element_by_id('passbutton').click()
            sleepRand(1,1)
            if self.drv.title == '健康信息填报':
                break
        else:
            logLine(f"***失败***：{self.act} 未能成功登录")
            pdb.set_trace()
        self.drv.find_element_by_xpath("//input[@name='tw']").clear()
        self.drv.find_element_by_xpath("//input[@name='tw']").send_keys(tp_str)
        sleepRand(1,1)
        self.drv.find_element_by_id('post').click()
        try:
            self.drv.find_element_by_xpath("//div[text()='健康填报成功']")
        except:
            logLine(f"***失败***：{self.act} 未能成功填报")
            pdb.set_trace()
        else:
            logLine(f"{self.act} {tp_str} 填报成功")
            self.drv.quit()
 
if __name__ == '__main__':
    s = time.localtime(time.time()).tm_hour
    while True:
        n = time.localtime(time.time()).tm_hour
        if n<7 or (n<12 and am_sub) or (n>=12 and pm_sub):
            sleepRand(0,2e3)
            continue
        threads = []
        for act,pwd in zip(ids,pws):
            thread = subTpThread(act,pwd)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        am_sub = n<12
        pm_sub = n>=12
