# coding=utf8

import email.parser
import re
from email.header import decode_header
from email.utils import parseaddr


my_parser = email.parser.Parser()


def decode_section(sect, coding=None):
    # TODO: chardet ? (topic2k)

    cp_list = ('utf-8', 'iso-8859-1', 'us-ascii')
    if coding:
        cp_list = (coding,) + cp_list
    for char_set in cp_list:
        try:
            sect = sect.decode(char_set, 'strict')
        except UnicodeError:
            pass
        else:
            return sect.strip(' "')

    for char_set in cp_list:
        try:
            sect = sect.decode(char_set, 'replace')
        except UnicodeError:
            pass
        else:
            return sect.strip(' "')
    return u''


def get_parts(msg, ext=False):
    from email.iterators import typed_subpart_iterator

    def get_charset(part, default="ascii"):
        """Get the part charset"""
        if part.get_content_charset():
            return part.get_content_charset()
        if part.get_charset():
            return part.get_charset()
        return default

    def get_body(message):
        """Get the body of the email message"""

        # TODO : option choice for html part viewing

        if message.is_multipart():
            # get the text (plain or html) version only
            text_parts = [
                part for part in typed_subpart_iterator(message, 'text')
            ]
            body = []
            for part in text_parts:
                charset = get_charset(part, get_charset(message))
                try:
                    body.append(
                        unicode(
                            part.get_payload(decode=True),
                            charset,
                            "replace"
                        )
                    )
                except UnicodeError:
                    body.append(
                        unicode(
                            part.get_payload(decode=True),
                            'us-ascii',
                            "replace"
                        )
                    )
            return u"\n".join(body).strip() + u"\n"

        else:
            # if it is not multipart, the payload will be a string
            # representing the message body
            try:
                body = unicode(
                    message.get_payload(decode=True),
                    get_charset(message),
                    "replace"
                )
            except UnicodeError:
                body = unicode(
                    message.get_payload(decode=True),
                    'us-ascii',
                    "replace"
                )
            return body.strip() + u"\n"

    if not ext:
        return [parse_item(msg['Subject']), msg['From'], get_body(msg)]
    else:
        return [
            parse_item(msg['Subject']),
            msg['From'],
            get_body(msg),
            None,
            None,
            msg['References'],
            msg['Reply-To'],
            msg['Message-ID'],
            msg['X-Original-To'] if 'X-Original-To' in msg else parseaddr(msg['To'])[1],
        ]


def move_item(lst, index, direction):
    tmp_list = lst[:]
    max_idx = len(lst) - 1
    # Last to first position, other down
    if index == max_idx and direction == 1:
        tmp_list[1:] = lst[:-1]
        tmp_list[0] = lst[max_idx]
        index2 = 0
    # First to last position, other up
    elif index == 0 and direction == -1:
        tmp_list[:-1] = lst[1:]
        tmp_list[max_idx] = lst[0]
        index2 = max_idx
    else:
        index2 = index + direction
        tmp_list[index] = lst[index2]
        tmp_list[index2] = lst[index]
    return index2, tmp_list


def parse_address(item):
    parse_addr = parseaddr(item)
    if parse_addr[0] == '':
        return parse_addr[1]
    dec_addr = decode_header(parse_addr[0])[0]
    if not dec_addr[1]:
        return parse_addr[0]
    else:
        return decode_section(dec_addr[0], dec_addr[1])


def parse_item(item):
    x = decode_header(item)[0]
    if x[1]:
        return decode_section(x[0], x[1])
    else:
        return x[0]


def run_email_client():
    """
    Get the path of default email client through querying the
    Windows registry.
    """
    import webbrowser
    webbrowser.open('mailto:')


regex = r"^([a-z0-9_\-.+]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)" \
        r"|(([a-z0-9\-]+\.)+))([a-z]{2,4}|[0-9]{1,3})(\]?)$"
rex = re.compile(regex, re.IGNORECASE)


def validate_email_addr(email_addr):
    return bool(rex.match(email_addr))
