from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time

class VkDriverTools:

    def __init__(self, config):
        self.driver = webdriver.Chrome(config['paths']['chromedriver'])
        self.vk_login_url = config['vk']['urls']['login']
        self.vk_feed_url = config['vk']['urls']['feed']
        self.vk_login = config['vk']['auth']['login']
        self.vk_password = config['vk']['auth']['password']

    def get_driver(self):
        return self.driver

    def get_feed(self):
        self.driver.get(self.vk_feed_url)
        wall_data = []
        posts = self.driver.find_elements_by_class_name('feed_row')
        for post in posts:
            try:
                id = post.find_element_by_class_name('_post').get_attribute('data-post-id')
                photo = post.find_element_by_class_name('image_cover')
                background_image_property = photo.value_of_css_property('background-image')
                url = self.__format_background_url(background_image_property)
                text = post.find_element_by_class_name('wall_post_text').text
                wall_data.append({"image": url, "text": text, "id": id, "link": "https://vk.com/wall{}".format(id)})
            except NoSuchElementException as e:
                pass

        return wall_data

    @staticmethod
    def __format_background_url(url):
        start_position = url.find('("')
        end_position = url.find('")')
        return url[start_position+2:end_position]


    def login(self):
        self.driver.get(self.vk_login_url)
        login_field = self.driver.find_element_by_id('email')
        password_field = self.driver.find_element_by_id('pass')
        login_button = self.driver.find_element_by_id('login_button')
        login_field.send_keys(self.vk_login)
        password_field.send_keys(self.vk_password)
        login_button.submit()
        time.sleep(2)