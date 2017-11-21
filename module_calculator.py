#!/usr/bin/python3
# _*_ coding:utf-8 _*_
__author__ = 'anyco'

import sys, getopt, os.path, configparser
from datetime import datetime
from multiprocessing import Process, Value, Pool, Queue


"""
Args类定义了两个函数,usage()函数定义在参数帮助信息,
validity()函数被装饰为Args的属性,用于对参数进行校验并将用户提供的参数值赋值到变量
变量argsdict为存储所有参数的字典
"""
class Args(object):
    def __init__(self, args=sys.argv[1:]):
        self._args = args
        self._argsdict = dict()

    def usage(self):
        print("Usage: %s [-C|-c|-d|-o|-h] [--city|--config|--data|--output|--help] args..." %sys.argv[0])

    @property
    def validity(self):
        try:
            opts, args = getopt.getopt(self._args, "hC:c:d:o:",
                                       ["help", "city=", "config=", "data=", "output="])

            for op, value in opts:
                if op in ("-h", "--help"):
                    self.usage()
                elif op in ("-C", "--city"):
                    self._argsdict['C'] = value.upper()
                elif op in ("-c", "--config"):
                    if os.path.exists(value) is False:
                        raise IOError()
                    else:
                        self._argsdict['c'] = value
                elif op in ("-d", "--data"):
                    if os.path.exists(value) is False:
                        raise IOError
                    else:
                        self._argsdict['d'] = value
                elif op in ("-o", "--output"):
                    self._argsdict['o'] = value

            if self._argsdict.get('C') is None:
                self._argsdict['C'] = 'DEFAULT'

            for arg in ['c', 'd', 'o']:
                if self._argsdict.get(arg) is None:
                    print("Please provide correct args!")
                    self.usage()
                    sys.exit(-1)
            return self._argsdict

        except getopt.GetoptError:
            self.usage()
            sys.exit(-1)

"""
Insurance类继承Config父类处理城市社保配置文件，并将数据写入self._congig字典返回,
使用时Config类提供社保税率配置文件路径和城市名，
Userdata类继承Config父类处理工号工资配置文件，并将数据写入self._config字典返回，
使用时Config类提供员工工资配置文件路径。
"""
class Config(object):
    def __init__(self, conf_path):
        self._conf_path = conf_path
        # self._argsdict = Args().validity
        self._config = dict()

    def dispose(self):
        pass

class Insurance(Config):
    def __init__(self, conf_path, city):
        Config.__init__(self, conf_path)
        self._city = city

    def dispose(self):
        conf = configparser.ConfigParser()
        # confpath = self._argsdict.get('c')
        # city = self._argsdict.get('C')
        conf.read(self._conf_path)
        try:
            if self._city != 'DEFAULT' and self._city not in conf.sections():
                raise configparser.NoSectionError(self._city)
                # if city not in conf.sections():
                #     raise configparser.NoSectionError(city)
                # elif item.lower() not in conf.options(city):
                #     raise configparser.NoOptionError(item, city)
                # else:
                #     self._config = conf.items(city)
            else:
                    self._config = conf.items(self._city)
                # if item.lower() not in conf.defaults().keys():
                #     raise configparser.NoOptionError(item, city)
            return self._config
        except configparser.NoSectionError:
            print('No city in config:',self._city)
            sys.exit(-1)

class Userdata(Config):
    def dispose(self):
        # confpath = self._argsdict.get('d')

        with open(self._conf_path, 'r') as file:
            try:
                for line in file:
                    data = line.split(',')
                    info = [i.strip() for i in data]
                    self._config[info[0]] = info[1]
                queue.put(self._config)
                # return self._config
            except:
                raise TypeError()

class Calculator(object):
    tax_rate = [0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45]  # 税率
    quick_cal = [0, 105, 555, 1005, 2755, 5505, 13505]  # 速算扣除数
    tax_amount = [0, 1500, 4500, 9000, 35000, 55000, 80000]  # 应纳税额

    def __init__(self):
        self._userdata = queue.get()
        self.after_tax = dict()

    def calculate(self, insurance_func):
        self.ins_conf = dict()
        insurance_conf  = insurance_func.dispose()
        for tuple in insurance_conf:
            self.ins_conf[tuple[0]] = tuple[1]

        JiShuL = float(self.ins_conf.get('jishul'))
        JiShuH = float(self.ins_conf.get('jishuh'))

        for key, value in self._userdata.items():
            value = float(value)
            if value <= JiShuL:
                base = JiShuL
            elif value >= JiShuH:
                base = JiShuH
            else:
                base = value
            count_insurance = base * float(self.ins_conf.get('yanglao')) + \
                base * float(self.ins_conf.get('yiliao')) + \
                base * float(self.ins_conf.get('shiye')) + base * float(self.ins_conf.get('gongshang')) +\
                base * float(self.ins_conf.get('shengyu')) + base * float(self.ins_conf.get('gongjijin'))

            if value > 3500:
                tax_income = value - count_insurance - 3500 #应税所得额
            else:
                tax_income = 0

            for i in range(6,-1,-1):
                if tax_income == 0:
                    tax = 0
                    break
                elif tax_income > self.tax_amount[i]:
                    tax = tax_income  * self.tax_rate[i] - self.quick_cal[i]
                    break

            after = value - count_insurance - tax
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.after_tax[key] = [value, count_insurance, tax, after, time]
        queue.put(self.after_tax)
        # return self.ater_tax

class Dumptofile(object):
    def __init__(self, dumppath):
        self._dumppath = dumppath
        self._final_data = queue.get()
        # print(self._final_data)

    def dump(self):
        # data = queue.get()
        for user, value in self._final_data.items():
            data = '%s,%.2f,%.2f,%.2f,%.2f,%s' % (user, value[0], value[1], value[2], value[3], value[4])
            with open(self._dumppath, 'a+') as file:
                file.write(data)
                file.write('\r')

if __name__ == '__main__':
    try:
        queue = Queue()

        args = Args().validity
        ins_conf = args.get('c')
        city_name = args.get('C')
        user_conf = args.get('d')
        dump_path = args.get('o')
        insurance_func = Insurance(ins_conf,city_name)

        Process(target=Userdata(user_conf).dispose()).start()
        Process(target=Calculator().calculate(insurance_func)).start()
        Process(target=Dumptofile(dump_path).dump()).start()
    except IOError:
        print('Error config file path! ')
    except TypeError:
        print("Config File Format error")