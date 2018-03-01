# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

# ------------------------- BEGIN SLIDER CODE  ---------------------

import wx
from cStringIO import StringIO
from PIL import Image

LEFT_THUMB = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x13\x00\x00\x00\x0B\x08\x06\x00\x00\x00\x9D\xD5\xB6\x3A\x00\x00\x01'
    '\x2E\x49\x44\x41\x54\x78\x9C\x95\xD2\x31\x6B\xC2\x40\x00\x05\xE0\x77\x10'
    '\x42\x09\x34\xD0\x29\x21\x82\xC9\x9C\x2E\x72\x4B\x87\x40\x50\xB9\xBF\x5B'
    '\x28\x35\xA1\xA4\x94\x76\x68\x1C\x1C\x74\xCD\x9A\xE8\x20\x0A\x12\xA5\x5A'
    '\xE4\x72\xC9\x75\x10\x6D\xDC\xCE\xF7\x03\x3E\xDE\x83\x47\xA4\x94\x68\x67'
    '\xB5\xD9\x4E\xBF\xBF\x3E\xE8\x78\x3C\x86\x6A\x3C\xCF\x43\x10\x04\x20\x6D'
    '\x6C\xB5\xD9\x4E\x93\xF8\x95\x5A\x96\x05\xC6\x98\x32\x56\x14\x05\x46\xA3'
    '\x11\xB4\x36\x14\xBD\x3C\xD3\x4E\xA7\x03\xC6\x18\x8E\xC7\x23\x9A\xA6\x51'
    '\xC2\x5C\xD7\x45\x9E\xE7\x27\xEC\x0C\x39\x8E\x03\xC6\x18\x0E\x87\x83\x32'
    '\x04\x00\xE7\x75\x1A\xE7\x7C\xF2\xF9\xFE\x46\x6D\xDB\x06\x63\x0C\xFB\xFD'
    '\x1E\x75\x5D\x2B\x43\x57\x58\xF9\xF3\xAB\xAD\xD7\x6B\x98\xA6\x09\x21\x04'
    '\x76\xBB\x1D\x84\x10\x37\x61\x86\x61\x9C\x30\x00\x70\x1C\x07\x49\x92\x80'
    '\x10\x82\x7E\xBF\x8F\xE5\x72\x79\x13\x78\x69\xF6\x70\x6F\x88\x5E\xAF\x37'
    '\x2B\xCB\x92\xC6\x71\x0C\x42\x08\xC2\x30\xC4\x7C\x3E\x57\x06\x2F\x98\xAE'
    '\xEB\x4F\xAE\xEB\x4E\x06\x83\xC1\x4C\x4A\x49\xA3\x28\x82\x94\x12\x61\x18'
    '\x2A\x37\x5B\x2C\x16\xE8\x76\xBB\xFF\x3F\xE3\x9C\x4F\x8A\xA2\xD0\xD2\x34'
    '\xA5\x59\x96\xA1\xAA\x2A\x65\xCC\xB2\x2C\x0C\x87\xC3\xEB\xD3\x9E\xC1\xAA'
    '\xAA\xEE\x38\xE7\x4A\x90\xAE\xEB\x00\x00\xDF\xF7\x1F\xFF\x00\x09\x7C\xA7'
    '\x93\xB1\xFB\xFA\x11\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82'
)

LEFT_THUMB_ACTIVE = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x13\x00\x00\x00\x0B\x08\x06\x00\x00\x00\x9D\xD5\xB6\x3A\x00\x00\x01'
    '\x62\x49\x44\x41\x54\x78\x9C\x95\xD2\x4D\x4B\x02\x51\x18\x05\xE0\x63\x0C'
    '\x83\x04\x81\x42\x69\x63\xA5\x48\xB6\x31\x2C\x1B\xA2\x11\xA2\x22\xDC\x64'
    '\x2D\x5B\xB4\x68\x21\xD1\xBE\x5F\x12\x45\xDB\x6A\xD3\xAE\x88\x16\x45\xA0'
    '\x41\x11\x25\x11\x46\x8A\xB5\xAA\x85\xC8\x40\x0C\x4D\xE0\x47\x94\x96\xF7'
    '\xCE\x78\x5B\x4C\x1F\xB6\xEA\x76\x7E\xC0\xF3\x9E\x03\xAF\x8D\x31\x86\xE6'
    '\xE8\xC5\x4A\x66\x23\x71\x2D\xEF\x9C\xE6\xC0\x9B\xC1\x5E\x0F\xE6\x26\xC3'
    '\xB0\x35\x63\x7A\xB1\x92\x59\xDB\x3B\x97\xBD\x92\x0B\x8B\x33\x0A\x37\x76'
    '\x9B\xD7\xB0\xBA\x7B\x06\xA1\x19\x5A\xDE\x3E\x91\xBD\x5D\x12\xE2\x31\x05'
    '\x5A\xCD\x84\xD1\xE0\xC3\x82\x7E\x0F\x6E\xF2\x9A\x85\x7D\x41\xDD\x1E\x09'
    '\xF1\xE9\x08\xEE\xCA\x06\xEA\x26\xFB\xCB\xF8\x4E\x87\xBD\x05\x00\x20\x10'
    '\x42\xD2\x9B\x87\x17\xB2\xAB\xD3\x8D\xF9\x58\x04\x57\x3A\x41\xD5\xE0\x87'
    '\x00\x20\xD0\xB0\x06\x0A\xE5\x97\x9A\xA0\x3F\xEA\xE8\x09\x38\x40\x4D\x86'
    '\xD2\xBB\x89\x57\xFA\x3F\x8C\x7E\xAE\x10\x00\x40\xF1\x3B\xB0\x95\x4C\x82'
    '\x9A\x0C\xB3\xD1\x61\xAC\x67\x9F\xF0\x5C\x37\xB9\xB1\x51\xB7\x64\x61\xCE'
    '\xB6\x56\x63\x64\x28\x94\x2D\x96\xCA\xF2\x7E\x32\x01\xC6\x18\x16\x26\xC2'
    '\x58\x49\x15\x50\x7E\xA3\x7C\xCD\x68\xBB\x85\x89\xA2\xA8\xF8\x7C\xBE\x74'
    '\x2C\x3A\x9E\x65\x8C\xC9\x07\x47\x49\x34\x1A\x26\x96\xC6\x06\xB8\x9B\xDD'
    '\xAB\x1A\x42\x7E\xE9\xE7\xCF\x08\x21\x69\x55\x55\x85\xE3\xD4\xA5\x9C\xC8'
    '\x3D\xA0\x50\x15\xB9\xB1\x3E\x8F\x13\xF1\x29\xE5\xF7\xD3\x7E\x81\x94\x52'
    '\x3B\x21\x84\x0B\x12\x45\xEB\x68\x30\x18\xEC\xFF\x00\xCE\xA5\xA4\xC6\x64'
    '\xB3\xEF\x63\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82'
)

RIGHT_THUMB = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x13\x00\x00\x00\x0B\x08\x06\x00\x00\x00\x9D\xD5\xB6\x3A\x00\x00\x01'
    '\x3A\x49\x44\x41\x54\x78\x9C\x95\xD1\xB1\x6A\xC2\x50\x14\xC6\xF1\xBF\x92'
    '\x44\x28\x14\x5A\x8A\x36\x38\x18\x1C\x5D\x54\xEC\xD0\x41\x33\x04\xEE\x03'
    '\xFA\x0A\x3E\x40\xA1\x43\xA5\xDA\x21\xE2\xE0\x10\x44\xB7\xBA\x09\x01\x97'
    '\x46\x5A\x0C\x54\x43\x88\x57\x6E\x87\x92\x52\xB7\xEB\x85\x6F\xB9\x07\x7E'
    '\x7C\x87\x53\x98\xCF\xE7\x6A\x36\x9B\x11\x86\x21\xBA\xAF\xDB\xED\xE2\x7A'
    '\x62\x79\x7F\x77\xF3\x70\x36\xE8\xF7\xFB\x6A\xBD\x5E\x2B\x29\xA5\x76\x46'
    '\xA3\x91\x1A\x0C\x06\xEA\xE3\x73\xB7\x50\x4A\x91\xA7\x18\x86\x21\x8E\xE3'
    '\x90\x24\x89\x56\xD2\x34\x45\x08\x41\xA5\x52\xE1\xE5\xF9\xA9\x13\x7D\xC5'
    '\x8B\xBC\x58\x11\x40\x29\xC5\xE9\x74\xD2\xCA\xF1\x78\xE4\x70\x38\x20\x84'
    '\xA0\x5A\xAD\x9E\x81\x17\x63\x39\xB8\xDF\xEF\x11\x42\x60\xDB\x36\xFE\xDB'
    '\x6B\x27\xCB\xB2\xC0\x00\x90\x52\x12\xC7\xB1\xF6\x01\x00\x0C\xC3\xA0\x54'
    '\x2A\x01\xB0\xDD\x6E\xD9\x7D\x27\x86\x91\x37\x93\x52\x5E\x04\x95\xCB\x65'
    '\x26\x93\x09\xE3\xF1\x18\xD7\x75\x7F\xFF\x73\x2C\xCB\x32\x6D\xC8\xB6\x6D'
    '\xA6\xD3\x29\xC3\xE1\x90\x56\xAB\x45\xBB\xDD\x5E\xDE\x5E\x5F\x49\xA3\x56'
    '\xAB\xB1\xD9\x6C\xA8\xD7\xEB\xDA\xCD\x72\xA8\xD9\x6C\xE2\x79\xDE\xD2\x71'
    '\x1C\x69\x59\xD6\x63\x21\x08\x02\xE5\xFB\x3E\x51\x14\x69\x63\xA6\x69\xD2'
    '\x68\x34\xE8\xF5\x7A\x7F\x10\x40\x41\x29\xC5\x6A\xB5\x7A\x07\xB4\x57\xB5'
    '\x2C\x0B\xD3\x34\xD3\xFF\x10\xC0\x0F\x69\x21\x1F\x08\x32\x77\xE9\x5A\x00'
    '\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82'
)

