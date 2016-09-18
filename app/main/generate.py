# -*- coding: utf-8 -*-
__author__ = 'lihui'

# TODO 写注释
# TODO GUI
# TODO 创建单个页面的函数
# TODO 所有资源加载监控，制作对应的加载滚动条

import os

from template import *

class Impress(object):

    def __init__(self):
        self.slides = []

    # ro_x represent rotate-x
    # pers represent data-perspective
    # locate represent the locate of the slide you create manually
    def create(self, img, x=0, y=0, z=0, ro_x=0, ro_y=0, ro_z=0, locate=None):

        slide = """
        <div class="step" data-x="%d" data-y="%d"
        data-z="%d" data-rotate-x="%d" data-rotate-y="%d" data-rotate-z="%d">
          <div align="center">
              <img src="%s" height="600">
          </div>
        </div>
        """ % (x, y, z, ro_x, ro_y, ro_z, img)

        # insert slide
        if locate is None:
            self.slides.append(slide)
        else:
            self.slides.insert(locate, slide)

    def bg_music(self, filename=""):
        """
        put the music file in music/
        """
        self.music = filename

    def title_page(self):
        x = self.half_row
        y = self.half_col
        z = self.z + 3000

        slide = """
        <div class="step" id="start" align="center" data-x="%d" data-y="%d"
        data-z="%d">
          <b>{{ album.title }}<br><span style="font-size:25px">{{ album.about }}</span></b><hr>
          <a class="button" id="start-bt" href="#overview">开始</a>
        </div>
        """ % (x, y, z)
        self.slides.insert(0, slide)

    def add_slide(self, text, x, y, z=0, ro_x=0, ro_y=0, ro_z=0, locate=None,
                     scale=1, tran=500, pers=1000):
        """
        if you want to add slide, just use it! You can write HTML and use all the data attribute in impress.js!
        """
        slide = """
        <div class="step" data-x="%d" data-y="%d" data-z="%d"
         data-rotate-x="%d" data-rotate-y="%d" data-rotate-z="%d"
         data-scale="%d" data-transition-duration="%d" data-perspective="%d">
          %s
        </div>
        """ % (x, y, z, ro_x, ro_y, ro_z, scale, tran, pers, text)

        if locate is None:
            self.slides.append(slide)
        else:
            self.slides.insert(locate, slide)

    def overview(self):
        x = self.half_row
        y = self.half_col
        z = self.z

        slide = """
        <div class="step" id="overview" data-x="%d" data-y="%d" data-z="%d" data-scale="1" data-transition-duration="2000">
        </div>
        """ % (x, y, z)
        self.slides.insert(1, slide)

    def get_result(self):
        return part1 % self.music + "\n" + "\n".join(self.slides) + part2