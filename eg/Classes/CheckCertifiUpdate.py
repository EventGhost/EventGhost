# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import json
import os
import pycurl
import threading
import tempfile

import wx

import eg


class Text(eg.TranslatableStrings):
    newVersionMesg = \
        "A new version of the certifi module has been released!\n\n"\
        "Your version:\t%s\n"\
        "Newest version:\t%s\n\n"\
        "Do you want to update now (EventGhost will restart)?"
    ManErrorMesg = \
        "It wasn't possible to get the information from the PyPI website.\n\n"\
        "Please try it again later."


class CheckCertifiUpdate(object):
    @classmethod
    @eg.LogIt
    def start(cls):
        threading.Thread(target=_check_update, name="CheckCertifiUpdate").start()


class MessageDialog(eg.MessageDialog):
    def __init__(self, ver_pypi, ver_local):
        eg.MessageDialog.__init__(
            self,
            parent=eg.document.frame,
            message=Text.newVersionMesg % (ver_local, ver_pypi),
            caption=eg.APP_NAME,
            style=wx.YES | wx.NO
        )
        self.Bind(wx.EVT_BUTTON, self.on_yes, id=wx.ID_YES)
        self.ShowModal()

    @staticmethod
    def on_yes(evt):
        wx.CallAfter(eg.app.Restart, update_certifi=True)
        evt.Skip()


