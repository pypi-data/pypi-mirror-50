from lxml.etree import HTML as LXHTML
from lxml.etree import XML as LXML
from xdict.jprint import pdir,pobj
from nvhtml import txt
from nvhtml import lvsrch
from nvhtml import fs
from nvhtml import engine
from nvhtml import utils
import lxml.sax
import argparse
from efdir import fs
import elist.elist as elel
import estring.estring as eses
import spaint.spaint as spaint
from xml.sax.handler import ContentHandler

import copy
import re


####html to easy format
# #     comment
# -     attrib     属性有两种写法,直接跟或者当作子元素,换行的话会用空格连接
# .     text and tail
# |     text and tail content can multiline

####################################################################
#html
#    head
#        -id menu-item-27961
#        -class
#            qtranxs-lang-menu-item
#            qtranxs-lang-menu-item-ca
#            menu-item
#            menu-item-type-custom
#            menu-item-object-custom
#            menu-item-27961
#        .text
#            |hello
#            |hi
#            |hao
#            |hihihi
#        .tail
#            |this is a tail
#        meta
#            -http-equiv X-UA-Compatible
#            -content IE=edge,chrome=1
#        meta
#            -name viewport
#            -content
#                width=device-width,
#                user-scalable=yes,
#                initial-scale=1.0,
#                minimum-scale=1.0,
#                maximum-scale=3.0
#        meta
#            -http-equiv Content-Type
#            -content text/html; charset=UTF-8
#        link
#        link
#    body
#        div
#            li
#            li
#            li
#        div
#            li
#            li
#        div
#    #comment
#        .text
#            |this is a comment
####################################################################


INDENT = "    "

