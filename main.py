from BirthdayBot.facebook_spider import FacebookSpider

'''
    remove everything inside those single quote.
    replace it with your data.
    do NOT remove the single quote.
    dummy data are given for your understanding.
'''

fb_username = 'abcd@gmail.com'   
fb_password = '12345'   

'''
    1.go to your profile
    2.look at the url on the address bar of your browser.copy everything after https://www.facebook.com 
    mine is = /rafat.islam.73
    4. thats your profile id
'''
profile_id = '/rafat.islam.73'

'''
    For birthday field below, please follow the exact format as given. 
    2018 is for this year's birthday post.
'''
birthday = 'May 18, 2018'

if __name__ == '__main__':
    spider = FacebookSpider(fb_username, fb_password, birthday)
    spider.set_target_url(profile_id)
    spider.set_browser()
    spider.facebook_login()
    spider.process_target_page()
    urls = spider.extract_post_urls()
    spider.process_post_links(urls)
