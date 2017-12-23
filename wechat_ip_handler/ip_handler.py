#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

from wechatpy.messages import TextMessage
from wechatpy import create_reply, parse_message
from qqwry import QQwry


class CommandHandler:
    command = ''

    def check_match(self, message):
        if not isinstance(message, TextMessage):
            return False
        if not message.content.strip().lower().startswith(self.command):
            return False
        return True


class IPLocationHandler(CommandHandler):
    command = 'ip'

    def handle(self, message):
        if not self.check_match(message):
            return None
        ip = message.content.strip().lower()[1]
        pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        ip = pattern.search(message.content)
        if not ip:
            # msg = wechatpy.replies.TextReply(content='IP地址无效', message=message)
            reply = create_reply("IP地址无效", message)
            # print(reply)
            return reply
        q = QQwry()
        q.load_file('qqwry.dat')
        ip_locate = q.lookup(ip.group())
        # msg = wechatpy.replies.TextReply(content=ip_locate[0], message=message)
        reply = create_reply(ip_locate[0], message)
        # print(reply)
        return reply
        


# if __name__ == '__main__':
#     xml = '<xml>\n<ToUserName>\n<![CDATA[gh_ff39d444c0fc]]>\n</ToUserName>\n<FromUserName>\n<![CDATA[oCkcnt-sSI5ZF7jC92uBOCM7uEqI]]>\n</FromUserName>\n<CreateTime>1508673914</CreateTime>\n<MsgType>\n<![CDATA[text]]>\n</MsgType>\n<Content>\n<![CDATA[ip 180.97.33.108]]>\n</Content>\n<MsgId>6479705121392016106</MsgId>\n</xml>'
#     message = parse_message(xml)
#     cmd = IPLocationHandler()
#     cmd.handle(message)