PYPI_PEM = r'''  # retrieved on 07.02.2019
-----BEGIN CERTIFICATE-----
MIIIczCCB1ugAwIBAgIQDl7PGBeDAG2brEU2EfVJEjANBgkqhkiG9w0BAQsFADB1
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMTQwMgYDVQQDEytEaWdpQ2VydCBTSEEyIEV4dGVuZGVk
IFZhbGlkYXRpb24gU2VydmVyIENBMB4XDTE4MDkxODAwMDAwMFoXDTIwMTAxNDEy
MDAwMFowgdgxHTAbBgNVBA8MFFByaXZhdGUgT3JnYW5pemF0aW9uMRMwEQYLKwYB
BAGCNzwCAQMTAlVTMRkwFwYLKwYBBAGCNzwCAQITCERlbGF3YXJlMRAwDgYDVQQF
EwczMzU5MzAwMQswCQYDVQQGEwJVUzEWMBQGA1UECBMNTmV3IEhhbXBzaGlyZTES
MBAGA1UEBxMJV29sZmVib3JvMSMwIQYDVQQKExpQeXRob24gU29mdHdhcmUgRm91
bmRhdGlvbjEXMBUGA1UEAxMOd3d3LnB5dGhvbi5vcmcwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQD2roGTDc+m3g3mReIf7j5rzLovnk3Zggvy2kWWMnDB
Yz2m6sgxOL1pkzIu7YNe4noH7ZRym0OIQjZbDIleB7SOGAoD2BBv+Mv79HtedJ3d
vhXwmgRenlNxBxhDcaVLDONVC9Ir3Ft46uuGIrXnKB8L1KZV6h8IFC2G3GZXJtkw
EojXdmJFzuRrKMRi0cLPlF60upRISIj3jg9kK4D+f0xYrsQAJvK0veqRsNQ8bXPE
YR8kG4Paj7rOeh3FVGxrKOKNpoI+kV6EqOVIhJY698P7EbDLGjG2Im9P6VFmwXod
YAZ2CTFaMlrC0FljAO/FKeQKR29vitthLMutcd+AkoDDAgMBAAGjggSZMIIElTAf
BgNVHSMEGDAWgBQ901Cl1qCt7vNKYApl0yHU+PjWDzAdBgNVHQ4EFgQUUTsyHAXZ
y6d2HWn+8MZNUhBCkEwwggFCBgNVHREEggE5MIIBNYIOd3d3LnB5dGhvbi5vcmeC
D2RvY3MucHl0aG9uLm9yZ4IPYnVncy5weXRob24ub3Jngg93aWtpLnB5dGhvbi5v
cmeCDWhnLnB5dGhvbi5vcmeCD21haWwucHl0aG9uLm9yZ4IPcHlwaS5weXRob24u
b3JnghRwYWNrYWdpbmcucHl0aG9uLm9yZ4IQbG9naW4ucHl0aG9uLm9yZ4ISZGlz
Y3Vzcy5weXRob24ub3Jnggx1cy5weWNvbi5vcmeCB3B5cGkuaW+CDGRvY3MucHlw
aS5pb4IIcHlwaS5vcmeCDWRvY3MucHlwaS5vcmeCD2RvbmF0ZS5weXBpLm9yZ4IT
ZGV2Z3VpZGUucHl0aG9uLm9yZ4ITd3d3LmJ1Z3MucHl0aG9uLm9yZ4IKcHl0aG9u
Lm9yZzAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUF
BwMCMHUGA1UdHwRuMGwwNKAyoDCGLmh0dHA6Ly9jcmwzLmRpZ2ljZXJ0LmNvbS9z
aGEyLWV2LXNlcnZlci1nMi5jcmwwNKAyoDCGLmh0dHA6Ly9jcmw0LmRpZ2ljZXJ0
LmNvbS9zaGEyLWV2LXNlcnZlci1nMi5jcmwwSwYDVR0gBEQwQjA3BglghkgBhv1s
AgEwKjAoBggrBgEFBQcCARYcaHR0cHM6Ly93d3cuZGlnaWNlcnQuY29tL0NQUzAH
BgVngQwBATCBiAYIKwYBBQUHAQEEfDB6MCQGCCsGAQUFBzABhhhodHRwOi8vb2Nz
cC5kaWdpY2VydC5jb20wUgYIKwYBBQUHMAKGRmh0dHA6Ly9jYWNlcnRzLmRpZ2lj
ZXJ0LmNvbS9EaWdpQ2VydFNIQTJFeHRlbmRlZFZhbGlkYXRpb25TZXJ2ZXJDQS5j
cnQwDAYDVR0TAQH/BAIwADCCAX8GCisGAQQB1nkCBAIEggFvBIIBawFpAHcA7ku9
t3XOYLrhQmkfq+GeZqMPfl+wctiDAMR7iXqo/csAAAFl7l3MWwAABAMASDBGAiEA
qfAJSfOHG4r8YvzTkZsr8cEXFcnFIns40+JXVdgY0vsCIQCvnB+YExtMRQVQXONc
glOTsIYmNgYPrtyHYsTj/Xua5QB3AFYUBpov18Ls0/XhvUSyPsdGdrm8mRFcwO+U
mFXWidDdAAABZe5dzHoAAAQDAEgwRgIhAIF6xXakKVdREciK8aM2z1c71eiU8qF/
UCZbl4sEfLTQAiEA870pR9Hazod3FgZszr9itk8sYPLoQjV9/WENl0HXXGwAdQC7
2d+8H4pxtZOUI5eqkntHOFeVCqtS6BqQlmQ2jh7RhQAAAWXuXcwzAAAEAwBGMEQC
IAeIvcaqPATJrCo3+ceBlVbsyPJcDPM7QGLpaRPFBduQAiBHNfcsBLaelS9bUmfU
R0VjJLoTA39AJAj8oU6iAzruHDANBgkqhkiG9w0BAQsFAAOCAQEAwH5+PXougfo5
qMVIE65Dei/CEb4ahZfoMvvlJRvuNAI/ARWYQSHh6IKXdxFxIE5hCC/NNtdAcc1p
CoZ2+IM/x0cGBjHZegSjhXfQy+w7twfgyeTSNalV2jzKQ0Yv/JvfI9qiMdhEQbfL
qaQ6Nj/js8uvQqWf6w8yo7hAzKs1jTF7Wy/cM0lvqNocDWYROhAVcI+jSMKwlcLv
75xAbOZqw2D483mkQizVj7wQ1fYP3Tr0wfvFNeoIAPUXLrEHiEmHWA0h+U9KEgVf
VQ3PvzItecKWFI+0d9RpNupc1HdipBCySvnNa1LcG2AviYXpIsbo8EBvbj0HcEVx
7NEANHNX2g==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIEtjCCA56gAwIBAgIQDHmpRLCMEZUgkmFf4msdgzANBgkqhkiG9w0BAQsFADBs
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSswKQYDVQQDEyJEaWdpQ2VydCBIaWdoIEFzc3VyYW5j
ZSBFViBSb290IENBMB4XDTEzMTAyMjEyMDAwMFoXDTI4MTAyMjEyMDAwMFowdTEL
MAkGA1UEBhMCVVMxFTATBgNVBAoTDERpZ2lDZXJ0IEluYzEZMBcGA1UECxMQd3d3
LmRpZ2ljZXJ0LmNvbTE0MDIGA1UEAxMrRGlnaUNlcnQgU0hBMiBFeHRlbmRlZCBW
YWxpZGF0aW9uIFNlcnZlciBDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
ggEBANdTpARR+JmmFkhLZyeqk0nQOe0MsLAAh/FnKIaFjI5j2ryxQDji0/XspQUY
uD0+xZkXMuwYjPrxDKZkIYXLBxA0sFKIKx9om9KxjxKws9LniB8f7zh3VFNfgHk/
LhqqqB5LKw2rt2O5Nbd9FLxZS99RStKh4gzikIKHaq7q12TWmFXo/a8aUGxUvBHy
/Urynbt/DvTVvo4WiRJV2MBxNO723C3sxIclho3YIeSwTQyJ3DkmF93215SF2AQh
cJ1vb/9cuhnhRctWVyh+HA1BV6q3uCe7seT6Ku8hI3UarS2bhjWMnHe1c63YlC3k
8wyd7sFOYn4XwHGeLN7x+RAoGTMCAwEAAaOCAUkwggFFMBIGA1UdEwEB/wQIMAYB
Af8CAQAwDgYDVR0PAQH/BAQDAgGGMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEF
BQcDAjA0BggrBgEFBQcBAQQoMCYwJAYIKwYBBQUHMAGGGGh0dHA6Ly9vY3NwLmRp
Z2ljZXJ0LmNvbTBLBgNVHR8ERDBCMECgPqA8hjpodHRwOi8vY3JsNC5kaWdpY2Vy
dC5jb20vRGlnaUNlcnRIaWdoQXNzdXJhbmNlRVZSb290Q0EuY3JsMD0GA1UdIAQ2
MDQwMgYEVR0gADAqMCgGCCsGAQUFBwIBFhxodHRwczovL3d3dy5kaWdpY2VydC5j
b20vQ1BTMB0GA1UdDgQWBBQ901Cl1qCt7vNKYApl0yHU+PjWDzAfBgNVHSMEGDAW
gBSxPsNpA/i/RwHUmCYaCALvY2QrwzANBgkqhkiG9w0BAQsFAAOCAQEAnbbQkIbh
hgLtxaDwNBx0wY12zIYKqPBKikLWP8ipTa18CK3mtlC4ohpNiAexKSHc59rGPCHg
4xFJcKx6HQGkyhE6V6t9VypAdP3THYUYUN9XR3WhfVUgLkc3UHKMf4Ib0mKPLQNa
2sPIoc4sUqIAY+tzunHISScjl2SFnjgOrWNoPLpSgVh5oywM395t6zHyuqB8bPEs
1OG9d4Q3A84ytciagRpKkk47RpqF/oOi+Z6Mo8wNXrM9zwR4jxQUezKcxwCmXMS1
oVWNWlZopCJwqjyBcdmdqEU79OX2olHdx3ti6G8MdOu42vi/hw15UJGQmxg7kVkn
8TUoE6smftX3eg==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDxTCCAq2gAwIBAgIQAqxcJmoLQJuPC3nyrkYldzANBgkqhkiG9w0BAQUFADBs
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSswKQYDVQQDEyJEaWdpQ2VydCBIaWdoIEFzc3VyYW5j
ZSBFViBSb290IENBMB4XDTA2MTExMDAwMDAwMFoXDTMxMTExMDAwMDAwMFowbDEL
MAkGA1UEBhMCVVMxFTATBgNVBAoTDERpZ2lDZXJ0IEluYzEZMBcGA1UECxMQd3d3
LmRpZ2ljZXJ0LmNvbTErMCkGA1UEAxMiRGlnaUNlcnQgSGlnaCBBc3N1cmFuY2Ug
RVYgUm9vdCBDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMbM5XPm
+9S75S0tMqbf5YE/yc0lSbZxKsPVlDRnogocsF9ppkCxxLeyj9CYpKlBWTrT3JTW
PNt0OKRKzE0lgvdKpVMSOO7zSW1xkX5jtqumX8OkhPhPYlG++MXs2ziS4wblCJEM
xChBVfvLWokVfnHoNb9Ncgk9vjo4UFt3MRuNs8ckRZqnrG0AFFoEt7oT61EKmEFB
Ik5lYYeBQVCmeVyJ3hlKV9Uu5l0cUyx+mM0aBhakaHPQNAQTXKFx01p8VdteZOE3
hzBWBOURtCmAEvF5OYiiAhF8J2a3iLd48soKqDirCmTCv2ZdlYTBoSUeh10aUAsg
EsxBu24LUTi4S8sCAwEAAaNjMGEwDgYDVR0PAQH/BAQDAgGGMA8GA1UdEwEB/wQF
MAMBAf8wHQYDVR0OBBYEFLE+w2kD+L9HAdSYJhoIAu9jZCvDMB8GA1UdIwQYMBaA
FLE+w2kD+L9HAdSYJhoIAu9jZCvDMA0GCSqGSIb3DQEBBQUAA4IBAQAcGgaX3Nec
nzyIZgYIVyHbIUf4KmeqvxgydkAQV8GK83rZEWWONfqe/EW1ntlMMUu4kehDLI6z
eM7b41N5cdblIZQB2lWHmiRk9opmzN6cN82oNLFpmyPInngiK3BD41VHMWEZ71jF
hS9OMPagMRYjyOfiZRYzy78aG6A9+MpeizGLYAiJLQwGXFK3xPkKmNEVX58Svnw2
Yzi9RKR/5CYrCsSXaQ3pjOLAEFe4yHYSkVXySGnYvCoCWw9E1CAx2/S6cCZdkGCe
vEsXCS+0yx5DaMkHJ8HSXPfqIbloEpw8nL+e/IBcm2PN7EeqJSdnoDfzAIJ9VNep
+OkuE6N36B9K
-----END CERTIFICATE-----
'''
SHA1_KEY = 'C5:B5:C4:D3:A7:28:8C:74:1E:BD:C9:83:E4:0E:EE:AD:3B:17:09:50'
SHA_256 = '6E:F7:0B:83:2F:A0:21:A1:8E:4B:A9:48:B8:F6:46:BE:DD:AC:32:1E:' \
          '73:A3:4D:4C:1E:78:35:55:9E:65:39:6B'


def _check_update():
    dialog = None
    try:
        cacert_fd, cacert_path = tempfile.mkstemp()
        cacert = os.fdopen(cacert_fd, 'w')
        cacert.write(PYPI_PEM)
        cacert.close()
        curl = pycurl.Curl()
        curl.setopt(pycurl.CAINFO, cacert_path)
        curl.setopt(pycurl.URL, "https://pypi.org/pypi/certifi/json")
        json_str = curl.perform_rs()
        os.remove(cacert_path)
        prj_info = json.loads(json_str)

        try:
            import certifi
        except ImportError:
            # noinspection PyPep8Naming
            class certifi(object):
                __version__ = 0
        if prj_info['info']['version'] > certifi.__version__:
            wx.CallAfter(
                MessageDialog,
                prj_info['info']['version'],
                certifi.__version__
            )

    except ValueError:
        if dialog:
            dialog.Destroy()
        dlg = wx.MessageDialog(
            None,
            Text.ManErrorMesg,
            eg.APP_NAME,
            style=wx.OK | wx.ICON_ERROR
        )
        dlg.ShowModal()
        dlg.Destroy()
