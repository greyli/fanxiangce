# -*- coding: utf-8 -*-
import os
from ..models import User, Role, Permission, Album, Photo
from generate import Impress

generator = Impress()
generator.slides = []

def wall():
    album = Album.query.get_or_404(95)
    photos = album.photos.order_by(Photo.timestamp.asc())
    files = []
    for photo in photos:
        files.append(photo.path)

    show_title = True
    imgs = []
    ## According the sum of images(multiple of 10, 10~100), use different layout: {sum: (col, row. height)}
    pos = {10: (2, 5, 5000), 20: (4, 5, 5000), 30: (5, 6, 5000), 40: (5, 8, 6000), 50: (5, 10, 7000),
           60: (6, 10, 8000), 70: (7,10, 8000), 80: (8, 10, 8000), 90: (9, 10, 9000), 100: (10, 10, 10000)}

    for pic in files:
        imgs.append(pic)

    # web
    #imgs = "[url=http://kekaoyun.com/bcbc7c3ca5c0a75c][img]http://i2.piimg.com/567591/1ba705c8e8011fa0.jpg[/img][/url][url=http://kekaoyun.com/bd5ec13d974cb282][img]http://i2.piimg.com/567591/d8f56dee8cd85292.jpg[/img][/url][url=http://kekaoyun.com/c4a4e84c130fb494][img]http://i2.piimg.com/567591/c7e626d9b4c9311e.jpg[/img][/url][url=http://kekaoyun.com/6035ce69c73b8c7e][img]http://i2.piimg.com/567591/e696d116d82baf1f.jpg[/img][/url][url=http://kekaoyun.com/541192f6c8f2efd8][img]http://i2.piimg.com/567591/9f3823c18d2c2bc4.jpg[/img][/url][url=http://kekaoyun.com/b1910c584af25c90][img]http://i2.piimg.com/567591/f710d08aa5b3e381.jpg[/img][/url][url=http://kekaoyun.com/ab65d8aac418333e][img]http://i2.piimg.com/567591/7127a81b8a3325e9.jpg[/img][/url][url=http://kekaoyun.com/c61fd2e839e5c8a6][img]http://i2.piimg.com/567591/21e61aae623e0d3d.jpg[/img][/url][url=http://kekaoyun.com/14f0fde1469713bc][img]http://i2.piimg.com/567591/038b10e465a37798.jpg[/img][/url][url=http://kekaoyun.com/2a7829ee5bac4b9a][img]http://i2.piimg.com/567591/6e622580f9b11d21.jpg[/img][/url][url=http://kekaoyun.com/ce988d37c6fd5c0e][img]http://i2.piimg.com/567591/af292caa22ba075e.jpg[/img][/url][url=http://kekaoyun.com/d0567d28b10962b0][img]http://i2.piimg.com/567591/f296eb161e5e1d8b.jpg[/img][/url][url=http://kekaoyun.com/6b6482c5662f0f1c][img]http://i2.piimg.com/567591/483797b749819530.jpg[/img][/url][url=http://kekaoyun.com/1f67e830a94bb08f][img]http://i2.piimg.com/567591/1c4fac9ad2db7bc2.jpg[/img][/url][url=http://kekaoyun.com/965058319bdb4377][img]http://i2.piimg.com/567591/9bbb57a230bbc43e.jpg[/img][/url][url=http://kekaoyun.com/0ca55e17373d00cb][img]http://i2.piimg.com/567591/40cb3d4188e61658.jpg[/img][/url][url=http://kekaoyun.com/0f07e56bd297b2cc][img]http://i2.piimg.com/567591/eddce987aa804cc9.jpg[/img][/url][url=http://kekaoyun.com/5681bdf9f2d17acf][img]http://i2.piimg.com/567591/1582eff962865fef.jpg[/img][/url][url=http://kekaoyun.com/77f01ce2769ac500][img]http://i2.piimg.com/567591/46a062540be0d61c.jpg[/img][/url][url=http://kekaoyun.com/e68cebcc8c8a4f40][img]http://i2.piimg.com/567591/175d8df1df5c2dd6.jpg[/img][/url][url=http://kekaoyun.com/ad3dc70e9994db97][img]http://i2.piimg.com/567591/b5b97bdf0a5ef7ae.jpg[/img][/url][url=http://kekaoyun.com/5cef8b2dc5c3d6a6][img]http://i2.piimg.com/567591/017a3c754af4a7f5.jpg[/img][/url][url=http://kekaoyun.com/f4e8db27062a8e95][img]http://i2.piimg.com/567591/972162eec3c6ec3f.jpg[/img][/url][url=http://kekaoyun.com/ee8dfcdc74a6754e][img]http://i2.piimg.com/567591/b4e3c8de44fd9c63.jpg[/img][/url][url=http://kekaoyun.com/607a07093e4c9c3a][img]http://i2.piimg.com/567591/500a62e71d8a9da2.jpg[/img][/url][url=http://kekaoyun.com/dd36877557926500][img]http://i2.piimg.com/567591/0557eb980e593e30.jpg[/img][/url][url=http://kekaoyun.com/56dd8dd4e1b9a1e2][img]http://i2.piimg.com/567591/18e5924961c36ae5.jpg[/img][/url][url=http://kekaoyun.com/5dc55fffe80fbb83][img]http://i2.piimg.com/567591/08ced14a14a11537.jpg[/img][/url][url=http://kekaoyun.com/e6f6b8ec4a4d96e5][img]http://i2.piimg.com/567591/5a38f0a45ff41cec.jpg[/img][/url][url=http://kekaoyun.com/07e1136b9f430081][img]http://i2.piimg.com/567591/532e7083df8c14da.jpg[/img][/url]"
    #photos = []
    #urls = []
    #for img in imgs.split("[/url]"):
    #    photos.append(img)
#
    #for photo in photos:
    #    url = photo.partition("[img]")[2]
    #    urls.append(url[:-6])
#
    pic_sum = len(imgs)
    print pic_sum
    for length in pos.keys():
        if pic_sum in range(length - 10, length):
            col, row, generator.z = pos[length-10]

    for y in range(300, 700*col, 700):
        for x in range(400, 900*row, 900):
            generator.create(imgs.pop(), x, y)

    # find the center of the image wall
    generator.half_row = 900 * row / 2
    generator.half_col = 700 * col / 2

    generator.overview()
    generator.bg_music("musssic.mp3")

    return generator.get_result()