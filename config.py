import os
import platform


def get_driver_path():
    if platform.system() == 'Windows':
        return os.path.abspath(os.path.join('.', 'resources', 'chromedriver.exe'))
    else:
        return os.path.abspath(os.path.join('.', 'resources', 'chromedriver'))


captcha_temp = os.path.abspath(os.path.join('.', 'temp')) + os.path.sep + 'captcha.png'
captcha2_temp = os.path.abspath(os.path.join('.', 'temp')) + os.path.sep + 'captcha2.png'

download_temp_path = os.path.abspath(os.path.join('.', 'temp', 'download'))
output_path = os.path.abspath(os.path.join('.', 'output'))

columns = ["dc.contributor.author[zh_TW]",
           "dc.contributor.author[en_US]",
           "dc.title[zh_TW]",
           "dc.title[en_US]",
           "dc.date[zh_TW]",
           "contents",
           "dc.description.abstract[zh_TW]",
           "dc.description.abstract[en_US]",
           "dc.relation[zh_TW]",
           "dc.subject[zh_TW]",
           "dc.subject[en_US]",
           "dc.type[zh_TW]"]
