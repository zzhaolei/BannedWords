#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64


# base64.b64encode()

with open("./pub_banned_words.txt", "r",encoding='utf-8') as f:
    with open("./encryption_banned_word.txt", "a",encoding='utf-8') as en:
        for i in f.readlines():
            en.write(base64.b64decode(i).decode('utf-8'))
