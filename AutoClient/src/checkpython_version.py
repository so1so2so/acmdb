#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import sys


def check():
    if sys.version_info > (3, 0):
        return True
    else:
        return False