RIGHT_THUMB_ACTIVE = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x13\x00\x00\x00\x0B\x08\x06\x00\x00\x00\x9D\xD5\xB6\x3A\x00\x00\x01'
    '\x7C\x49\x44\x41\x54\x78\x9C\x95\x8F\xCF\x2B\xA4\x71\x1C\xC7\x5F\x0F\xCF'
    '\xF3\xB0\x24\xA4\xC8\xA6\xA6\xC7\x79\x15\xE3\xE7\x1E\x28\x6B\x1D\xC6\x81'
    '\x23\x72\x90\x2D\xFE\x01\x1C\x9C\xF6\xE4\xC4\x5D\x4A\xC9\x41\x51\xCA\x12'
    '\x45\xB3\x7E\x1C\xD6\x4C\x7E\xCC\x44\x32\x2D\x1B\x65\x63\x98\x18\x23\x34'
    '\x3B\x9E\x67\x9E\xE7\xEB\x82\xD6\xED\xEB\x5D\xAF\xD3\xA7\x5E\xBD\x3E\xCA'
    '\xBC\xEF\x40\x4C\xAF\xED\xB2\x77\x1C\x46\x76\xAD\xF5\xA5\x74\x7B\x2A\x82'
    '\x05\x79\x39\xE5\x6F\x0E\x1D\x83\x93\x62\xE7\xE8\x4C\x98\xB6\x23\xCD\xC8'
    '\xBC\x5F\x0C\x8C\xCE\x89\xCB\xEB\x58\x40\x08\xC1\x0B\xCA\xA7\x6F\x43\x62'
    '\x6B\xB4\x97\x70\xDC\x96\xAA\x52\x53\x20\x3F\x3D\x95\xB1\x05\x3F\x7F\xCF'
    '\x2F\xE8\x6B\x6B\x78\x2D\x4C\x01\xB0\x1C\xC1\x55\xDC\x91\xE2\xE2\xC1\xE1'
    '\x77\x2C\x49\x67\x53\x0D\x45\x1F\x0B\x19\x9E\x5A\x71\x47\xA2\xB7\x01\x00'
    '\x15\xC0\x74\x20\xF2\x4F\xAE\xEC\x65\xD1\x84\x4D\x87\xA7\x86\xF1\x45\x1F'
    '\x63\x0B\x1B\xEE\xFE\xF6\xC6\x4D\x15\xC0\xB2\x05\xD1\x77\xCA\x1E\x35\x05'
    '\xCB\x16\x80\x42\xE4\x32\x42\xEC\x3E\xAE\xAA\x00\x77\x09\x0B\xDF\xC9\x95'
    '\xB4\x28\x3B\x2D\x95\x1E\x77\x3E\xE3\x8B\x7E\xD6\xBD\xCB\x74\x36\x96\x01'
    '\xCF\x6F\x5A\x96\x45\xF4\xE6\x46\x4A\x94\xFB\x41\xA3\xAB\xC2\x60\xE6\xE7'
    '\x36\xAB\xCB\x4B\xB4\x54\x15\x53\x55\x56\x12\xCC\xCD\xCA\x48\xAA\x25\x46'
    '\x21\x87\xA7\x61\xBE\x7F\x31\xA4\xCB\x66\xD7\x02\xAC\x7B\xBD\x34\x57\x1A'
    '\x78\x1A\xEA\x82\x2E\x97\x2B\xA9\xEB\x7A\xB5\xF2\xE3\xD7\xBE\x98\x58\xDA'
    '\xE4\x4F\x38\x26\x2D\x33\x32\x4D\x3C\xA5\x45\x7C\xAD\xFD\xFC\x2A\x02\x50'
    '\x84\x10\x84\x42\xA1\x03\x00\xD3\x34\xA5\x64\xBA\xAE\xA3\x69\x5A\xE2\x7F'
    '\x11\xC0\x13\xE5\xFC\xE6\x0A\x0E\xDD\x66\x24\x00\x00\x00\x00\x49\x45\x4E'
    '\x44\xAE\x42\x60\x82'
)

TOP_THUMB = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x0B\x00\x00\x00\x13\x08\x06\x00\x00\x00\x46\x29\xF7\xD0\x00\x00\x01'
    '\x37\x49\x44\x41\x54\x78\x9C\xB5\x92\xA1\x8E\xC2\x40\x10\x86\xFF\x6D\x6B'
    '\x08\x4D\xFA\x02\x08\x08\xA8\xC3\x63\xAA\xF6\x59\x78\x2D\xDE\xA0\x8A\x20'
    '\xA8\x21\x28\x04\x68\x40\xA1\xA8\x20\xA9\x00\xC2\x36\xAD\xE8\x0E\xFF\x09'
    '\xD2\x4B\x0F\xCA\xE5\x4E\xDC\x27\x27\xDF\xCC\xFC\xBB\x19\x45\x12\x15\x97'
    '\xCB\x65\xBD\xD9\x6C\x46\x00\x10\x86\xE1\xDE\xF7\xFD\x21\x6A\x38\x75\x71'
    '\xB1\x58\x8C\x44\x04\x22\x82\xE9\x74\xFA\x91\x65\xD9\xAE\x2E\x83\x24\xCE'
    '\xE7\xF3\x3A\x8A\x22\xCE\xE7\x73\x5A\x6B\x69\xAD\x65\x1C\xC7\x9C\x4C\x26'
    '\x34\xC6\xEC\x48\x82\x24\xBE\xC4\x38\x8E\x59\x96\x25\x8D\x31\x34\xC6\xB0'
    '\x2C\xCB\x97\x06\x15\x45\x11\x83\x20\x80\xD6\x1A\x45\x51\xE0\x7E\xBF\x3F'
    '\xF2\x39\x0E\x5A\xAD\x16\x96\xCB\x25\x8E\xC7\x23\xC6\xE3\xB1\x72\x56\xAB'
    '\x15\xB4\xD6\xC8\xF3\x1C\x22\x82\x6A\xA5\x88\x20\xCF\x73\x68\xAD\xB1\xDD'
    '\x6E\x91\x65\xD9\xCE\xAB\xB2\x8B\x08\x9E\xA9\xD7\x0E\x87\x03\xBC\xEA\x91'
    '\xD5\xFA\x67\xEA\x5F\xEB\x35\x15\xDF\xE1\x01\x80\xB5\x16\xD7\xEB\xB5\x51'
    '\x68\xB7\xDB\xDF\xE5\x3F\xC7\x78\x27\xBF\xC4\x78\x9E\xF0\xA3\xFC\x7F\x31'
    '\x7E\x3D\xB9\xDB\xED\x22\x49\x12\xF4\xFB\xFD\x46\x39\x49\x12\x28\xA5\x1E'
    '\x72\x18\x86\x98\xCD\x66\x38\x9D\x4E\x8D\xB2\x52\x0A\x9D\x4E\x07\x83\xC1'
    '\x00\x8A\x24\x8A\xA2\x60\x9A\xA6\xB8\xDD\x6E\x2F\x37\xE2\xBA\x2E\x7A\xBD'
    '\xDE\xDE\xF7\xFD\xE1\x27\x77\xEF\xEE\x6C\xDC\x06\xF4\x56\x00\x00\x00\x00'
    '\x49\x45\x4E\x44\xAE\x42\x60\x82'
)

