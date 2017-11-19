#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import os.path
from multiprocessing import Process, Queue, Pool

"""
处理命令行参数，self._args变量为存储3个文件路径的列表，
使用@property将检测参数合法性的validity方法声明为属性，
对指定文件路径的文件检测是否存在，不存在则抛出IOerror异常。
"""
class Args(object):
    def __init__(self, args=sys.argv[1:]):
        self._args = args
    @property
    def validity(self):
        self.insurance_conf = self._args[self._args.index('-c') + 1]
        self.user_conf = self._args[self._args.index('-d') + 1]
        self.dumpfile = self._args[self._args.index('-o') + 1]
        if os.path.exists(self.insurance_conf) is False:
            raise IOError()
        elif os.path.exists(self.user_conf) is False :
            raise IOError()
        else:
            return self._args

"""
Config类定义两个方法，dispose方法对配置文件进行解析，
get_config方法用来获取解析配置文件得到的数据，
子类Insurance_ratio改写父类dispose方法，用来对社保配置文件进行解析，
子类User_data改写父类dispose方法，用来对工号工资配置文件解析。
"""
class Config(object):
    def __init__(self, configfile):
        self._configfile = configfile
        self._config = {}

    def get_config(self,key):
        self._key = key
        self.value = self._config.get(self._key)
        if self.value == None:
            raise KeyError()
        else:
            return self.value

    def dispose(self):
        pass


class Insurane_ratio(Config):
    def dispose(self):
        # self.insurance_dict = {}
        with open(self._configfile, 'r') as file:
            try:
                for line in file:
                    data = line.split('=')
                    info = [i.strip() for i in data]
                    self._config[info[0]] = info[1]
                #queue.put(self._config)
                return self._config
            except:
                raise TypeError()


class Userdata(Config):
    def dispose(self):
        with open(self._configfile, 'r') as file:
            try:
                for line in file:
                    data = line.split(',')
                    info = [i.strip() for i in data]
                    self._config[info[0]] = info[1]
                queue.put(self._config)
                # return self._config
            except:
                raise TypeError()

"""
Calculator类用来计算社保，个税和税后工资，calculate方法参数为Insurance_tatio类的实例和工号工资字典，
计算社保和个税并存入self._insurance和self._income_tax字典
"""
class Calculator(object):
    tax_rate = [0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45]  # 税率
    quick_cal = [0, 105, 555, 1005, 2755, 5505, 13505]  # 速算扣除数
    tax_amount = [0, 1500, 4500, 9000, 35000, 55000, 80000]  # 应纳税额

    # def __init__(self, userdata):
    #     self._userdata = userdata
    #     self._insurance = dict()
    #     self._income_tax = dict()

    def __init__(self):
        self._userdata = queue.get()
        # print(self._userdata)
        self._insurance = dict()
        self._income_tax = dict()
        self.after_tax = dict()

    def calculate(self, insurance_ratio):
        self.ins_conf = insurance_ratio
        self.insurance_ratio_dispose = self.ins_conf.dispose()

        for key, value in self._userdata.items():
            JiShuL = float(self.ins_conf.get_config('JiShuL'))
            JiShuH = float(self.ins_conf.get_config('JiShuH'))
            if float(value) <= JiShuL:
                base = JiShuL
            elif float(value) >= JiShuH:
                base = JiShuH
            else:
                base = float(value)
            self._insurance[key] = base * float(self.ins_conf.get_config('YangLao')) + \
                base * float(self.ins_conf.get_config('YiLiao')) + \
                base * float(self.ins_conf.get_config('ShiYe')) + base * float(self.ins_conf.get_config('GongShang')) +\
                base * float(self.ins_conf.get_config('ShengYu')) + base * float(self.ins_conf.get_config('GongJiJin'))

            if float(value) > 3500:
                tax_income = float(value) - self._insurance[key] - 3500
            else:
                tax_income = 0
            for i in range(6,-1,-1):
                if tax_income == 0:
                    self._income_tax[key] = 0
                    break
                elif tax_income > self.tax_amount[i]:
                    self._income_tax[key] = tax_income * self.tax_rate[i] - self.quick_cal[i]
                    break

            ins = float(self._insurance.get(key))
            tax = float(self._income_tax.get(key))
            after = float(value) - ins - tax
            self.after_tax[key] = [float(value), ins, tax, after]
        queue.put(self.after_tax)
        # return self._insurance, self._income_tax

    # def dumptofile(self, dumpfile_path):
    #     for user, salary in self._userdata.items():
    #         ins = float(self._insurance.get(user))
    #         tax = float(self._income_tax.get(user))
    #         after_tax = float(salary) - ins - tax
    #         salary = float(salary)
    #         data = '%s,%.2f,%.2f,%.2f,%.2f' %(user, salary, ins, tax, after_tax)
    #         with open(dumpfile_path,'a+') as file:
    #             file.write(data)
    #             file.write('\r')

class Dumptofile(object):
    def __init__(self, dumpfile_path):
        self._dumpfile_path = dumpfile_path

    def dump(self):
        data = queue.get()
        for user, value in data.items():
            data = '%s,%.2f,%.2f,%.2f,%.2f' %(user, value[0], value[1], value[2], value[3])
            with open(self._dumpfile_path, 'a+') as file:
                file.write(data)
                file.write('\r')

# if __name__ == '__main__':
#     try:
#         queue = Queue()
#         args = Args().validity
#         # print(args)
#         insurance_conf = args[args.index('-c') + 1]
#         user_conf = args[args.index('-d') + 1]
#         dumpfile = args[args.index('-o') + 1]
#
#         Insurance = Insurane_ratio(insurance_conf)
#         Userdata = Userdata(user_conf).dispose()
#         # print(Userdata)
#
#         Calculator = Calculator(Userdata)
#         Calculator.calculate(Insurance)
#         Calculator.dumptofile(dumpfile)
#     except IOError:
#         print("Command Args Error")
#     except TypeError:
#         print("Config File Format error")
#     except KeyError:
#         print("Dict Key Error")

if __name__ == '__main__':
    try:
        queue = Queue()
        args = Args().validity
        insurance_conf = args[args.index('-c') + 1]
        user_conf = args[args.index('-d') + 1]
        dumpfile = args[args.index('-o') + 1]

        Insurance = Insurane_ratio(insurance_conf)

        Process(target=Userdata(user_conf).dispose()).start()
        Process(target=Calculator().calculate(Insurance)).start()
        Process(target=Dumptofile(dumpfile).dump())
    except IOError:
        print("Command Args Error")
    except TypeError:
        print("Config File Format error")
    except KeyError:
        print("Dict Key Error")