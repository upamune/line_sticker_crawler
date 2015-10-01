#! /usr/bin/env python
# coding: utf-8
# vim: ft=python fenc=utf-8 ts=4 sw=4

import errno
import lxml
import lxml.html
import os
import sys
import urllib2


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def image_download(url, save_path):
    u = urllib2.urlopen(url)
    f = open(save_path, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (save_path, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,
    f.close()


# set url

url = ""

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    sys.exit("error: argument is missing\nEx: ./sticker_crawler.py `LINE_STICKER_URL`")

req = urllib2.Request(url)
html = urllib2.urlopen(req).read()
root = lxml.html.fromstring(html)

# fetch title
title = root.xpath('/html/body/div[1]/div/div[2]/section/div[1]/div[1]/div[2]/h3')[0].text

# mkdir to save stickers
save_path = u"stickers/" + title + u"/"
mkdir_p(save_path)

# fetch icon
main_icon_url = root.xpath('/html/body/div[1]/div/div[2]/section/div[1]/div[1]/div[1]/img')[0].attrib['src']
image_download(main_icon_url, save_path + "main_icon.png")

# fetch stickers
stickers = root.xpath('/html/body/div[1]/div/div[2]/section/div[1]/div[3]/div[2]/div/ul/li/div/span')
for idx, sticker in enumerate(stickers):
    style = sticker.attrib['style']
    start_pos = style.find('(') + 1
    end_pos = style.find(')')
    sticker_url = style[start_pos:end_pos]
    image_download(sticker_url, unicode(save_path) + unicode(idx) + u".png")
