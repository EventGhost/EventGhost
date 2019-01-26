# -*- coding: utf-8 -*-

import requests


class Icon(object):

    def __init__(self, parent, url, node):
        self.__parent = parent
        self.mime_type = None
        self.width = None
        self.height = None
        self.depth = None
        self.url = None

        for item in node:
            tag = item.tag
            try:
                text = int(item.text)
            except ValueError:
                text = item.text

            if tag == 'url':
                name = text.split('/')[-1]
                name = name.replace('.', '_')
                self.__name__ = name
                text = url + text

            setattr(self, tag, text)

    @property
    def data(self):
        return requests.get(self.url).content

    @property
    def access_point(self):
        return self.__parent.access_point + '.' + self.__name__

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            access_point=self.access_point,
            name=self.__name__,
            mime_type=self.mime_type,
            width=self.width,
            height=self.height,
            depth=self.depth,
            url=self.url,
        )

        return output


TEMPLATE = '''
{indent}Icon name: {name}
{indent}Access point: {access_point}
{indent}----------------------------------------------
{indent}    Mime Type: {mime_type}
{indent}    Width: {width}
{indent}    Height: {height}
{indent}    Color Depth: {depth}
{indent}    URL: {url}
'''