TOP_THUMB_ACTIVE = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x0B\x00\x00\x00\x13\x08\x06\x00\x00\x00\x46\x29\xF7\xD0\x00\x00\x01'
    '\x8B\x49\x44\x41\x54\x78\x9C\x8D\xD2\x3F\x4B\x23\x51\x14\x05\xF0\x33\x99'
    '\xA4\x1B\x31\xB0\x95\x0B\x16\xD1\x54\x8A\xEC\x82\x18\x6C\xB6\xD0\x46\x7B'
    '\x0B\x8B\x88\x5F\xC0\xD6\x6F\x60\xB5\x58\x58\xB8\xD9\x0F\xA0\x55\xC0\x62'
    '\xB3\x20\x04\x2C\x44\x44\x34\xC2\xAE\x36\x91\x10\x82\x7F\xA2\x08\x06\x36'
    '\x23\x99\xC9\x4C\xB2\x6F\xDE\x3D\x16\xB2\x6E\x06\x27\x90\x53\xBD\xE2\xF7'
    '\x2E\xE7\xC2\x35\x48\xE2\x5F\x6C\xDB\x2E\xE5\x8F\x2B\x19\x00\x58\x99\x9F'
    '\xBA\xB2\x2C\x6B\x12\x3D\x89\xF5\xC2\xDC\xFE\xAF\x8C\x12\x81\x12\xC1\xD7'
    '\xFC\xD1\x84\xEB\xBA\xE5\x5E\x0C\x92\x68\x36\x9B\xA5\x8D\xDD\x03\x6E\xFF'
    '\x38\x61\x27\x10\x76\x02\xE1\xF7\x9F\xA7\x5C\xFF\xB6\x47\xC7\x71\xCA\x24'
    '\x41\x12\x6F\x30\x57\x38\xA5\xA7\x84\x77\x4E\xC0\x5B\x47\xD1\x53\xC2\x5C'
    '\x21\xFC\xC1\xD8\xD8\x3D\xE0\x87\xE1\x21\xAC\x2E\x66\x70\xEF\x6A\x28\x79'
    '\xDD\x21\x11\x33\x30\x6A\x99\xD8\x29\x9E\xE3\xBA\xFE\x80\xCD\xB5\x25\x23'
    '\x96\x3F\xBC\x44\x76\x61\x06\x15\x3B\xC0\x73\x57\xD0\x56\x44\x5B\x11\xCF'
    '\x5D\x41\xC5\x0E\x90\x5D\x98\x41\xF1\xF7\x0D\x5C\xD7\x2D\xC7\x01\x40\x13'
    '\xB0\xBB\x1A\x51\xD1\x34\x01\x00\xB5\x5A\x0D\x6F\xB8\x1D\xB0\x0F\xFE\xFF'
    '\x8E\x03\x80\x08\xE1\x29\x89\xC4\x22\x0C\x63\x4D\xC0\x1F\x74\xB2\xFB\x37'
    '\xC0\xC5\x63\x2B\x12\x7F\x19\x49\xBC\xAF\xE1\x77\xBA\x83\xD5\x10\xD1\xF0'
    '\x7D\xBF\x0F\xD6\x61\xAC\xB5\xC0\xEB\x83\xB5\x96\x30\x16\x11\x78\x9E\xD7'
    '\x67\xF2\x3B\xAC\xD1\x19\xA4\xC6\xA7\xF1\x8F\xA8\xD6\x9F\xB0\xB5\x34\x1D'
    '\x89\xAB\xF5\x27\x24\xE3\xEA\x15\x2F\xCF\x7D\xC6\x4E\xF1\x0C\x95\x87\x3F'
    '\x91\x38\x19\x57\x98\x1D\x4B\x22\x9D\x4E\xC3\x20\x09\xDF\xF7\xD9\x68\x34'
    '\xD0\x6A\xB5\xA0\x75\xF8\x46\x4C\xD3\x44\x2A\x95\xBA\xB2\x2C\x6B\xF2\x05'
    '\xC8\xC0\x03\xCE\x1B\x4B\x04\x3A\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42'
    '\x60\x82'
)

BOTTOM_THUMB = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x0B\x00\x00\x00\x13\x08\x06\x00\x00\x00\x46\x29\xF7\xD0\x00\x00\x01'
    '\x55\x49\x44\x41\x54\x78\x9C\xB5\xD1\xC1\x6B\x1A\x41\x14\xC7\xF1\xEF\xEE'
    '\x73\xDD\x52\xE9\x21\x17\x91\xD9\xC3\x78\x15\x44\x90\x1C\x5A\x58\x82\x08'
    '\xB9\x89\xFF\xA9\x85\x1C\x2C\x56\xE8\x61\xE7\xB0\x87\x62\xDA\x53\xFF\x80'
    '\xF5\x10\x14\x56\x50\x08\x48\x94\x65\x26\x87\xB0\x76\x03\x9B\x42\x0E\x7D'
    '\x30\x30\xBC\xF9\xCC\xE3\x37\x8C\xB7\x5A\xAD\x5C\x9A\xA6\x64\x59\x46\x5D'
    '\x75\xBB\x5D\xE2\x38\xE6\xE1\xF4\xC1\x6F\xA4\x69\xCA\x74\x3A\x45\x6B\x5D'
    '\x8B\xD7\xEB\x35\xB3\xD9\x8C\xC9\x64\xF2\xA7\x91\x65\x19\x5A\x6B\x8E\xC7'
    '\x63\x2D\xD6\x5A\xB3\xD9\x6C\x00\x68\x00\x38\xE7\x70\xCE\xD5\xE2\xB2\x7F'
    '\x3E\x9F\x5F\x70\xB5\xF9\xAF\xFA\xCF\xD8\x39\x87\xB5\xB6\x16\x54\x87\xBC'
    '\x7F\x72\x51\x14\x1C\x0E\x87\x5A\xD0\x6A\xB5\xDE\x1F\xC3\xF3\xBC\xBF\x31'
    '\xDE\xC2\xD5\xF2\xCB\x8D\x88\x5C\x3E\xA7\x5C\x22\xF2\x1A\xC7\x71\x8C\x31'
    '\x06\xA5\x14\x22\x82\xB5\x16\x6B\x2D\x22\x82\x52\x0A\x63\x0C\x41\x10\xD0'
    '\x6C\x36\xF1\x6F\xC6\xB7\xBF\xF2\x3C\x27\x49\x12\xA2\x28\x42\x44\x10\x11'
    '\xA2\x28\x22\x49\x12\xE6\xF3\x39\xBD\x5E\x8F\x20\x08\x9E\x3C\x80\xED\x6E'
    '\x7F\x3F\xBF\xFB\x7A\xDD\xE9\x74\x18\x8D\x46\x00\x18\x63\x58\x2C\x16\x0C'
    '\x06\x03\xC6\xE3\xF1\x6F\xAD\x75\xE1\x95\x79\xCA\x0B\xED\x76\x1B\xDF\xF7'
    '\x59\x2E\x97\xF4\xFB\xFD\x0B\x0C\xC3\xF0\xB3\x57\x7D\xC0\x76\xB7\xBF\xFF'
    '\xF1\xFD\xDB\x75\x9E\xE7\x28\xA5\x18\x0E\x87\x17\x08\xF0\x0A\x03\x9C\x4E'
    '\xA7\x9F\xFB\xC7\x63\x03\x70\x57\x9F\x3E\x16\x61\x18\x7E\x29\xCF\x9E\x01'
    '\x6D\xF9\xA5\xD9\x81\x2C\xF3\x97\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42'
    '\x60\x82'
)

