#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-CLI.
# @File         : cli
# @Time         : 2019-07-11 15:34
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import sys
sys.path.append('./')
import fire
from clis.send_mail import send_mail
from clis.spark import spark
from clis.info import ip

# import clis
# __import__("clis.info")
# model_py = getattr(clis, 'info')
# model_class = getattr(model_py, 'ip')
#
# print(model_class())
# getattr("clis.info", "info_local")
# for (k, v) in self.scen2processorNames.items():
#     self.scenarios2processor[k] = []
#     for name in v:
#         __import__("models." + name + "_model")
#         model_py = getattr(models, name + "_model")
#         model_class = getattr(model_py, name + "Model")
#         self.scenarios2processor[k].append(model_class())


def main():
    fire.Fire()


if __name__ == '__main__':
    fire.Fire()
