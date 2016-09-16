# -*- coding: utf-8 -*-
__author__ = 'lihui'


B = raw_input("Did you have a good day [y/N]")
while B not in "YNyn":
    B = raw_input("Did you have a good day [y/N]")
else:
    print "hi"