BOTTOM_THUMB_ACTIVE = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x0B\x00\x00\x00\x13\x08\x06\x00\x00\x00\x46\x29\xF7\xD0\x00\x00\x01'
    '\x92\x49\x44\x41\x54\x78\x9C\x8D\x8F\x3B\x4B\x63\x41\x18\x40\xCF\x1D\x92'
    '\x5C\xDD\xC4\x67\x97\xB0\x18\x1F\xAD\x68\x20\x3E\x8B\x15\x64\xAB\xC0\xE2'
    '\x36\x82\x85\xB5\x85\xE0\x6F\xB0\xB3\xF3\x17\x6C\x61\x27\x68\x13\xD0\x4A'
    '\x0B\x93\x65\x05\x41\x48\xE2\x06\x22\x88\x60\x17\x82\xF8\x20\xEB\x23\xF7'
    '\x26\x37\x77\x66\x6C\x4C\x5C\xF5\x46\x1C\x98\x62\xBE\x39\x73\x38\x63\xEC'
    '\x1E\x9D\xEA\xED\xF4\x5F\xF2\x17\x25\xBC\xD6\xE8\x50\x84\x85\xD9\x18\x4A'
    '\x29\xC1\xE2\xDA\xA6\xCE\x9C\x17\xB5\x23\x95\xE7\xCE\x9C\x17\xF5\xFC\xEA'
    '\x86\x2E\x14\x0A\xA7\xBE\xFC\x45\x89\xE1\xC1\x08\xD7\xB6\xF2\x34\x0F\x0F'
    '\x46\x38\x2B\xDE\x02\xE0\x03\x50\x1A\x6C\xA9\x3D\x61\xF5\x3C\x76\x1C\xE7'
    '\x05\xB6\xEA\x1F\xC3\x4D\xB3\xD4\x9A\x4A\x0B\x58\x6A\xFD\x16\x86\xC7\xBA'
    '\x77\xB3\x7C\x6F\x86\x8A\xDB\xCA\xFC\x06\x56\x4A\x63\xB5\x30\x2B\xE5\x91'
    '\x61\x7F\xD6\xFC\xE8\xB8\x9C\x94\xEE\x3D\xE1\x6F\x61\x3F\x00\x86\x61\xBC'
    '\x64\xD8\xD5\xDA\xE7\x32\x94\x92\x98\xBA\xCE\xBF\xAA\xFB\x0A\xEC\x6E\xF3'
    '\xA1\x94\x6C\x9E\xC5\xC2\x6C\x8C\x64\x2A\xC7\xF2\x78\x98\xA0\x90\x58\xB6'
    '\x8D\x65\xDB\x04\x85\x64\x79\x3C\x4C\x32\x95\x63\x20\xE8\x10\x08\x04\x10'
    '\x4B\x89\xB1\x6C\xE5\xAE\x4C\x32\x9D\x65\x65\xBA\x8F\x90\x90\x84\x84\x64'
    '\x65\xBA\x8F\x64\x3A\x4B\x6A\x7F\x8F\x44\xEC\x2B\x7E\xBF\xBF\x6A\x00\x5C'
    '\xDE\x94\x33\xEB\x5B\x07\xF1\x50\x4F\x2F\x3F\x67\x46\x01\xD8\xF9\x93\xE7'
    '\x30\x75\xC0\xDC\xD8\x00\x89\xEF\x33\xB9\x68\x34\xEA\x1A\x8D\x9E\xC6\x83'
    '\xF6\xCE\x6E\x84\x30\x38\xFA\x9D\xE6\x47\xBC\xBF\x09\x9A\xA6\x39\x69\xFC'
    '\xFF\xA1\xCB\x9B\x72\xE6\xD7\xEE\x61\xFC\xEA\xEA\x9A\x89\x68\x17\x53\xF1'
    '\x91\x26\x08\xF0\x0A\x06\xA8\xD5\x6A\xC7\xE5\x07\xCB\x07\xE8\x9E\x8E\x2F'
    '\xAE\x69\x9A\x53\x8D\xBB\x27\x3A\xE9\xDD\x50\xEC\x2B\xA7\x04\x00\x00\x00'
    '\x00\x49\x45\x4E\x44\xAE\x42\x60\x82'
)

NUMBER_CODES = {
    wx.WXK_NUMPAD0: 0,
    wx.WXK_NUMPAD1: 1,
    wx.WXK_NUMPAD2: 2,
    wx.WXK_NUMPAD3: 3,
    wx.WXK_NUMPAD4: 4,
    wx.WXK_NUMPAD5: 5,
    wx.WXK_NUMPAD6: 6,
    wx.WXK_NUMPAD7: 7,
    wx.WXK_NUMPAD8: 8,
    wx.WXK_NUMPAD9: 9
}
NUMBER_CODES.update({i + 48: i for i in range(10)})

PAGE_CODES = (
    wx.WXK_PAGEUP,
    wx.WXK_NUMPAD_PAGEUP,
    wx.WXK_PAGEDOWN,
    wx.WXK_NUMPAD_PAGEDOWN
)

DIRECTION_CODES = (
    wx.WXK_RIGHT,
    wx.WXK_NUMPAD_RIGHT,
    wx.WXK_UP,
    wx.WXK_NUMPAD_UP,
    wx.WXK_LEFT,
    wx.WXK_NUMPAD_LEFT,
    wx.WXK_DOWN,
    wx.WXK_NUMPAD_DOWN
)


def GetBitmap(pngData):
    pil = GetImage(pngData)
    return wx.BitmapFromBufferRGBA(
        pil.size[0],
        pil.size[1],
        str(pil.tobytes())
    )


def GetImage(pngData):
    stream = StringIO(pngData)
    pil = Image.open(stream).convert("RGBA")
    stream.close()
    return pil

def CheckColour(colour):
    if isinstance(colour, wx.Colour):
        return colour.Red(), colour.Green(), colour.Blue()
    else:
        return colour


