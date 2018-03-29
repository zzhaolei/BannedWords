#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64


# base64.b64encode()

with open("./pub_banned_words.txt", "a") as f:
    with open("./encryption_banned_word.txt", "r") as en:
        for i in en.readlines():
            f.write(base64.b64decode(i))
