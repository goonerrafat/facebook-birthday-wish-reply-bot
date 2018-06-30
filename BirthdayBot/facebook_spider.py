from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from lxml import html
from random import choice
import re
import time

class FacebookSpider():
    # static variable
    uname_xpath = "//input[@id='email']"
    pass_xpath = "//input[@id='pass']"
    loginbutton_id = "loginbutton"

    facebook = 'https://www.facebook.com'
    activity_log_extension_url = '/allactivity?privacy_source=activity_log&log_filter=cluster_5'

    scroll_count = 100
    escape_count = 10
    sleep_time1 = 3
    sleep_time2 = .5

    birthday_keywords = ["(b|B)day","(b|B)\'day","(b|B)irthday","(h|H)bd","(w|W)ish" ,"(r|R)eturns", u"জন্মদিন" , u"বার্থডে"] ;
    response_keywords = ['Thank you very much :D', 'Thanks a lot! :D', 'Thank you! :D' ,u'ধন্যবাদ ! :D']


    def __init__(self, userid , password , birthday):
        self.userid = userid
        self.password = password
        self.birthday = birthday
        self.browser = None
        self.key_actions = None
        self.webdriver_path = ''
        self.profile = ''
        self.target_url = ''


    def set_webdriver_path(self, path):
        self.webdriver_path = path

    def set_target_url(self , profile_url):
        self.profile = FacebookSpider.facebook +profile_url
        self.target_url = self.profile + FacebookSpider.activity_log_extension_url

    def set_browser(self):
        self.browser = webdriver.Firefox()
        self.key_actions = webdriver.ActionChains(self.browser)


    def facebook_login(self):
        self.browser.get(FacebookSpider.facebook)
        uname_element = self.browser.find_element_by_xpath(FacebookSpider.uname_xpath)
        pass_element = self.browser.find_element_by_xpath(FacebookSpider.pass_xpath)
        loginbutton_element = self.browser.find_element_by_id(FacebookSpider.loginbutton_id)

        # Logging in
        uname_element.send_keys(self.userid)
        pass_element.send_keys(self.password)
        loginbutton_element.click()


    def perform_escape(self):
        for i in range (FacebookSpider.escape_count):
            self.key_actions.send_keys(Keys.ESCAPE).perform()
            time.sleep(FacebookSpider.sleep_time2)

    def perform_scroll(self):
        for i in range(FacebookSpider.scroll_count):
            self.key_actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(FacebookSpider.sleep_time2)

    def process_target_page(self):
        #implement escape , scroll etc
        self.browser.get(self.target_url)
        time.sleep(FacebookSpider.sleep_time1)
        self.perform_escape()
        self.perform_scroll()


    def extract_post_urls(self):
        sc = self.browser.page_source
        soup = BeautifulSoup(sc, 'lxml')
        links = [self.facebook + l['href'] for l in soup.find_all('a', class_ = '_39g5' , string = re.compile(self.birthday+r"\s\w*"))]

        return links 


    def check_birthday(self):
        page = self.browser.page_source
        tree = html.fromstring(page)
        user_content = tree.xpath("//div[contains(@class, '_5pbx userContent')]")

        # check whether it is a valid post(post on your wall made by someone)
        try:
            if any(re.search(post , user_content[0].text_content()) for post in FacebookSpider.birthday_keywords):
                #print("This is a birthday post!!!!!!!")
                return True
            else:
                #print("This is not a birthday post, ignore it") ;
                return False
        except IndexError:
            print("No Post")
            return False

    def response_birthday(self):
        self.perform_escape()
        time.sleep(FacebookSpider.sleep_time1)
        comment= self.browser.find_element_by_xpath("//a[contains(@class, 'comment_link _5yxe')]")
        comment.click()
        time.sleep(FacebookSpider.sleep_time1)
        comment_box= self.browser.find_element_by_xpath("//div[@contenteditable='true']")

        comment_box.send_keys(choice(FacebookSpider.response_keywords))
        #browser.implicitly_wait(1)
        comment_box.send_keys(Keys.ENTER)

        #like the post(not working for now)
       # like_button = self.browser.find_elements_by_css_selector("a.UFILikeLink._4x9-._4x9_._48-k")
       # like_button.click()

    def process_post_links(self , links):
        for link in links:
            self.browser.get(link)

            if(self.check_birthday()):
                self.response_birthday()

        time.sleep(FacebookSpider.sleep_time1)
       # browser.close()