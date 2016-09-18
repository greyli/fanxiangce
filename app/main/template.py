# -*- coding: utf-8 -*-
__author__ = 'lihui'


"""
Hello, everyone!
Impress.py is a tool to make photo wall slides.
Powerd by impress.js and csshake.

usage:
    1. my_photo_wall = Impress()

----------------------------------------------
Copyright 2011-2012 li hui
----------------------------------------------
author: lihui
email: withlihui@gmail.com
website: withlihui.com
url:
source:
----------------------------------------------

impress.js@bartaz:
csshake@:
"""

# part1 and part2 is the html template of impress.js.
part1 = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1024">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <title>照片墙</title>
  <link rel="stylesheet" href="css/impress-demo.css">
  <link rel="stylesheet" href="css/csshake.css">
  <link rel="stylesheet" href="css/remodal.css">
  <link rel="stylesheet" href="css/remodal-default-theme.css">
  <link rel="stylesheet" href="css/photo.css">
  <link rel="stylesheet" href="css/hint.min.css">
</head>

<body class="impress-not-supported">

  <!--
  if user's browser can't supported impress, the message below will be show.
  -->

  <div class="fallback-message">
    <p>照片墙正在生成中，请耐心等待。但如果等了一分钟还没有跳转（暂不支持手机浏览器），很可能是你的浏览器太落后了，
    试一下下面这些浏览器吧(ง •̀_•́)ง<b>Chrome</b>, <b>Safari</b> or <b>Firefox</b></p><hr>
    <p>The photo wall is being generated, please wait... If the page didn't change after one minute, there must be
    something wrong about your browser, you better try this browser: <b>Chrome</b>, <b>Safari</b> or <b>Firefox</b>.</p>
  </div>

  <!--
  <div id="status" style="opacity: 0;">
    <progress max="100" value="0"></progress>
  </div>
  -->

  <div id="loader"></div>
  <div id="mask-bg"></div>

  <div id="mask-show">
    <div id="tips">图片资源正在努力加载，请稍候......</div>
  </div>

  <!--
  background music, default for autoplay and loop.
  -->
  <audio id="bg_music" autoplay loop>
    <source src="music/%s">
  </audio>

  <!--
  Four buttons: back to overview, about, play/ pause music, enter/quit fullscreen
  -->


  <a class="button" id="back" href="#overview"><span class="hint--bottom hint--info hint--small" aria-label="返回全景视图">全景</span></a>
  <a class="button" id="about" href="#info">关于</a>
  <input class="button" id="music_bt" onclick="playPause()" type="image" src="images/play.png" width="30" heigth="30">
  <input class="button" id="fullscreen" type="image" src="images/fullscreen.png" width="30" heigth="30" onclick="toggleFullScreen()">

  <div id="impress">
  <div id="image-container">
"""

part2 = """

      <div class="remodal-is-closed" style="display: none;">
      </div>
      <div class="remodal-wrapper remodal-is-closed" style="display: none;">
      <div class="remodal remodal-is-initialized remodal-is-closed" data-remodal-id="info">
      <button data-remodal-action="close" class="remodal-close"></button>
        <span align="center" style="font-size:40px;"><a href="http://fanxiangce.com" target="_blank"><b>
          <span style="color: #f79d00">翻</span>
          <span style="color: #8b3fb2">相</span>
          <span style="color: #4CAF50">册</span>
          </b></a></span><br><br><hr>
          <div style="font-size:20px; text-align:center left!important;">
            <br><span style="color: #008CBA">了解更多：</span> <a class="shake shake-slow" href="http://fanxiangce.com" target="_blank"><b>翻相册/fanxiangce.com</b></a><br>
            <br><span style="color: #f44336">联系方式：</span> <a class="shake shake"><b>withlihui@gmail.com</b></a><br>
            <br><span style="color: #555555">Powerd</span> by <a class="shake shake-opacity" href="https://elrumordelaluz.github.io/csshake/" target="_blank"><b>csshake</b></a> and
            <a class="shake shake-opacity" href="https://github.com/impress/impress.js" target="_blank"><b>impress.js</b></a><br>
          </div>
        <br>
        <a id="start-bt" href="#overview" data-remodal-action="close">返回</a>
        <a class="shake shake-hard" id="donate-bt" href="#pay">赞助</a>
      </div>
      </div>

      <div class="remodal-is-closed" style="display: none;">
      </div>
      <div class="remodal-wrapper remodal-is-closed" style="display: none;">
      <div class="remodal remodal-is-initialized remodal-is-closed" data-remodal-id="pay">
      <button data-remodal-action="close" class="remodal-close"></button>
          <div style="text-align: center;">
          <span align="center" style="font-size:20px">赞助我，让我做的更好</span>
      <hr>
      <br>
      <p>
      <img src="images/qr.png" width="175" height="175"><br>
      打开支付宝，扫描二维码即可付款，金额不限。
      </p>
      <br><br>
          </div>
          <div class="margin10" align="center"> <button class="remodal-confirm" data-remodal-action="close">好，我考虑下</button></div>
      </div>
      </div>
    </div>
  </div>

  <script src="js/jquery.min.js"></script>
  <script src="js/impress.js"></script>
  <script src="js/imagesloaded.js"></script>
  <script src="js/remodal.min.js"></script>
  <script src="js/photo.js"></script>
  <script>impress().init();</script>

</body>
</html>
"""