class SliderHandler(object):
    """
    Cache object for FloatSliderCtrl

    This object holds the data for the various parts of the float slider.
    The object will do calculations when necessary and record the results and
    when those results are needed are handed back. If something gets changed
    that would alter the results the results get cleared. The next time they
    are requested the calculation gets done again and the results ge stored.
    """
    def __init__(self):
        self.floatFormat = None
        self.minValue = None
        self.maxValue = None
        self.value = None
        self.size = None
        self.font = None
        self.minText = None
        self.maxText = None
        self.valueText = None
        self.minSize = None
        self.maxSize = None
        self.valueSize = None
        self.tickFreq = None
        self.increment = None
        self.minMaxLabels = False
        self.valueLabel = False
        self.selStart = None
        self.selEnd = None
        self.int_ctrl = None

        self.Horizontal = False
        self.Top = False
        self.Left = False
        self.AutoTicks = False
        self.Inverse = False
        self.PageSize = 10

        self.cache = {}

    def ResetKey(self, key):
        del(self.cache[key])

    def Reset(self):
        self.cache.clear()

    def SetMinMaxLabels(self, label):
        self.Reset()
        self.minMaxLabels = label

    def GetMinMaxLabels(self):
        return self.minMaxLabels

    def SetValueLabel(self, label):
        self.Reset()
        self.valueLabel = label

    def GetValueLabel(self):
        return self.valueLabel

    def SetFont(self, font):
        self.Reset()
        self.font = font

    def GetFont(self):
        return self.font

    def SetMaxValue(self, maxValue):
        self.Reset()
        self.maxValue = maxValue

    def SetMinValue(self, minValue):
        self.Reset()
        self.minValue = minValue

    def SetValue(self, value):
        self.Reset()

        if value < self.minValue:
            value += self.Increment
        elif value > self.maxValue:
            value -= self.Increment

        self.value = value

    def SetSize(self, size):
        self.Reset()
        self.size = size

    def GetSize(self):
        return self.size

    def SetFloatFormat(self):
        if self.floatFormat is not None:
            del(self.cache['FloatFormat'])

        if self.int_ctrl:
            return '%d'
        else:
            incT = '%f' % self.Increment
            maxT = '%f' % self.MaxValue
            minT = '%f' % self.MinValue
            incDec = len(incT.rstrip('0').split('.')[1])
            maxDec = len(maxT.rstrip('0').split('.')[1])
            minDec = len(minT.rstrip('0').split('.')[1])
            decPos = max([incDec, maxDec, minDec])
            if not decPos:
                decPos = 1
            return '%.' + str(decPos) + 'f'

    def GetFloatFormat(self):
        return self.SetFloatFormat()

    def GetMinSize(self):
        dc = wx.MemoryDC()
        dc.SetFont(self.Font)
        return dc.GetTextExtent(self.MinText)

    def GetMaxSize(self):
        dc = wx.MemoryDC()
        dc.SetFont(self.Font)
        return dc.GetTextExtent(self.MaxText)

    def GetValueSize(self):
        dc = wx.MemoryDC()
        dc.SetFont(self.Font)
        return dc.GetTextExtent(self.ValueText)

    def GetMinText(self):
        return self.FloatFormat % self.MinValue

    def GetMaxText(self):
        return self.FloatFormat % self.MaxValue

    def GetValueText(self):
        return self.FloatFormat % self.Value

    def GetMinValue(self):
        return self.minValue

    def GetMaxValue(self):
        return self.maxValue

    def GetValue(self):
        return self.value

    def GetSliderLength(self):
        width, height = self.Size

        minW, minH = self.MinSize
        maxW, maxH = self.MaxSize
        if self.Horizontal:
            sliderLen = width - 26
            if self.MinMaxLabels:
                sliderLen -= minW
                sliderLen -= maxW
            elif self.ValueLabel:
                sliderLen -= minW / 2
                sliderLen -= maxW / 2
        else:
            sliderLen = height - 10
            if self.MinMaxLabels:
                sliderLen -= minH
                sliderLen -= maxH
            elif self.ValueLabel:
                sliderLen -= minH / 2
                sliderLen -= maxH / 2

        return sliderLen

    def SetTickFreq(self, tickFreq):
        self.Reset()
        self.tickFreq = tickFreq

    def GetTickFreq(self):
        return self.tickFreq

    def SetIncrement(self, increment):
        self.Reset()
        self.increment = increment

    def GetIncrement(self):
        return self.increment

    def GetSliderSteps(self):
        if self.MinValue > self.MaxValue:
            sliderSteps = (self.MinValue - self.MaxValue) / self.Increment
        else:
            sliderSteps = (self.MaxValue - self.MinValue) / self.Increment

        return sliderSteps

    def GetSelectionStart(self):
        return self.selStart

    def GetSelectionEnd(self):
        return self.selEnd

    def SetSelection(self, minVal, maxVal):
        self.selStart = minVal
        self.selEnd = maxVal

    def GetMinMaxPosition(self):
        minW, minH = self.MinSize
        maxW, maxH = self.MaxSize
        width, height = self.Size

        if self.Horizontal:
            minX = 3
            maxX = width - maxW - 3
            if self.Top:
                minY = (height / 2) - minH
                maxY = (height / 2) - maxH
            else:
                minY = (height / 2)
                maxY = (height / 2)

        else:
            minY = 2
            maxY = height - maxH - 2
            if self.Left:
                minX = (width / 2) - minW
                maxX = (width / 2) - maxW
            else:
                minX = (width / 2) + 2
                maxX = (width / 2) + 2

        return (minX, minY), (maxX, maxY)

    def GetSliderPosition(self):
        minW, minH = self.MinSize
        maxW, maxH = self.MaxSize
        width, height = self.Size

        sliderLines = []

        for pos in [0, 1, 2]:

            if self.Horizontal:
                x = 13
                x2 = 13
                if self.MinMaxLabels:
                    x += minW
                    x2 += maxW
                elif self.ValueLabel:
                    x += minW / 2
                    x2 += maxW / 2

                if self.Top:
                    y = (height / 2) - 2
                else:
                    y = (height / 2) - 1

                y += pos
                sliderLines.append([x, y, width - x2 - 4, y])
            else:
                y = 5
                y2 = 5
                if self.MinMaxLabels:
                    y += minH
                    y2 += maxH
                elif self.ValueLabel:
                    y += minH / 2
                    y2 += maxH / 2

                if self.Left:
                    x = (width / 2) - 2
                else:
                    x = (width / 2) - 1

                x += pos
                sliderLines.append([x, y, x, height - y2 - 4])

        return sliderLines

    def SetThumb(self, mousePos):
        minW, minH = self.MinSize
        value = self.Value

        if self.Inverse:
            minVal, maxVal = self.MaxValue, self.MinValue
        else:
            minVal, maxVal = self.MinValue, self.MaxValue

        minR = 0

        if self.Horizontal:
            pos = mousePos[0]
            if self.MinMaxLabels:
                minR += minW - 5
                pos -= minW + 3
        else:
            pos = mousePos[1]
            if self.MinMaxLabels:
                minR += minH - 5
                pos -= minH + 3

        newValue = (
            ((pos - minR) * (maxVal - minVal)) / (self.SliderLength - minR)
        ) + minVal

        if newValue > value:
            while value < newValue:
                value += self.Increment
            newValue = value

        elif newValue < value:
            while value > newValue:
                value -= self.Increment
            newValue = value

        else:
            newValue = None

        if newValue is not None and maxVal >= newValue >= minVal:
            self.SetValue(newValue)
            try:
                del (self.cache['ValueSize'])
            except KeyError:
                pass
            try:
                del (self.cache['ValueText'])
            except KeyError:
                pass
            return True

    def GetValuePosition(self):
        width, height = self.Size
        valW, valH = self.ValueSize
        thumbPos = self.GetThumb()

        if self.Horizontal:
            valX = thumbPos - (valW / 2)
            if self.Top:
                valY = (height / 2) + 8
            else:
                valY = (height / 2) - valH - 9
        else:
            valY = thumbPos - (valH / 2)

            if self.Left:
                valX = (width / 2) + 8
            else:
                valX = (width / 2) - valW - 9

        return valX, valY

    def GetThumb(self, value=None):
        if value is None:
            value = self.Value

        if self.Inverse:
            minVal, maxVal = self.MaxValue, self.MinValue
        else:
            minVal, maxVal = self.MinValue, self.MaxValue

        thumbPos = int((value - minVal) / self.Increment)

        if value == minVal:
            thumbPos = 0
        elif value == maxVal:
            thumbPos = len(self.TickPosition) - 1

        try:
            if self.Horizontal:
                thumbPos = self.TickPosition[thumbPos][0]
            else:
                thumbPos = self.TickPosition[thumbPos][1]
        except IndexError:
            import traceback
            traceback.print_exc()

        return thumbPos

    def GetThumbPosition(self):
        width, height = self.Size
        thumbPos = self.GetThumb()

        if self.Top:
            thumbPos = (thumbPos - 5, (height / 2) - 11)
        elif self.Left:
            thumbPos = ((width / 2) - 12, thumbPos - 5)
        elif self.Horizontal:
            thumbPos = (thumbPos - 5, (height / 2) - 8)
        else:
            thumbPos = ((width / 2) - 8, thumbPos - 5)
        return thumbPos

    def GetTickPosition(self):
        sliderLen = self.SliderLength - 13
        steps = int(round(self.SliderSteps)) + 1
        spacing = 0
        while steps * spacing < sliderLen:
            spacing += 0.1
        dif = (sliderLen - (self.SliderSteps * spacing))
        spacing += dif / steps

        width, height = self.Size
        if self.Horizontal:
            tickX = self.SliderPosition[0][0] + 5
            if self.Top:
                tickY = (height / 2) - 17
            else:
                tickY = (height / 2) + 13
        else:
            tickY = self.SliderPosition[0][1] + 5
            if self.Left:
                tickX = (width / 2) - 17
            else:
                tickX = (width / 2) + 13

        tickList = []

        for _ in range(steps):
            tickX1, tickY1 = tickX, tickY

            if self.Horizontal:
                tickX += spacing
                tickX2 = tickX1
                tickY2 = tickY1 + 3
            else:
                tickY += spacing
                tickX2 = tickX1 + 3
                tickY2 = tickY1

            tickList.append([
                int(tickX1),
                int(tickY1),
                int(tickX2),
                int(tickY2)
            ])

        return tickList

    def __getattr__(self, item):
        if item.startswith('Get'):
            raise AttributeError

        if item in self.cache:
            return self.cache[item]

        attrName = 'Get' + item
        self.cache[item] = attr = getattr(self, attrName)()
        return attr


