#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import os.path

"""
????????self._args?????3?????????
??@property?????????validity????????
???????????????????????IOerror???
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
Config????????dispose????????????
get_config??????????????????
??Insurance_ratio????dispose?????????????????
??User_data????dispose?????????????????
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
                return self._config
            except:
                raise TypeError()

"""
Calculator????????????????calculate?????Insurance_tatio????????????
??????????self._insurance?self._income_tax??
"""
class Calculator(object):
    tax_rate = [0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45]  # ??
    quick_cal = [0, 105, 555, 1005, 2755, 5505, 13505]  # ?????
    tax_amount = [0, 1500, 4500, 9000, 35000, 55000, 80000]  # ????

    def __init__(self, userdata):
        self._userdata = userdata
        self._insurance = dict()
        self._income_tax = dict()

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
                base * float(self.ins_conf.get_config('ShiYe')) + base * float(self.ins_conf.get_config('GongShang')) + \
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
        return self._insurance, self._income_tax

    def dumptofile(self, dumpfile_path):
        for user, salary in self._userdata.items():
            ins = float(self._insurance.get(user))
            tax = float(self._income_tax.get(user))
            after_tax = float(salary) - ins - tax
            salary = float(salary)
            data = '%s,%.2f,%.2f,%.2f,%.2f' %(user, salary, ins, tax, after_tax)
            with open(dumpfile_path,'a+') as file:
                file.write(data)
                file.write('\r')


if __name__ == '__main__':
    try:
        args = Args().validity
        # print(args)
        insurance_conf = args[args.index('-c') + 1]
        user_conf = args[args.index('-d') + 1]
        dumpfile = args[args.index('-o') + 1]

        Insurance = Insurane_ratio(insurance_conf)
        Userdata = Userdata(user_conf).dispose()
        # print(Userdata)

        Calculator = Calculator(Userdata)
        Calculator.calculate(Insurance)
        Calculator.dumptofile(dumpfile)
    except IOError:
        print("Command Args Error")
    except TypeError:
        print("Config File Format error")
    except KeyError:
        print("Dict Key Error")

