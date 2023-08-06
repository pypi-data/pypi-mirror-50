import os
import ast
import importlib.util
from scraper_factory.core import base_spider


class SpiderManager(object):

    def __init__(self, path=''):
        self.spiders = {}
        self.spiders_path = path
        self.load(self.spiders_path)

    def load(self, path):
        for f in os.listdir(path):
            spider_file = os.path.join(path, f)

            if os.path.isdir(spider_file) or '__' in spider_file:
                continue

            sp = self.__load_spider_from_file(spider_file)
            self.spiders[sp.__name__] = sp

    def __load_spider_from_file(self, filename):
        if not os.path.exists(filename):
            return None

        print('reading {}'.format(filename))
        with open(filename) as f:
            node = ast.parse(f.read())

        classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
        if len(classes) > 1:
            raise AttributeError('File can\'t contain more than one class')
        spider_class = classes[0].name

        spec = importlib.util.spec_from_file_location("spider_module", filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not self.__check_valid_module(module):
            return None

        return getattr(module, spider_class)

    def __check_valid_module(self, module):
        if not hasattr(module, 'metadata'):
            msg = 'Missing metadata dict in module'
            print(msg)
            return False

        if not issubclass(module.metadata.get('instance'), base_spider.BaseSpider):
            return False

        for param in base_spider.metadata:
            if not module.metadata.get(param):
                msg = 'Skipped {}: doesn\'t have a "{}" parameter'.format(file, param)
                print(msg)
                return False

        return True

    def instance(self, name):
        sp = self.spiders.get(name)
        if not sp:
            return None

        return sp.get('instance')