class FloatSliderCtrl(wx.PyPanel):
    """
    This widget is full custom widget that displays exactly like the default
    wxSlider widget except 3 changes. It displays the Labels as floats.
    The value label tracks with the thumb instead of being static. The tick
    marks are separated into small and large, The page up and page down will
    jump to the large tick positions and the up and down will work as normal.
    This custom widget accepts all the same parameters as the wxSlider except
    one added parameter. You can set an increment value so if you want to have
    the slider skip specified amount on movements it will. I have also added
    the ability to change the widget colours without having to change system
    colours.
    """

    def __init__(
            self,
            parent,
            id=wx.ID_ANY,
            value=None,
            minValue=0.0,
            maxValue=100.0,
            increment=None,
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.SL_HORIZONTAL,
            name=wx.SliderNameStr
    ):
        """
        :param parent: a wxWindow object
        :param id: wxID - if not set will automatically generate a new wxId.

        Default - wx.ID_ANY
        :param value: float(), str(), int() - The starting value of the slider.
        If not set will be set to the minValue parameter.

        Default - None
        :param minValue: float(), str(), int() - The lowest value the slider
        can be set to.

        Default - 0.0
        :param maxValue: float(), str(), int() - The highest value the slider
        can be set to.

        Default - 100.0
        :param increment: float(), str(), int() - The "step" size to take when
        the slider value is changed. If not set one will be generated using
        float(100 / (maxValue - minValue)).

        Default - None
        :param pos: Tuple for where you want the widget to be placed.

        Default - wx.DefaultPosition
        :param size: Tuple for the displayed size of the widget.

        Default - wx.DefaultSize
        :param style:
        wx.SL_HORIZONTAL: Displays the slider horizontally.
        wx.SL_VERTICAL: Displays the slider vertically.
        wx.SL_AUTOTICKS: Displays tick marks. Windows only.
        wx.SL_MIN_MAX_LABELS: Displays minimum, maximum labels.
        wx.SL_VALUE_LABEL: Displays value label.
        wx.SL_LABELS: Displays minimum, maximum and value labels.
        wx.SL_LEFT: Displays ticks on the left and forces the slider to be
        vertical.
        wx.SL_RIGHT: Displays ticks on the right and forces the slider to be
        vertical.
        wx.SL_TOP: Displays ticks on the top and forces slider to be
        horizontal.
        wx.SL_BOTTOM: Displays ticks on the bottom and forces the slider to
        be horizontal.
        wx.SL_SELRANGE: Allows the user to select a range on the slider.
        Windows only.
        wx.SL_INVERSE: Inverses the minimum and maximum endpoints on the
        slider.
         Not compatible with wx.SL_SELRANGE.

        Notice:
        SL_LEFT , SL_TOP , SL_RIGHT and SL_BOTTOM specify the position of the
        slider ticks in MSW implementation and that the min/max labels,
        if any, are positioned on the opposite side. So, to have a label on
        the left side of a vertical slider, wx.SL_RIGHT must be used.

        Warning: If using SL_AUTOTICKS as an example if you have an increment
        set at 0.001 and a min of 0.0 and a max of 10000.00 this will take a
        while for the widget to draw due to the sheer number of tick marks. If
        you need to display that many ticks for some reason then I would advise
        against resizing the widget.

        Default - wx.SL_HORIZONTAL
        :param name: user identifier for the widget.

        Default - wx.SliderNameStr
        """

        self._parent = parent
        self._name = name

        # here we check if the value was set. and if not we set it to minValue
        if value is None:
            value = minValue

        # check to see if the increment was set and if not to set a generic one
        if increment is None:
            increment = 100 / (maxValue - minValue)

        self._int_ctrl = (
            isinstance(value, int) and
            isinstance(minValue, int) and
            isinstance(maxValue, int) and
            isinstance(increment, int)
        )

        # checking the styles to set the proper characteristics of the slider
        if style | wx.SL_HORIZONTAL == style:
            horizontal = True
        elif style | wx.SL_VERTICAL == style:
            horizontal = False
        else:
            horizontal = True

        if style | wx.SL_TOP == style:
            horizontal = True
            top = True
        elif style | wx.SL_BOTTOM == style:
            horizontal = True
            top = False
        else:
            top = False

        if style | wx.SL_RIGHT == style:
            horizontal = False
            left = False
        elif style | wx.SL_LEFT == style:
            horizontal = False
            left = True
        else:
            left = False

        if style | wx.SL_SELRANGE == style:
            selRange = True
        else:
            selRange = False

        if style | wx.SL_LABELS == style:
            mLabel = True
            vLabel = True
        else:
            mLabel = False
            vLabel = False

        if style | wx.SL_MIN_MAX_LABELS == style:
            mLabel = True

        if style | wx.SL_VALUE_LABEL == style:
            vLabel = True

        if style | wx.SL_INVERSE == style:
            inverse = True
            minValue, maxValue = maxValue, minValue
        else:
            inverse = False

        if style | wx.SL_AUTOTICKS == style:
            autoTicks = True
        else:
            autoTicks = False

        wx.PyPanel.__init__(
            self,
            parent=parent,
            id=id,
            pos=pos,
            size=size
        )

        self.keyboardFocus = False
        self.thumbJump = None

        # binding mouse and keystrokes to move the slider and generate events
        self.Bind(wx.EVT_LEFT_DOWN, self._OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self._OnMouseUp)
        self.Bind(wx.EVT_MOTION, self._OnMouseMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self._OnMouseWheel)
        self.Bind(wx.EVT_SIZE, self._OnSize)
        self.Bind(wx.EVT_CHAR_HOOK, self._OnChar)

        self.Bind(wx.EVT_KILL_FOCUS, self._OnKillFocus)
        # binding paint events to draw the custom widget
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        # setting up the different colours the slider uses
        get = wx.SystemSettings.GetColour
        self.SetBackgroundColour(get(wx.SYS_COLOUR_WINDOW))
        self.SetForegroundColour(get(wx.SYS_COLOUR_SCROLLBAR))
        self.fontColour = get(wx.SYS_COLOUR_WINDOWTEXT)
        self.sliderColour = get(wx.SYS_COLOUR_3DFACE)
        self.sliderShadowColour = get(wx.SYS_COLOUR_3DSHADOW)

        # we use the SliderHandler to implement memoization magic. it will
        # cache the results of the math used to generate the static elements
        # of the slider. this is done to speed things up so that way the
        # slider does not have to do the calculations again for a simple
        # things like moving the thumb. if something like a resize takes
        # place then the slider cache is emptied and the calculations are
        # done again

        if horizontal:
            if top:
                self.thumb = GetBitmap(TOP_THUMB)
                self.activeThumb = GetBitmap(TOP_THUMB_ACTIVE)
            else:
                self.thumb = GetBitmap(BOTTOM_THUMB)
                self.activeThumb = GetBitmap((BOTTOM_THUMB_ACTIVE))
        else:
            if left:
                self.thumb = GetBitmap(LEFT_THUMB)
                self.activeThumb = GetBitmap(LEFT_THUMB_ACTIVE)
            else:
                self.thumb = GetBitmap(RIGHT_THUMB)
                self.activeThumb = GetBitmap(RIGHT_THUMB_ACTIVE)

        sh = self.SliderHandler = SliderHandler()
        sh.int_ctrl = self._int_ctrl
        sh.Top = top
        sh.Left = left
        sh.Horizontal = horizontal
        sh.Inverse = inverse
        sh.AutoTicks = autoTicks
        sh.SelRange = selRange
        sh.SetMinMaxLabels(mLabel)
        sh.SetValueLabel(vLabel)
        sh.SetMinValue(float(minValue))
        sh.SetMaxValue(float(maxValue))
        sh.SetIncrement(float(increment))
        sh.SetValue(float(value))
        sh.SetSize(size)
        sh.SetFont(wx.PyPanel.GetFont(self))
        if -1 in size:
            bestSize = self.DoGetBestSize()
            if size[0] == -1:
                size = (bestSize[0], size[1])
            if size[1] == -1:
                size = (size[0], bestSize[1])

            self.SetSize(size)

        dc = wx.ClientDC(self)
        self._Draw(dc)

# ----------------- EVENT GENERATION

    def _CreateEvent(self, event):
        """
        Internal use, creates a new wxScrollEvent that has this wxPyPanel
        instance as the event object.
        :param event: wx event metric.
        :return: None
        """
        event = wx.ScrollEvent(event, self.GetId())
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def _Top(self):
        """
        Internal use, generation of the wxEVT_SCROLL_TOP event.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_TOP)

    def _Bottom(self):
        """
        Internal use, generation of the wxEVT_SCROLL_BOTTOM event.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_BOTTOM)

    def _LineUp(self):
        """
        Internal use, generation of the wxEVT_SCROLL_LINEUP event.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_LINEUP)
        self._Changed()

    def _LineDown(self):
        """
        Internal use, generation of the wxEVT_SCROLL_LINEDOWN event.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_LINEDOWN)
        self._Changed()

    def _PageUp(self):
        """
        Internal use, generation of the wxEVT_SCROLL_PAGEUP event.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_PAGEUP)
        self._Changed()

    def _PageDown(self):
        """
        Internal use, generation of the wxEVT_SCROLL_PAGEDOWN event.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_PAGEDOWN)
        self._Changed()

    def _ThumbTrack(self):
        """
        Internal use, generation of the wxEVT_SCROLL_THUMBTRACK event.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_THUMBTRACK)

    def _ThumbRelease(self):
        """
        Internal use, generation of the wxEVT_SCROLL_THUMBRELEASE event.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_THUMBRELEASE)
        self._Changed()

    def _Changed(self):
        """
        Internal use, generation of the wxEVT_SCROLL_CHANGED event.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_CHANGED)

# ----------------- EVENTS

    def _OnKillFocus(self, evt):

        print 'Focus Killed'
        if self.HasCapture():
            self.ReleaseMouse()
        self.keyboardFocus = False
        self.thumbJump = None
        self.Refresh()
        evt.Skip()

    def _OnChar(self, evt):
        if self.HasFocus():
            keyCode = evt.GetKeyCode()
            sh = self.SliderHandler
            value = self.GetValue()

            if keyCode in (wx.WXK_RIGHT, wx.WXK_NUMPAD_RIGHT) and sh.Horizontal:
                increment = sh.Increment
                self._LineUp()
            elif keyCode in (wx.WXK_UP, wx.WXK_NUMPAD_UP) and not sh.Horizontal:
                print 'Key Up'
                increment = -sh.Increment
                self._LineDown()
            elif keyCode in (wx.WXK_LEFT, wx.WXK_NUMPAD_LEFT) and sh.Horizontal:
                print 'Key Left'
                increment = -sh.Increment
                self._LineDown()
            elif keyCode in (wx.WXK_DOWN, wx.WXK_NUMPAD_DOWN) and not sh.Horizontal:
                increment = sh.Increment
                self._LineUp()

            elif keyCode in (wx.WXK_PAGEUP, wx.WXK_NUMPAD_PAGEUP):
                increment = (sh.MaxValue - sh.MinValue) / sh.PageSize
                self._PageUp()
            elif keyCode in (wx.WXK_PAGEDOWN, wx.WXK_NUMPAD_PAGEDOWN):
                increment = -((sh.MaxValue - sh.MinValue) / sh.PageSize)
                self._PageDown()
            else:
                increment = 0

            value += increment

            if keyCode in NUMBER_CODES:
                value = (
                    self.GetMin() +
                    (self.GetMax() * ((float(NUMBER_CODES[keyCode])) * 0.1))
                )

            if value >= sh.MaxValue:
                self._Top()
            elif value <= sh.MinValue:
                self._Bottom()

            if value != self.GetValue():
                wx.CallAfter(self.SetValue, value)

        evt.Skip()

    def _OnMouseDown(self, evt):
        sh = self.SliderHandler
        startX, startY = sh.GetThumbPosition()
        w, h = self.thumb.GetSize()
        stopX = startX + w
        stopY = startY + h
        mouseX, mouseY = evt.GetPosition()

        if startX <= mouseX <= stopX and startY <= mouseY <= stopY:
            self.CaptureMouse()
            self.Refresh()

        else:
            w, h = sh.Size
            minW, minH = sh.MinSize
            sliderLen = sh.SliderLength
            minMaxLabels = sh.MinMaxLabels
            valueLabel = sh.ValueLabel

            if sh.Horizontal:
                startX = 10
                if minMaxLabels or valueLabel:
                    startX += minW
                if sh.Top:
                    startY = h / 2
                else:
                    startY = (h / 2)
                stopX = startX + sliderLen
                stopY = startY + 8
                startY -= 8
            else:
                startY = 10
                if minMaxLabels or valueLabel:
                    startY += minH
                if sh.Left:
                    startX = (w / 2)
                else:
                    startX = w / 2

                stopX = startX + 8
                stopY = startY + sliderLen
                startX -= 8

            if startX <= mouseX <= stopX and startY <= mouseY <= stopY:
                self.thumbJump = (mouseX, mouseY)
            else:
                self.thumbJump = None
        evt.Skip()

    def _OnMouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
            self.SliderHandler.SetThumb(evt.GetPosition())
            self.Refresh()
            self._ThumbRelease()

        elif self.thumbJump is not None:
            if self.SliderHandler.SetThumb(self.thumbJump):
                self.Refresh()
                self._Changed()
            self.thumbJump = None
        else:
            self.keyboardFocus = True
            self.Refresh()
        evt.Skip()

    def _OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown() and self.HasCapture():
            if self.SliderHandler.SetThumb(evt.GetPosition()):
                self.Refresh()
                self._ThumbTrack()
        evt.Skip()

    def _OnMouseWheel(self, evt):
        if self.HasFocus():
            rotation = evt.GetWheelRotation()
            if self.SliderHandler.Horizontal:
                if rotation < 0:
                    value = self.GetValue() - self.GetIncrement()
                else:
                    value = self.GetValue() + self.GetIncrement()
            else:
                if rotation > 0:
                    value = self.GetValue() - self.GetIncrement()
                else:
                    value = self.GetValue() + self.GetIncrement()

            if value < self.GetMin():
                value = self.GetMin()
            if value > self.GetMax():
                value = self.GetMax()

            self.SetValue(value)
        evt.Skip()

    def _OnSize(self, evt):
        self.SliderHandler.SetSize(evt.GetSize())
        # self.Refresh()
        self._ReDraw()
        # self.Refresh()
        evt.Skip()

    def _GetActualSliderPosition(self):
        s_width, s_height = self._GetActualSliderSize()
        c_width, c_height = self.GetSizeTuple()

        pos_x = (c_width / 2) - (s_width / 2)
        pos_y = (c_height / 2) - (s_height / 2)

        return pos_x, pos_y

    def _GetActualSliderSize(self):
        sh = self.SliderHandler

        minW, minH = sh.MinSize
        maxW, maxH = sh.MaxSize

        minMaxLabel = sh.MinMaxLabels
        valueLabel = sh.ValueLabel
        autoTicks = sh.AutoTicks

        sliderLength = sh.SliderLength

        if sh.Horizontal:
            w = 26 + sliderLength
            if minMaxLabel:
                w += minW + maxW
            elif valueLabel:
                w += (minW / 2) + (maxW / 2) - 11
            h = 42
            if autoTicks:
                h += 6
            if valueLabel:
                h += maxH
        else:
            w = 40
            if autoTicks:
                w += 6
            if valueLabel:
                w += maxW
            h = 10 + sliderLength
            if minMaxLabel:
                h += maxH * 2

        return w, h

    def DoGetClientSize(self, *args, **kwargs):

        print 'getting client size'
        return self.DoGetBestSize()

    def DoGetBestSize(self, *args, **kwargs):
        print 'getting best size'
        sh = self.SliderHandler

        minW, minH = sh.MinSize
        maxW, maxH = sh.MaxSize

        minMaxLabel = sh.MinMaxLabels
        valueLabel = sh.ValueLabel
        sliderSteps = sh.SliderSteps
        autoTicks = sh.AutoTicks

        sliderLength = (sliderSteps * sh.Increment) + 10

        if sh.Horizontal:
            w = 36 + sliderLength
            if minMaxLabel:
                w += minW + maxW
            elif valueLabel:
                w += (minW / 2) + (maxW / 2) - 11
            h = 42
            if autoTicks:
                h += 6
            if valueLabel:
                h += maxH
        else:
            w = 40
            if autoTicks:
                w += 6
            if valueLabel:
                w += maxW

            h = 36 + sliderLength
            if minMaxLabel:
                h += maxH * 2
        print (w, h)
        return wx.Size(w, h)

# ----------------- PAINT

    def _ReDraw(self):
        self.SliderHandler.Reset()
        # self.SliderHandler.SetSize(self.DoGetBestSize())
        self.SetSize(self.SliderHandler.GetSize())
        self.Refresh()

    def OnEraseBackground(self, evt):
        """
        Internal use, stops the widget from flickering when redrawn, this is an
        empty method.
        :param evt: wxEvent instance.
        :return: None
        """
        pass

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self._Draw(dc)
        evt.Skip()

    def _Draw(self, pdc):

        bmp = wx.EmptyBitmap(*self.GetSizeTuple())
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBrush(wx.Brush(wx.Colour(*self.GetBackgroundColour())))
        dc.Clear()

        if self.keyboardFocus:
            dc.SetPen(wx.Pen(
                wx.Colour(*self.fontColour),
                width=1,
                style=wx.PENSTYLE_DOT
            ))

            s_rectangle = (
                self._GetActualSliderPosition() + self._GetActualSliderSize()
            )
            dc.DrawRectangle(*s_rectangle)

        dc.SetFont(self.SliderHandler.Font)
        dc.SetTextForeground(wx.Colour(*self.fontColour))
        dc.SetTextBackground(wx.Colour(*self.GetBackgroundColour()))
        dc.SetBrush(wx.Brush(wx.Colour(*self.GetForegroundColour())))
        dc.SetPen(wx.Pen(wx.Colour(*self.GetForegroundColour()), 2))

        self._DrawMinMaxLabels(dc)
        self._DrawTicks(dc)
        self._DrawSliderBar(dc)
        self._DrawValue(dc)
        self._DrawThumb(dc)

        dc.Destroy()
        del(dc)

        pdc.DrawBitmap(bmp, 0, 0)

    def _DrawValue(self, dc):
        if self.SliderHandler.ValueLabel:
            dc.DrawText(
                self.SliderHandler.ValueText,
                *self.SliderHandler.GetValuePosition()
            )

    def _DrawThumb(self, dc):
        thumbPos = self.SliderHandler.GetThumbPosition()

        if self.HasCapture():
            dc.DrawBitmap(self.activeThumb, *thumbPos)
        else:
            dc.DrawBitmap(self.thumb, *thumbPos)

    def _DrawMinMaxLabels(self, dc):
        sh = self.SliderHandler

        if sh.MinMaxLabels:
            minPos, maxPos = sh.MinMaxPosition

            dc.DrawText(sh.MinText, *minPos)
            dc.DrawText(sh.MaxText, *maxPos)

    def _DrawTicks(self, dc):
        if self.SliderHandler.AutoTicks:
            dc.DrawLineList(self.SliderHandler.TickPosition)

    def _DrawSliderBar(self, dc):
        dc.DrawLineList(
            self.SliderHandler.SliderPosition,
            [
                wx.Pen(wx.Colour(*self.sliderShadowColour), 1),
                wx.Pen(wx.Colour(*self.sliderColour), 1),
                wx.Pen(wx.Colour(*self.sliderColour), 1)
            ]
        )

# ----------------- PUBLIC

    def IsMinMaxLabel(self):
        """
        Retruns whether or not the min/max labels are displayed.
        :return: bool()
        """
        return self.SliderHandler.MinMaxLabels

    def SetMinMaxLabel(self, flag=True):
        """
        This allows for dynamic displaying of the min/max labels.
        :param flag: True/False, default is True.
        :return: None
        """
        self.SliderHandler.SetMinMaxLabels(flag)
        self._ReDraw()

    def IsValueLabel(self):
        """
        Retruns whether or not the value label is displayed.
        :return: bool()
        """
        return self.SliderHandler.ValueLabel

    def SetValueLabel(self, flag=True):
        """
        This allows for dynamic displaying of the value label.
        :param flag: True/False, default is True.
        :return: None
        """
        self.SliderHandler.SetValueLabel(flag)
        self._ReDraw()

    def IsInverse(self):
        """
        Retruns whether or not the wx.SL_INVERSE was set.
        :return: bool()
        """
        return self.SliderHandler.Inverse

    def GetName(self):
        """
        Retruns the name given when creating the control. If one was not given
        returns wx.SliderNameStr.
        :return: str()
        """
        return self._name

    def SetName(self, name):
        self._name = name

    def GetValue(self):
        """
        Retruns a float of the current slider value.
        :return: float()
        """
        return self.SliderHandler.Value

    def SetValue(self, value):
        """
        Sets the value for the slider. Will convert to a float if a
        str of a float or an int is passed.
        :param value: float() int() or a str() of a float.
        :return: None
        """

        if self._int_ctrl:
            self.SliderHandler.SetValue(int(value))
        else:
            self.SliderHandler.SetValue(float(value))
        self.Refresh()

    def GetMin(self):
        """
        Retruns a float of the current min value.
        :return: float()
        """
        return self.SliderHandler.MinValue

    def SetMin(self, minValue):
        """
        Sets the min value for the slider. Will convert to a float if a
        str of a float or an int is passed.
        :param minValue: float() int() or a str() of a float.
        :return: None
        """

        if self._int_ctrl:
            self.SliderHandler.SetMinValue(int(minValue))
        else:
            self.SliderHandler.SetMinValue(float(minValue))
        self._ReDraw()

    def GetMax(self):
        """
        Retruns a float of the current max value.
        :return: float()
        """
        return self.SliderHandler.MaxValue

    def SetMax(self, maxValue):
        """
        Sets the max value for the slider. Will convert to a float if a
        str of a float or an int is passed.
        :param maxValue: float() int() or a str() of a float.
        :return: None
        """

        if self._int_ctrl:
            self.SliderHandler.SetMaxValue(int(maxValue))
        else:
            self.SliderHandler.SetMaxValue(float(maxValue))
        self._ReDraw()

    def SetRange(self, minValue, maxValue):
        """
        Sets the min and max values for the slider. Will convert to a float if
        a str of a float or an int is passed.
        :param minValue: float() int() or a str() of a float.
        :param maxValue: float() int() or a str() of a float.
        :return: None
        """

        if self._int_ctrl:
            self.SliderHandler.SetMinValue(int(minValue))
            self.SliderHandler.SetMaxValue(int(maxValue))
        else:
            self.SliderHandler.SetMinValue(float(minValue))
            self.SliderHandler.SetMaxValue(float(maxValue))
        self._ReDraw()

    def GetIncrement(self):
        """
        Retruns a float of the current increment value.
        :return: float()
        """
        return self.SliderHandler.Increment

    def SetIncrement(self, increment):
        """
        Sets the increment for the slider. Will convert to a float if a
        str of a float or an int is passed.
        :param increment: float() int() or a str() of a float.
        :return: None
        """

        if self._int_ctrl:
            self.SliderHandler.SetIncrement(int(increment))
        else:
            self.SliderHandler.SetIncrement(float(increment))
        self._ReDraw()

    def SetPageSize(self, pageSize):
        self.SliderHandler.PageSize = pageSize

    def GetPageSize(self):
        return self.SliderHandler.PageSize

    def GetSelStart(self):
        """
        Retruns a float of the current selection start value, or None if one
        has not been set.
        :return: float(), None
        """
        return self.SliderHandler.SelectionStart

    def GetSelEnd(self):
        """
        Retruns a float of the current selection end value, or None if one
        has not been set.
        :return: float(), None
        """
        return self.SliderHandler.SelectionEnd

    def SetSelection(self, min, max):
        """
        Sets the selection start and end points
        :param min: float() int() or a str() of a float of the start point.
        :param max: float() int() or a str() of a float of the end point.
        :return: None
        """
        if self._int_ctrl:
            self.SliderHandler.SetSelection(int(min), int(max))
        else:
            self.SliderHandler.SetSelection(float(min), float(max))

    def GetFontColour(self):
        return self.fontColour

    def SetFontColour(self, colour):
        self.fontColour = CheckColour(colour)
        self.Refresh()

    def GetFont(self):
        return self.SliderHandler.Font

    def SetFont(self, font):
        wx.PyPanel.SetFont(self, font)
        self.SliderHandler.SetFont(font)
        self._ReDraw()

# ------------------------- END SLIDER CODE  ---------------------


if __name__ == '__main__':
    STYLES = [
        wx.SL_HORIZONTAL | wx.SL_TOP,
        wx.SL_VERTICAL | wx.SL_LEFT,
        wx.SL_VERTICAL | wx.SL_RIGHT,
        wx.SL_HORIZONTAL | wx.SL_BOTTOM
    ]

    STYLE_NAMES = [
        'wx.SL_HORIZONTAL | wx.SL_TOP',
        'wx.SL_VERTICAL | wx.SL_LEFT',
        'wx.SL_VERTICAL | wx.SL_RIGHT',
        'wx.SL_HORIZONTAL | wx.SL_BOTTOM'
    ]
    app = wx.App()

    frame = wx.Frame(
        None,
        size=(550, 600)
    )

    main_sizer = wx.BoxSizer(wx.VERTICAL)
    top_sizer = wx.BoxSizer(wx.HORIZONTAL)
    bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)

    from random import randrange

    for i, style in enumerate(STYLES):
        style |= wx.SL_AUTOTICKS | wx.SL_LABELS

        st = wx.StaticText(frame, -1, STYLE_NAMES[i])

        minVal = float(randrange(3, 75))
        maxVal = float(randrange(100, 165))

        slider = FloatSliderCtrl(
            frame,
            -1,
            value=float(randrange(minVal, maxVal)),
            minValue=minVal,
            maxValue=maxVal,
            increment=float(randrange(1, 9) / 10.0),
            style=style,
            # size=size
        )

        if i in (0, 3):
            sizer = wx.BoxSizer(wx.VERTICAL)

        else:
            sizer = wx.BoxSizer(wx.HORIZONTAL)

        label_sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_sizer.AddStretchSpacer(1)
        lbl_sizer.Add(st, 0, wx.EXPAND | wx.ALL, 10)
        lbl_sizer.AddStretchSpacer(1)
        label_sizer.Add(lbl_sizer)
        label_sizer.Add(sizer, 1, wx.EXPAND)

        sizer.AddStretchSpacer(0)
        sizer.Add(slider, 0, wx.ALL, 10)
        sizer.AddStretchSpacer(0)

        if i <= 1:
            top_sizer.Add(label_sizer, 0, wx.EXPAND)
        else:
            bottom_sizer.Add(label_sizer, 0, wx.EXPAND)

    main_sizer.Add(top_sizer)
    main_sizer.Add(bottom_sizer)
    frame.SetSizer(main_sizer)
    frame.Show()
    app.MainLoop()
