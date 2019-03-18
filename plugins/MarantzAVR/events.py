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

import re

EVENTS = {
    'CVBDL **': {
        'event': 'MainZone.ChannelVolume.SurroundBackLeftDolby.**',
        'description': 'Main Zone Channel Volume Surround Back Left Dolby Input'
    },
    'CVBDL DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundBackLeftDolby.Down',
        'description': 'Main Zone Channel Volume Surround Back Left Dolby Down'
    },
    'CVBDL UP': {
        'event': 'MainZone.ChannelVolume.SurroundBackLeftDolby.Up',
        'description': 'Main Zone Channel Volume Surround Back Left Dolby Up'
    },
    'CVBDR **': {
        'event': 'MainZone.ChannelVolume.SurroundBackRightDolby.**',
        'description': 'Main Zone Channel Volume Surround Back Right Dolby Input'
    },
    'CVBDR DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundBackRightDolby.Down',
        'description': 'Main Zone Channel Volume Surround Back Right Dolby Down'
    },
    'CVBDR UP': {
        'event': 'MainZone.ChannelVolume.SurroundBackRightDolby.Up',
        'description': 'Main Zone Channel Volume Surround Back Right Dolby Up'
    },
    'CVC **': {
        'event': 'MainZone.ChannelVolume.Center.**',
        'description': 'Main Zone Channel Volume Center Input'
    },
    'CVC DOWN': {
        'event': 'MainZone.ChannelVolume.Center.Down',
        'description': 'Main Zone Channel Volume Center Down'
    },
    'CVC UP': {
        'event': 'MainZone.ChannelVolume.Center.Up',
        'description': 'Main Zone Channel Volume Center Up'
    },
    'CVFDL **': {
        'event': 'MainZone.ChannelVolume.LeftFrontDolby.**',
        'description': 'Main Zone Channel Volume Left Front Dolby Input'
    },
    'CVFDL DOWN': {
        'event': 'MainZone.ChannelVolume.LeftFrontDolby.Down',
        'description': 'Main Zone Channel Volume Left Front Dolby Down'
    },
    'CVFDL UP': {
        'event': 'MainZone.ChannelVolume.LeftFrontDolby.Up',
        'description': 'Main Zone Channel Volume Left Front Dolby Up'
    },
    'CVFDR **': {
        'event': 'MainZone.ChannelVolume.RightFrontDolby.**',
        'description': 'Main Zone Channel Volume Right Front Dolby Input'
    },
    'CVFDR DOWN': {
        'event': 'MainZone.ChannelVolume.RightFrontDolby.Down',
        'description': 'Main Zone Channel Volume Right Front Dolby Down'
    },
    'CVFDR UP': {
        'event': 'MainZone.ChannelVolume.RightFrontDolby.Up',
        'description': 'Main Zone Channel Volume Right Front Dolby Up'
    },
    'CVFHL **': {
        'event': 'MainZone.ChannelVolume.LeftFrontHeight.**',
        'description': 'Main Zone Channel Volume Left Front Height Input'
    },
    'CVFHL DOWN': {
        'event': 'MainZone.ChannelVolume.LeftFrontHeight.Down',
        'description': 'Main Zone Channel Volume Left Front Height Down'
    },
    'CVFHL UP': {
        'event': 'MainZone.ChannelVolume.LeftFrontHeight.Up',
        'description': 'Main Zone Channel Volume Left Front Height Up'
    },
    'CVFHR **': {
        'event': 'MainZone.ChannelVolume.RightFrontHeight.**',
        'description': 'Main Zone Channel Volume Right Front Height Input'
    },
    'CVFHR DOWN': {
        'event': 'MainZone.ChannelVolume.RightFrontHeight.Down',
        'description': 'Main Zone Channel Volume Right Front Height Down'
    },
    'CVFHR UP': {
        'event': 'MainZone.ChannelVolume.RightFrontHeight.Up',
        'description': 'Main Zone Channel Volume Right Front Height Up'
    },
    'CVFL **': {
        'event': 'MainZone.ChannelVolume.FrontLeft.**',
        'description': 'Main Zone Channel Volume Front Left Input'
    },
    'CVFL DOWN': {
        'event': 'MainZone.ChannelVolume.FrontLeft.Down',
        'description': 'Main Zone Channel Volume Front Left Down'
    },
    'CVFL UP': {
        'event': 'MainZone.ChannelVolume.FrontLeft.Up',
        'description': 'Main Zone Channel Volume Front Left Up'
    },
    'CVFR **': {
        'event': 'MainZone.ChannelVolume.FrontRight.**',
        'description': 'Main Zone Channel Volume Front Right Input'
    },
    'CVFR DOWN': {
        'event': 'MainZone.ChannelVolume.FrontRight.Down',
        'description': 'Main Zone Channel Volume Front Right Down'
    },
    'CVFR UP': {
        'event': 'MainZone.ChannelVolume.FrontRight.Up',
        'description': 'Main Zone Channel Volume Front Right Up'
    },
    'CVFWL **': {
        'event': 'MainZone.ChannelVolume.LeftFrontWide.**',
        'description': 'Main Zone Channel Volume Left Front Wide Input'
    },
    'CVFWL DOWN': {
        'event': 'MainZone.ChannelVolume.LeftFrontWide.Down',
        'description': 'Main Zone Channel Volume Left Front Wide Down'
    },
    'CVFWL UP': {
        'event': 'MainZone.ChannelVolume.LeftFrontWide.Up',
        'description': 'Main Zone Channel Volume Left Front Wide Up'
    },
    'CVFWR **': {
        'event': 'MainZone.ChannelVolume.RightFrontWide.**',
        'description': 'Main Zone Channel Volume Right Front Wide Input'
    },
    'CVFWR DOWN': {
        'event': 'MainZone.ChannelVolume.RightFrontWide.Down',
        'description': 'Main Zone Channel Volume Right Front Wide Down'
    },
    'CVFWR UP': {
        'event': 'MainZone.ChannelVolume.RightFrontWide.Up',
        'description': 'Main Zone Channel Volume Right Front Wide Up'
    },
    'CVRHL **': {
        'event': 'MainZone.ChannelVolume.LeftRearHeight.**',
        'description': 'Main Zone Channel Volume Left Rear Height Input'
    },
    'CVRHL DOWN': {
        'event': 'MainZone.ChannelVolume.LeftRearHeight.Down',
        'description': 'Main Zone Channel Volume Left Rear Height Down'
    },
    'CVRHL UP': {
        'event': 'MainZone.ChannelVolume.LeftRearHeight.Up',
        'description': 'Main Zone Channel Volume Left Rear Height Up'
    },
    'CVRHR **': {
        'event': 'MainZone.ChannelVolume.RightRearHeight.**',
        'description': 'Main Zone Channel Volume Right Rear Height Input'
    },
    'CVRHR DOWN': {
        'event': 'MainZone.ChannelVolume.RightRearHeight.Down',
        'description': 'Main Zone Channel Volume Right Rear Height Down'
    },
    'CVRHR UP': {
        'event': 'MainZone.ChannelVolume.RightRearHeight.Up',
        'description': 'Main Zone Channel Volume Right Rear Height Up'
    },
    'CVSB **': {
        'event': 'MainZone.ChannelVolume.SurroundBack.**',
        'description': 'Main Zone Channel Volume Surround Back Input'
    },
    'CVSB DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundBack.Down',
        'description': 'Main Zone Channel Volume Surround Back Down'
    },
    'CVSB UP': {
        'event': 'MainZone.ChannelVolume.SurroundBack.Up',
        'description': 'Main Zone Channel Volume Surround Back Up'
    },
    'CVSBL **': {
        'event': 'MainZone.ChannelVolume.SurroundBackLeft.**',
        'description': 'Main Zone Channel Volume Surround Back Left Input'
    },
    'CVSBL DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundBackLeft.Down',
        'description': 'Main Zone Channel Volume Surround Back Left Down'
    },
    'CVSBL UP': {
        'event': 'MainZone.ChannelVolume.SurroundBackLeft.Up',
        'description': 'Main Zone Channel Volume Surround Back Left Up'
    },
    'CVSBR **': {
        'event': 'MainZone.ChannelVolume.SurroundBackRight.**',
        'description': 'Main Zone Channel Volume Surround Back Right Input'
    },
    'CVSBR DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundBackRight.Down',
        'description': 'Main Zone Channel Volume Surround Back Right Down'
    },
    'CVSBR UP': {
        'event': 'MainZone.ChannelVolume.SurroundBackRight.Up',
        'description': 'Main Zone Channel Volume Surround Back Right Up'
    },
    'CVSDL **': {
        'event': 'MainZone.ChannelVolume.SurroundLeftDolby.**',
        'description': 'Main Zone Channel Volume Surround Left Dolby Input'
    },
    'CVSDL DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundLeftDolby.Down',
        'description': 'Main Zone Channel Volume Surround Left Dolby Down'
    },
    'CVSDL UP': {
        'event': 'MainZone.ChannelVolume.SurroundLeftDolby.Up',
        'description': 'Main Zone Channel Volume Surround Left Dolby Up'
    },
    'CVSDR **': {
        'event': 'MainZone.ChannelVolume.SurroundRightDolby.**',
        'description': 'Main Zone Channel Volume Surround Right Dolby Input'
    },
    'CVSDR DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundRightDolby.Down',
        'description': 'Main Zone Channel Volume Surround Right Dolby Down'
    },
    'CVSDR UP': {
        'event': 'MainZone.ChannelVolume.SurroundRightDolby.Up',
        'description': 'Main Zone Channel Volume Surround Right Dolby Up'
    },
    'CVSHL **': {
        'event': 'MainZone.ChannelVolume.SurroundLeftHeightAuro-3D.**',
        'description': 'Main Zone Channel Volume Surround Left Height Auro-3D  Input'
    },
    'CVSHL DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundLeftHeightAuro-3D.Down',
        'description': 'Main Zone Channel Volume Surround Left Height Auro-3D  Down'
    },
    'CVSHL UP': {
        'event': 'MainZone.ChannelVolume.SurroundLeftHeightAuro-3D.Up',
        'description': 'Main Zone Channel Volume Surround Left Height Auro-3D  Up'
    },
    'CVSHR **': {
        'event': 'MainZone.ChannelVolume.SurroundRightHeightAuro-3D.**',
        'description': 'Main Zone Channel Volume Surround Right Height Auro-3D  Input'
    },
    'CVSHR DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundRightHeightAuro-3D.Down',
        'description': 'Main Zone Channel Volume Surround Right Height Auro-3D  Down'
    },
    'CVSHR UP': {
        'event': 'MainZone.ChannelVolume.SurroundRightHeightAuro-3D.Up',
        'description': 'Main Zone Channel Volume Surround Right Height Auro-3D  Up'
    },
    'CVSL **': {
        'event': 'MainZone.ChannelVolume.SurroundLeft.**',
        'description': 'Main Zone Channel Volume Surround Left Input'
    },
    'CVSL DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundLeft.Down',
        'description': 'Main Zone Channel Volume Surround Left Down'
    },
    'CVSL UP': {
        'event': 'MainZone.ChannelVolume.SurroundLeft.Up',
        'description': 'Main Zone Channel Volume Surround Left Up'
    },
    'CVSR **': {
        'event': 'MainZone.ChannelVolume.SurroundRight.**',
        'description': 'Main Zone Channel Volume Surround Right Input'
    },
    'CVSR DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundRight.Down',
        'description': 'Main Zone Channel Volume Surround Right Down'
    },
    'CVSR UP': {
        'event': 'MainZone.ChannelVolume.SurroundRight.Up',
        'description': 'Main Zone Channel Volume Surround Right Up'
    },
    'CVSW **': {
        'event': 'MainZone.ChannelVolume.Subwoofer.**',
        'description': 'Main Zone Channel Volume Subwoofer Input'
    },
    'CVSW DOWN': {
        'event': 'MainZone.ChannelVolume.Subwoofer.Down',
        'description': 'Main Zone Channel Volume Subwoofer Down'
    },
    'CVSW UP': {
        'event': 'MainZone.ChannelVolume.Subwoofer.Up',
        'description': 'Main Zone Channel Volume Subwoofer Up'
    },
    'CVSW2 **': {
        'event': 'MainZone.ChannelVolume.Subwoofer2.**',
        'description': 'Main Zone Channel Volume Subwoofer 2 Input'
    },
    'CVSW2 DOWN': {
        'event': 'MainZone.ChannelVolume.Subwoofer2.Down',
        'description': 'Main Zone Channel Volume Subwoofer 2 Down'
    },
    'CVSW2 UP': {
        'event': 'MainZone.ChannelVolume.Subwoofer2.Up',
        'description': 'Main Zone Channel Volume Subwoofer 2 Up'
    },
    'CVTFL **': {
        'event': 'MainZone.ChannelVolume.LeftFrontTop.**',
        'description': 'Main Zone Channel Volume Left Front Top Input'
    },
    'CVTFL DOWN': {
        'event': 'MainZone.ChannelVolume.LeftFrontTop.Down',
        'description': 'Main Zone Channel Volume Left Front Top Down'
    },
    'CVTFL UP': {
        'event': 'MainZone.ChannelVolume.LeftFrontTop.Up',
        'description': 'Main Zone Channel Volume Left Front Top Up'
    },
    'CVTFR **': {
        'event': 'MainZone.ChannelVolume.RightFrontTop.**',
        'description': 'Main Zone Channel Volume Right Front Top Input'
    },
    'CVTFR DOWN': {
        'event': 'MainZone.ChannelVolume.RightFrontTop.Down',
        'description': 'Main Zone Channel Volume Right Front Top Down'
    },
    'CVTFR UP': {
        'event': 'MainZone.ChannelVolume.RightFrontTop.Up',
        'description': 'Main Zone Channel Volume Right Front Top Up'
    },
    'CVTML **': {
        'event': 'MainZone.ChannelVolume.LeftFrontMiddle.**',
        'description': 'Main Zone Channel Volume Left Front Middle Input'
    },
    'CVTML DOWN': {
        'event': 'MainZone.ChannelVolume.LeftFrontMiddle.Down',
        'description': 'Main Zone Channel Volume Left Front Middle Down'
    },
    'CVTML UP': {
        'event': 'MainZone.ChannelVolume.LeftFrontMiddle.Up',
        'description': 'Main Zone Channel Volume Left Front Middle Up'
    },
    'CVTMR **': {
        'event': 'MainZone.ChannelVolume.RightFrontMiddle.**',
        'description': 'Main Zone Channel Volume Right Front Middle Input'
    },
    'CVTMR DOWN': {
        'event': 'MainZone.ChannelVolume.RightFrontMiddle.Down',
        'description': 'Main Zone Channel Volume Right Front Middle Down'
    },
    'CVTMR UP': {
        'event': 'MainZone.ChannelVolume.RightFrontMiddle.Up',
        'description': 'Main Zone Channel Volume Right Front Middle Up'
    },
    'CVTRL **': {
        'event': 'MainZone.ChannelVolume.LeftRearTop.**',
        'description': 'Main Zone Channel Volume Left Rear Top Input'
    },
    'CVTRL DOWN': {
        'event': 'MainZone.ChannelVolume.LeftRearTop.Down',
        'description': 'Main Zone Channel Volume Left Rear Top Down'
    },
    'CVTRL UP': {
        'event': 'MainZone.ChannelVolume.LeftRearTop.Up',
        'description': 'Main Zone Channel Volume Left Rear Top Up'
    },
    'CVTRR **': {
        'event': 'MainZone.ChannelVolume.RightRearTop.**',
        'description': 'Main Zone Channel Volume Right Rear Top Input'
    },
    'CVTRR DOWN': {
        'event': 'MainZone.ChannelVolume.RightRearTop.Down',
        'description': 'Main Zone Channel Volume Right Rear Top Down'
    },
    'CVTRR UP': {
        'event': 'MainZone.ChannelVolume.RightRearTop.Up',
        'description': 'Main Zone Channel Volume Right Rear Top Up'
    },
    'CVTS **': {
        'event': 'MainZone.ChannelVolume.SurroundTopAuro-3D.**',
        'description': 'Main Zone Channel Volume Surround Top Auro-3D  Input'
    },
    'CVTS DOWN': {
        'event': 'MainZone.ChannelVolume.SurroundTopAuro-3D.Down',
        'description': 'Main Zone Channel Volume Surround Top Auro-3D  Down'
    },
    'CVTS UP': {
        'event': 'MainZone.ChannelVolume.SurroundTopAuro-3D.Up',
        'description': 'Main Zone Channel Volume Surround Top Auro-3D  Up'
    },
    'CVZRL': {
        'event': 'MainZone.ChannelVolume.Reset',
        'description': 'Main Zone Channel Volume Reset'
    },
    'DCAUTO': {
        'event': 'MainZone.DigitalAudioInputMode.Auto',
        'description': 'Main Zone Digital Audio Input Mode Auto'
    },
    'DCDTS': {
        'event': 'MainZone.DigitalAudioInputMode.DTS',
        'description': 'Main Zone Digital Audio Input Mode DTS'
    },
    'DCPCM': {
        'event': 'MainZone.DigitalAudioInputMode.PCM',
        'description': 'Main Zone Digital Audio Input Mode PCM'
    },
    'DIM BRI': {
        'event': 'System.FrontPanelLightLevel.Bright',
        'description': 'System Front Panel Light Level Bright'
    },
    'DIM DAR': {
        'event': 'System.FrontPanelLightLevel.Dark',
        'description': 'System Front Panel Light Level Dark'
    },
    'DIM DIM': {
        'event': 'System.FrontPanelLightLevel.Dim',
        'description': 'System Front Panel Light Level Dim'
    },
    'DIM OFF': {
        'event': 'System.FrontPanelLightLevel.Off',
        'description': 'System Front Panel Light Level Off'
    },
    'DIM SEL': {
        'event': 'System.FrontPanelLightLevel.Toggle',
        'description': 'System Front Panel Light Level Toggle'
    },
    'ECOAUTO': {
        'event': 'MainZone.EcoMode.Auto',
        'description': 'Main Zone Eco Mode Auto'
    },
    'ECOOFF': {
        'event': 'MainZone.EcoMode.Off',
        'description': 'Main Zone Eco Mode Off'
    },
    'ECOON': {
        'event': 'MainZone.EcoMode.On',
        'description': 'Main Zone Eco Mode On'
    },
    'HDALBUM ****************************************': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDARTIST ****************************************': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDGENRE ***********************': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDMLT CAST CH *': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDMLT CURRCH *': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDMODE ANALOG': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDMODE DIGITAL': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDPTY ******************': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDSIG LEV 0': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDSIG LEV 1': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDSIG LEV 2': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDSIG LEV 3': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDSIG LEV 4': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDSIG LEV 5': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDSIG LEV 6': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDST NAME ********': {
        'event': 'HDRadio',
        'description': ''
    },
    'HDTITLE ****************************************': {
        'event': 'HDRadio',
        'description': ''
    },
    'MNCDN': {
        'event': 'System.DirectionPad.CursorDown',
        'description': 'System Direction Pad Cursor Down'
    },
    'MNCHL': {
        'event': 'System.DirectionPad.ChannelAdjustMenu',
        'description': 'System Direction Pad Channel Adjust Menu'
    },
    'MNCLT': {
        'event': 'System.DirectionPad.CursorLeft',
        'description': 'System Direction Pad Cursor Left'
    },
    'MNCRT': {
        'event': 'System.DirectionPad.CursorRight',
        'description': 'System Direction Pad Cursor Right'
    },
    'MNCUP': {
        'event': 'System.DirectionPad.CursorUp',
        'description': 'System Direction Pad Cursor Up'
    },
    'MNENT': {
        'event': 'System.DirectionPad.Enter',
        'description': 'System Direction Pad Enter'
    },
    'MNINF': {
        'event': 'System.DirectionPad.Info',
        'description': 'System Direction Pad Info'
    },
    'MNMEN OFF': {
        'event': 'System.DirectionPad.SetupMenuOff',
        'description': 'System Direction Pad Setup Menu Off'
    },
    'MNMEN ON': {
        'event': 'System.DirectionPad.SetupMenuOn',
        'description': 'System Direction Pad Setup Menu On'
    },
    'MNOPT': {
        'event': 'System.DirectionPad.Option',
        'description': 'System Direction Pad Option'
    },
    'MNRTN': {
        'event': 'System.DirectionPad.Return',
        'description': 'System Direction Pad Return'
    },
    'MNZST OFF': {
        'event': 'System.AllZoneStereo.Off',
        'description': 'System All Zone Stereo Off'
    },
    'MNZST ON': {
        'event': 'System.AllZoneStereo.On',
        'description': 'System All Zone Stereo On'
    },
    'MSAAC+DOLBY EX': {
        'event': 'MainZone.SurroundMode.AAC.Dolby.EX',
        'description': ''
    },
    'MSAAC+DS': {
        'event': 'MainZone.SurroundMode.AAC.DigitalSurround',
        'description': ''
    },
    'MSAAC+NEO:X C': {
        'event': 'MainZone.SurroundMode.AAC.Neo:X.Cinema',
        'description': ''
    },
    'MSAAC+NEO:X G': {
        'event': 'MainZone.SurroundMode.AAC.Neo:X.Music.Game',
        'description': ''
    },
    'MSAAC+NEO:X M': {
        'event': 'MainZone.SurroundMode.AAC.Neo:X.Music',
        'description': ''
    },
    'MSAAC+NEURAL:X': {
        'event': 'MainZone.SurroundMode.AAC.Neutral:X',
        'description': ''
    },
    'MSAAC+PL2X C': {
        'event': 'MainZone.SurroundMode.AAC.PrologicIIx.Cinema',
        'description': ''
    },
    'MSAAC+PL2X M': {
        'event': 'MainZone.SurroundMode.AAC.PrologicIIx.Music',
        'description': ''
    },
    'MSAAC+PL2Z H': {
        'event': 'MainZone.SurroundMode.AAC.PrologicIIz.Headphones',
        'description': ''
    },
    'MSAUDYSSEY DSX': {
        'event': 'MainZone.SurroundMode.Audyssey.DSX',
        'description': ''
    },
    'MSAURO2DSURR': {
        'event': 'MainZone.SurroundMode.Auro2D',
        'description': 'Main Zone Surround Mode Auro 2D'
    },
    'MSAURO3D': {
        'event': 'MainZone.SurroundMode.Auro3D',
        'description': 'Main Zone Surround Mode Auro 3D'
    },
    'MSAUTO': {
        'event': 'MainZone.SurroundMode.Auto',
        'description': 'Main Zone Surround Mode Auto'
    },
    'MSCLASSIC CONCERT': {
        'event': 'MainZone.SurroundMode.ClassicConcert',
        'description': 'Main Zone Surround Mode Classic Concert'
    },
    'MSDIRECT': {
        'event': 'MainZone.SurroundMode.Direct',
        'description': 'Main Zone Surround Mode Direct'
    },
    'MSDOLBY ATMOS': {
        'event': 'MainZone.SurroundMode.Dolby.Atmos',
        'description': ''
    },
    'MSDOLBY D EX': {
        'event': 'MainZone.SurroundMode.Dolby.Digital.EX',
        'description': ''
    },
    'MSDOLBY D+': {
        'event': 'MainZone.SurroundModeDolby.Digital+',
        'description': ''
    },
    'MSDOLBY D+ +DS': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-DigitalSurround',
        'description': ''
    },
    'MSDOLBY D+ +EX': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-EX',
        'description': ''
    },
    'MSDOLBY D+ +NEO:X C': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-Neo:X.Cinema',
        'description': ''
    },
    'MSDOLBY D+ +NEO:X G': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-Neo:X.Game',
        'description': ''
    },
    'MSDOLBY D+ +NEO:X M': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-Neo:X.Music',
        'description': ''
    },
    'MSDOLBY D+ +NEURAL:X': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-Neutral:X',
        'description': ''
    },
    'MSDOLBY D+ +PL2X C': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-PrologicIIx.Cinema',
        'description': ''
    },
    'MSDOLBY D+ +PL2X M': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-PrologicIIx.Music',
        'description': ''
    },
    'MSDOLBY D+ +PL2Z H': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-PrologicIIz.Headphones',
        'description': ''
    },
    'MSDOLBY D+ +PLZ H': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+-PrologicZ.Headphones',
        'description': ''
    },
    'MSDOLBY D+DS': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+.DigitalSurround',
        'description': ''
    },
    'MSDOLBY D+NEO:X C': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+.Neo:X.Cinema',
        'description': ''
    },
    'MSDOLBY D+NEO:X G': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+.Neo:X.Game',
        'description': ''
    },
    'MSDOLBY D+NEO:X M': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+.Neo:X.Music',
        'description': ''
    },
    'MSDOLBY D+NEURAL:X': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+.Neo:X.Music',
        'description': ''
    },
    'MSDOLBY D+PL2X C': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+.PrologicIIx.Cinema',
        'description': ''
    },
    'MSDOLBY D+PL2X M': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+.PrologicIIx.Music',
        'description': ''
    },
    'MSDOLBY D+PL2Z H': {
        'event': 'MainZone.SurroundMode.Dolby.Digital+.PrologicIIz.Headphones',
        'description': ''
    },
    'MSDOLBY DIGITAL': {
        'event': 'MainZone.SurroundMode.DolbyDigital',
        'description': 'Main Zone Surround Mode Dolby Digital'
    },
    'MSDOLBY HD': {
        'event': 'MainZone.SurroundMode.Dolby.HD',
        'description': ''
    },
    'MSDOLBY HD+DS': {
        'event': 'MainZone.SurroundMode.Dolby.HD-DigitalSurround',
        'description': ''
    },
    'MSDOLBY HD+EX': {
        'event': 'MainZone.SurroundMode.Dolby.HD-EX',
        'description': ''
    },
    'MSDOLBY HD+NEO:X C': {
        'event': 'MainZone.SurroundMode.Dolby.HD-Neo:X.Cinema',
        'description': ''
    },
    'MSDOLBY HD+NEO:X G': {
        'event': 'MainZone.SurroundMode.Dolby.HD-Neo:X.Game',
        'description': ''
    },
    'MSDOLBY HD+NEO:X M': {
        'event': 'MainZone.SurroundMode.Dolby.HD-Neo:X.Music',
        'description': ''
    },
    'MSDOLBY HD+NEURAL:X': {
        'event': 'MainZone.SurroundMode.Dolby.HD-Neutral:X',
        'description': ''
    },
    'MSDOLBY HD+PL2X C': {
        'event': 'MainZone.SurroundMode.Dolby.HD-PrologicIIx.Cinema',
        'description': ''
    },
    'MSDOLBY HD+PL2X M': {
        'event': 'MainZone.SurroundMode.Dolby.HD-PrologicIIx.Music',
        'description': ''
    },
    'MSDOLBY HD+PL2Z H': {
        'event': 'MainZone.SurroundMode.Dolby.HD-PrologicIIz.Headphones',
        'description': ''
    },
    'MSDOLBY PL2 C': {
        'event': 'MainZone.SurroundMode.Dolby.PrologicII.Cinema',
        'description': ''
    },
    'MSDOLBY PL2 G': {
        'event': 'MainZone.SurroundMode.Dolby.PrologicII.Game',
        'description': ''
    },
    'MSDOLBY PL2 M': {
        'event': 'MainZone.SurroundMode.Dolby.PrologicII.Music',
        'description': ''
    },
    'MSDOLBY PL2X C': {
        'event': 'MainZone.SurroundMode.Dolby.PrologicIIx.Cinema',
        'description': ''
    },
    'MSDOLBY PL2X G': {
        'event': 'MainZone.SurroundMode.Dolby.PrologicIIx.Game',
        'description': ''
    },
    'MSDOLBY PL2X M': {
        'event': 'MainZone.SurroundMode.Dolby.PrologicIIx.Music',
        'description': ''
    },
    'MSDOLBY PL2Z H': {
        'event': 'MainZone.SurroundMode.Dolby.PrologicIIz.Headphones',
        'description': ''
    },
    'MSDOLBY PRO LOGIC': {
        'event': 'MainZone.SurroundMode.Dolby.ProLogic',
        'description': ''
    },
    'MSDOLBY SURROUND': {
        'event': 'MainZone.SurroundMode.Dolby.Surround',
        'description': ''
    },
    'MSDSD DIRECT': {
        'event': 'MainZone.SurroundMode.DSD.Direct',
        'description': ''
    },
    'MSDSD PURE DIRECT': {
        'event': 'MainZone.SurroundMode.DSD.Pure.Direct',
        'description': ''
    },
    'MSDTS ES 8CH DSCRT': {
        'event': 'MainZone.SurroundMode.DTS.ES.8Channel.Discrete',
        'description': ''
    },
    'MSDTS ES DSCRT+NEURAL:X': {
        'event': 'MainZone.SurroundMode.DTS.ES.Discrete.Neutral:X',
        'description': ''
    },
    'MSDTS ES DSCRT6.1': {
        'event': 'MainZone.SurroundMode.DTS.ES.Discrete.6.1',
        'description': ''
    },
    'MSDTS ES MTRX+NEURAL:X': {
        'event': 'MainZone.SurroundMode.DTS.Matrix.Neutral:X',
        'description': ''
    },
    'MSDTS ES MTRX6.1': {
        'event': 'MainZone.SurroundMode.DTS.ES.Matrix.6.1',
        'description': ''
    },
    'MSDTS EXPRESS': {
        'event': 'MainZone.SurroundMode.DTS.Express',
        'description': ''
    },
    'MSDTS HD': {
        'event': 'MainZone.SurroundMode.DTS.HD',
        'description': ''
    },
    'MSDTS HD MSTR': {
        'event': 'MainZone.SurroundMode.DTS.HD.Master',
        'description': ''
    },
    'MSDTS HD+DS': {
        'event': 'MainZone.SurroundMode.DTS.HD.DolbySurround',
        'description': ''
    },
    'MSDTS HD+NEO:6': {
        'event': 'MainZone.SurroundMode.DTS.HD.Neo:6',
        'description': ''
    },
    'MSDTS HD+NEO:X C': {
        'event': 'MainZone.SurroundMode.DTS.HD.Neo:X.Cinema',
        'description': ''
    },
    'MSDTS HD+NEO:X G': {
        'event': 'MainZone.SurroundMode.DTS.HD.Neo:X.Game',
        'description': ''
    },
    'MSDTS HD+NEO:X M': {
        'event': 'MainZone.SurroundMode.DTS.HD.Neo:X.Music',
        'description': ''
    },
    'MSDTS HD+NEURAL:X': {
        'event': 'MainZone.SurroundMode.DTS.Neutral:X',
        'description': ''
    },
    'MSDTS HD+PL2X C': {
        'event': 'MainZone.SurroundMode.DTS.ProLogicIIx.Cinema',
        'description': ''
    },
    'MSDTS HD+PL2X M': {
        'event': 'MainZone.SurroundMode.DTS.ProLogicIIx.Music',
        'description': ''
    },
    'MSDTS HD+PL2Z H': {
        'event': 'MainZone.SurroundMode.DTS.PrologixIIz.Headphones',
        'description': ''
    },
    'MSDTS NEO:6 C': {
        'event': 'MainZone.SurroundMode.DTS.Neo:6.Cinema',
        'description': ''
    },
    'MSDTS NEO:6 M': {
        'event': 'MainZone.SurroundMode.DTS.Neo:6.Music',
        'description': ''
    },
    'MSDTS NEO:X C': {
        'event': 'MainZone.SurroundMode.DTS.Neo:X.Cinema',
        'description': ''
    },
    'MSDTS NEO:X G': {
        'event': 'MainZone.SurroundMode.DTS.Neo:X.Game',
        'description': ''
    },
    'MSDTS NEO:X M': {
        'event': 'MainZone.SurroundMode.DTS.Neo:X.Music',
        'description': ''
    },
    'MSDTS SURROUND': {
        'event': 'MainZone.SurroundMode.DTS',
        'description': 'Main Zone Surround Mode DTS'
    },
    'MSDTS+DS': {
        'event': 'MainZone.SurroundMode.DTS-DolbySurround',
        'description': ''
    },
    'MSDTS+NEO:6': {
        'event': 'MainZone.SurroundMode.DTS-Neo:6',
        'description': ''
    },
    'MSDTS+NEO:X C': {
        'event': 'MainZone.SurroundMode.DTS-Neo:X.Cinema',
        'description': ''
    },
    'MSDTS+NEO:X G': {
        'event': 'MainZone.SurroundMode.DTS-Neo:X.Game',
        'description': ''
    },
    'MSDTS+NEO:X M': {
        'event': 'MainZone.SurroundMode.DTS-Neo:X.Music',
        'description': ''
    },
    'MSDTS+NEURAL:X': {
        'event': 'MainZone.SurroundMode.DTS-Neutral:X',
        'description': ''
    },
    'MSDTS+PL2X C': {
        'event': 'MainZone.SurroundMode.DTS-PrologicIIx.Cinema',
        'description': ''
    },
    'MSDTS+PL2X M': {
        'event': 'MainZone.SurroundMode.DTS-PrologicIIx.Music',
        'description': ''
    },
    'MSDTS+PL2Z H': {
        'event': 'MainZone.SurroundMode.DTS-PrologicIIz.Headphones',
        'description': ''
    },
    'MSDTS96 ES MTRX': {
        'event': 'MainZone.SurroundMode.DTS96.ES.Matrix',
        'description': ''
    },
    'MSDTS96/24': {
        'event': 'MainZone.SurroundMode.DTS96/24',
        'description': ''
    },
    'MSDTS:X': {
        'event': 'MainZone.SurroundMode.DTS:X',
        'description': ''
    },
    'MSDTS:X MSTR': {
        'event': 'MainZone.SurroundMode.DTS:X.Master',
        'description': ''
    },
    'MSGAME': {
        'event': 'MainZone.SurroundMode.Game',
        'description': 'Main Zone Surround Mode Game'
    },
    'MSJAZZ CLUB': {
        'event': 'MainZone.SurroundMode.JazzClub',
        'description': 'Main Zone Surround Mode Jazz Club'
    },
    'MSLEFT': {
        'event': 'MainZone.SurroundMode.Left',
        'description': 'Main Zone Surround Mode Left'
    },
    'MSM CH IN+DOLBY EX': {
        'event': 'MainZone.SurroundMode.MultiChannelIn-Dolby.EX',
        'description': ''
    },
    'MSM CH IN+DS': {
        'event': 'MainZone.SurroundMode.MultiChannelIn-DolbySurround',
        'description': ''
    },
    'MSM CH IN+NEO:X C': {
        'event': 'MainZone.SurroundMode.MultiChannelIn-Neo:X.Cinema',
        'description': ''
    },
    'MSM CH IN+NEO:X G': {
        'event': 'MainZone.SurroundMode.MultiChannelIn-Neo:X.Game',
        'description': ''
    },
    'MSM CH IN+NEO:X M': {
        'event': 'MainZone.SurroundMode.MultiChannelIn-Neo:X.Music',
        'description': ''
    },
    'MSM CH IN+NEURAL:X': {
        'event': 'MainZone.SurroundMode.MultiChannelIn-Neutral:X',
        'description': ''
    },
    'MSM CH IN+PL2X C': {
        'event': 'MainZone.SurroundMode.MultiChannelIn-PrologicIIx.Cinema',
        'description': ''
    },
    'MSM CH IN+PL2X M': {
        'event': 'MainZone.SurroundMode.MultiChannelIn-PrologicIIx.Music',
        'description': ''
    },
    'MSM CH IN+PL2Z H': {
        'event': 'MainZone.SurroundMode.MultiChannelIn-PrologicIIz.Headphones',
        'description': ''
    },
    'MSMATRIX': {
        'event': 'MainZone.SurroundMode.Matrix',
        'description': 'Main Zone Surround Mode Matrix'
    },
    'MSMCH STEREO': {
        'event': 'MainZone.SurroundMode.MultiChannel.Stereo',
        'description': 'Main Zone Surround Mode Multi Channel Stereo'
    },
    'MSMONO MOVIE': {
        'event': 'MainZone.SurroundMode.Mono.Movie',
        'description': 'Main Zone Surround Mode Mono Movie'
    },
    'MSMOVIE': {
        'event': 'MainZone.SurroundMode.Movie',
        'description': 'Main Zone Surround Mode Movie'
    },
    'MSMPEG2 AAC': {
        'event': 'MainZone.SurroundMode.MPEG2.AAC',
        'description': ''
    },
    'MSMULTI CH IN': {
        'event': 'MainZone.SurroundMode.MultiChannelIn',
        'description': ''
    },
    'MSMULTI CH IN 7.1': {
        'event': 'MainZone.SurroundMode.MultiChannelIn.7.1',
        'description': ''
    },
    'MSMUSIC': {
        'event': 'MainZone.SurroundMode.Music',
        'description': 'Main Zone Surround Mode Music'
    },
    'MSNEO:6 C DSX': {
        'event': 'MainZone.SurroundMode.Neo:6.Cinema.DSX',
        'description': ''
    },
    'MSNEO:6 M DSX': {
        'event': 'MainZone.SurroundMode.Neo:6.Music.DSX',
        'description': ''
    },
    'MSNEURAL:X': {
        'event': 'MainZone.SurroundMode.Neutral:X',
        'description': ''
    },
    'MSPL DSX': {
        'event': 'MainZone.SurroundMode.ProLogic.DXS',
        'description': ''
    },
    'MSPL2 C DSX': {
        'event': 'MainZone.SurroundMode.ProLogicII.Cinema.DSX',
        'description': ''
    },
    'MSPL2 G DSX': {
        'event': 'MainZone.SurroundMode.ProLogicII.Game.DSX',
        'description': ''
    },
    'MSPL2 M DSX': {
        'event': 'MainZone.SurroundMode.ProLogic2.Music.DSX',
        'description': ''
    },
    'MSPL2X C DSX': {
        'event': 'MainZone.SurroundMode.ProLogicIIx.Cinema.DSX',
        'description': ''
    },
    'MSPL2X G DSX': {
        'event': 'MainZone.SurroundMode.ProLogicIIx.Game.DSX',
        'description': ''
    },
    'MSPL2X M DSX': {
        'event': 'MainZone.SurroundMode.ProLogicIIx.Music.DSX',
        'description': ''
    },
    'MSPURE DIRECT': {
        'event': 'MainZone.SurroundMode.PureDirect',
        'description': 'Main Zone Surround Mode Pure Direct'
    },
    'MSQUCIK4 MEMORY': {
        'event': 'MainZone.SurroundMode.QuickMemorySelect.4',
        'description': 'Main Zone Surround Mode Quick Memory Select 4'
    },
    'MSQUICK1': {
        'event': 'MainZone.SurroundMode.QuickSelect.1',
        'description': 'Main Zone Surround Mode Quick Select 1'
    },
    'MSQUICK2': {
        'event': 'MainZone.SurroundMode.QuickSelect.2',
        'description': 'Main Zone Surround Mode Quick Select 2'
    },
    'MSQUICK2 MEMORY': {
        'event': 'MainZone.SurroundMode.QuickMemorySelect.2',
        'description': 'Main Zone Surround Mode Quick Memory Select 2'
    },
    'MSQUICK3': {
        'event': 'MainZone.SurroundMode.QuickSelect.3',
        'description': 'Main Zone Surround Mode Quick Select 3'
    },
    'MSQUICK3 MEMORY': {
        'event': 'MainZone.SurroundMode.QuickMemorySelect.3',
        'description': 'Main Zone Surround Mode Quick Memory Select 3'
    },
    'MSQUICK4': {
        'event': 'MainZone.SurroundMode.QuickSelect.4',
        'description': 'Main Zone Surround Mode Quick Select 4'
    },
    'MSQUICK5': {
        'event': 'MainZone.SurroundMode.QuickSelect.5',
        'description': 'Main Zone Surround Mode Quick Select 5'
    },
    'MSQUICK5 MEMORY': {
        'event': 'MainZone.SurroundMode.QuickMemorySelect.5',
        'description': 'Main Zone Surround Mode Quick Memory Select 5'
    },
    'MSRIGHT': {
        'event': 'MainZone.SurroundMode.Right',
        'description': 'Main Zone Surround Mode Right'
    },
    'MSROCK ARENA': {
        'event': 'MainZone.SurroundMode.RockArena',
        'description': 'Main Zone Surround Mode Rock Arena'
    },
    'MSSTEREO': {
        'event': 'MainZone.SurroundMode.Stereo',
        'description': 'Main Zone Surround Mode Stereo'
    },
    'MSSUPER STADIUM': {
        'event': 'MainZone.SurroundMode.SuperStadium',
        'description': 'Main Zone Surround Mode Super Stadium'
    },
    'MSVIDEO GAME': {
        'event': 'MainZone.SurroundMode.VideoGame',
        'description': 'Main Zone Surround Mode Video Game'
    },
    'MSVIRTUAL': {
        'event': 'MainZone.SurroundMode.Virtual',
        'description': 'Main Zone Surround Mode Virtual'
    },
    'MSWIDE SCREEN': {
        'event': 'MainZone.SurroundMode.WideScreen',
        'description': 'Main Zone Surround Mode Wide Screen'
    },
    'MUOFF': {
        'event': 'MainZone.Mute.Off',
        'description': 'Main Zone Mute Off'
    },
    'MUON': {
        'event': 'MainZone.Mute.On',
        'description': 'Main Zone Mute On'
    },
    'MV**': {
        'event'      : 'MainZone.Volume.**',
        'description': 'Main Zone Volume Direct'
    },
    'MV***': {
        'event': 'MainZone.Volume.***',
        'description': 'Main Zone Volume Direct'
    },
    'MVDOWN': {
        'event': 'MainZone.Volume.Down',
        'description': 'Main Zone Volume Down'
    },
    'MVUP': {
        'event': 'MainZone.Volume.Up',
        'description': 'Main Zone Volume Up'
    },
    'NS90': {
        'event': 'NetAudio.CursorUp',
        'description': 'Net Audio Cursor Up'
    },
    'NS91': {
        'event': 'NetAudio.CursorDown',
        'description': 'Net Audio Cursor Down'
    },
    'NS92': {
        'event': 'NetAudio.CursorLeft',
        'description': 'Net Audio Cursor Left'
    },
    'NS93': {
        'event': 'NetAudio.CursorRight',
        'description': 'Net Audio Cursor Right'
    },
    'NS94': {
        'event': 'NetAudio.Enter',
        'description': 'Net Audio Enter'
    },
    'NS9A': {
        'event': 'NetAudio.Play',
        'description': 'Net Audio Play'
    },
    'NS9B': {
        'event': 'NetAudio.Pause',
        'description': 'Net Audio Pause'
    },
    'NS9C': {
        'event': 'NetAudio.Stop',
        'description': 'Net Audio Stop'
    },
    'NS9D': {
        'event': 'NetAudio.SkipForward',
        'description': 'Net Audio Skip Forward'
    },
    'NS9E': {
        'event': 'NetAudio.SkipBack',
        'description': 'Net Audio Skip Back'
    },
    'NS9F': {
        'event': 'NetAudio.FastForward',
        'description': 'Net Audio Fast Forward'
    },
    'NS9G': {
        'event': 'NetAudio.Rewind',
        'description': 'Net Audio Rewind'
    },
    'NS9H': {
        'event': 'NetAudio.Repeat',
        'description': 'Net Audio Repeat'
    },
    'NS9I': {
        'event': 'NetAudio.RepeatAll',
        'description': 'Net Audio Repeat All'
    },
    'NS9J': {
        'event': 'NetAudio.RepeatOff',
        'description': 'Net Audio Repeat Off'
    },
    'NS9K': {
        'event': 'NetAudio.RandomOn',
        'description': 'Net Audio Random On'
    },
    'NS9M': {
        'event': 'NetAudio.RandomOff',
        'description': 'Net Audio Random Off'
    },
    'NS9W': {
        'event': 'NetAudio.iPodMode/OnScreenMode',
        'description': 'Net Audio iPod Mode/On Screen Mode'
    },
    'NS9X': {
        'event': 'NetAudio.NextPage',
        'description': 'Net Audio Next Page'
    },
    'NS9Y': {
        'event': 'NetAudio.PreviousPage',
        'description': 'Net Audio Previous Page'
    },
    'NS9Z': {
        'event': 'NetAudio.StopFF/REW',
        'description': 'Net Audio Stop FF/REW'
    },
    'NSB**': {
        'event': 'NetAudio.PresetInput.**',
        'description': 'Net Audio Preset Input'
    },
    'NSC**': {
        'event': 'NetAudio.PresetMemoryInput.**',
        'description': 'Net Audio Preset Memory Input'
    },
    'NSCOK': {
        'event': 'Net.MemoryInput.OK',
        'description': ''
    },
    'NSH': {
        'event': 'NetAudio.PresetNameStatus',
        'description': 'Net Audio Preset Name Status'
    },
    'NSH**********************': {
        'event': 'Net.PresetName',
        'description': ''
    },
    'NSRND': {
        'event': 'NetAudio.RandomOn/Off',
        'description': 'Net Audio Random On/Off'
    },
    'NSRPT': {
        'event': 'NetAudio.RepeatOn/Off',
        'description': 'Net Audio Repeat On/Off'
    },
    'PSAUROPR LAR': {
        'event': 'MainZone.OtherSettings.AuroMatic3DPreset.Large',
        'description': 'Main Zone Other Settings Auro Matic 3D Preset Large'
    },
    'PSAUROPR MED': {
        'event': 'MainZone.OtherSettings.AuroMatic3DPreset.Medium',
        'description': 'Main Zone Other Settings Auro Matic 3D Preset Medium'
    },
    'PSAUROPR SMA': {
        'event': 'MainZone.OtherSettings.AuroMatic3DPreset.Small',
        'description': 'Main Zone Other Settings Auro Matic 3D Preset Small'
    },
    'PSAUROPR SPE': {
        'event': 'MainZone.OtherSettings.AuroMatic3DPreset.Special',
        'description': 'Main Zone Other Settings Auro Matic 3D Preset Special'
    },
    'PSAUROST **': {
        'event': 'MainZone.OtherSettings.AuroMaticStrength.**',
        'description': 'Main Zone Other Settings Auro Matic Strength Input'
    },
    'PSAUROST DOWN': {
        'event': 'MainZone.OtherSettings.AuroMaticStrength.Down',
        'description': 'Main Zone Other Settings Auro Matic Strength Down'
    },
    'PSAUROST UP': {
        'event': 'MainZone.OtherSettings.AuroMaticStrength.Up',
        'description': 'Main Zone Other Settings Auro Matic Strength Up'
    },
    'PSBAS **': {
        'event': 'MainZone.OtherSettings.Bass.**',
        'description': 'Main Zone Other Settings Bass Input'
    },
    'PSBAS DOWN': {
        'event': 'MainZone.OtherSettings.Bass.Down',
        'description': 'Main Zone Other Settings Bass Down'
    },
    'PSBAS UP': {
        'event': 'MainZone.OtherSettings.Bass.Up',
        'description': 'Main Zone Other Settings Bass Up'
    },
    'PSBSC **': {
        'event': 'MainZone.OtherSettings.BassSync.**',
        'description': 'Main Zone Other Settings Bass Sync Input'
    },
    'PSBSC DOWN': {
        'event': 'MainZone.OtherSettings.BassSync.Down',
        'description': 'Main Zone Other Settings Bass Sync Down'
    },
    'PSBSC UP': {
        'event': 'MainZone.OtherSettings.BassSync.Up',
        'description': 'Main Zone Other Settings Bass Sync Up'
    },
    'PSCES OFF': {
        'event': 'MainZone.OtherSettings.CenterSpread.Off',
        'description': 'Main Zone Other Settings Center Spread Off'
    },
    'PSCES ON': {
        'event': 'MainZone.OtherSettings.CenterSpread.On',
        'description': 'Main Zone Other Settings Center Spread On'
    },
    'PSCINEMA EQ.OFF': {
        'event': 'MainZone.OtherSettings.CinemaEQ.Off',
        'description': 'Main Zone Other Settings Cinema EQ Off'
    },
    'PSCINEMA EQ.ON': {
        'event': 'MainZone.OtherSettings.CinemaEQ.On',
        'description': 'Main Zone Other Settings Cinema EQ On'
    },
    'PSCNTAMT **': {
        'event': 'MainZone.OtherSettings.Containment.**',
        'description': 'Main Zone Other Settings Containment Input'
    },
    'PSCNTAMT DOWN': {
        'event': 'MainZone.OtherSettings.Containment.Down',
        'description': 'Main Zone Other Settings Containment Down'
    },
    'PSCNTAMT UP': {
        'event': 'MainZone.OtherSettings.Containment.Up',
        'description': 'Main Zone Other Settings Containment Up'
    },
    'PSDEH HIGH': {
        'event': 'MainZone.OtherSettings.DialogEnhancer.Hight',
        'description': 'Main Zone Other Settings Dialog Enhancer Hight'
    },
    'PSDEH LOW': {
        'event': 'MainZone.OtherSettings.DialogEnhancer.Low',
        'description': 'Main Zone Other Settings Dialog Enhancer Low'
    },
    'PSDEH MED': {
        'event': 'MainZone.OtherSettings.DialogEnhancer.Medium',
        'description': 'Main Zone Other Settings Dialog Enhancer Medium'
    },
    'PSDEH OFF': {
        'event': 'MainZone.OtherSettings.DialogEnhancer.Off',
        'description': 'Main Zone Other Settings Dialog Enhancer Off'
    },
    'PSDEL ***': {
        'event': 'MainZone.OtherSettings.Delay.***',
        'description': 'Main Zone Other Settings Delay Input'
    },
    'PSDEL DOWN': {
        'event': 'MainZone.OtherSettings.Delay.Down',
        'description': 'Main Zone Other Settings Delay Down'
    },
    'PSDEL UP': {
        'event': 'MainZone.OtherSettings.Delay.Up',
        'description': 'Main Zone Other Settings Delay Up'
    },
    'PSDELAY ***': {
        'event': 'MainZone.OtherSettings.AudioDelay.***',
        'description': 'Main Zone Other Settings Audio Delay Input'
    },
    'PSDELAY DOWN': {
        'event': 'MainZone.OtherSettings.AudioDelay.Down',
        'description': 'Main Zone Other Settings Audio Delay Down'
    },
    'PSDELAY UP': {
        'event': 'MainZone.OtherSettings.AudioDelay.Up',
        'description': 'Main Zone Other Settings Audio Delay Up'
    },
    'PSDIC **': {
        'event': 'MainZone.OtherSettings.DialogControl.**',
        'description': 'Main Zone Other Settings Dialog Control Input'
    },
    'PSDIC DOWN': {
        'event': 'MainZone.OtherSettings.DialogControl.Down',
        'description': 'Main Zone Other Settings Dialog Control Down'
    },
    'PSDIC UP': {
        'event': 'MainZone.OtherSettings.DialogControl.Up',
        'description': 'Main Zone Other Settings Dialog Control Up'
    },
    'PSDIL **': {
        'event': 'MainZone.OtherSettings.DialogLevel.**',
        'description': 'Main Zone Other Settings Dialog Level Input'
    },
    'PSDIL DOWN': {
        'event': 'MainZone.OtherSettings.DialogLevel.Down',
        'description': 'Main Zone Other Settings Dialog Level Down'
    },
    'PSDIL OFF': {
        'event': 'MainZone.OtherSettings.DialogLevel.Off',
        'description': 'Main Zone Other Settings Dialog Level Off'
    },
    'PSDIL ON': {
        'event': 'MainZone.OtherSettings.DialogLevel.On',
        'description': 'Main Zone Other Settings Dialog Level On'
    },
    'PSDIL UP': {
        'event': 'MainZone.OtherSettings.DialogLevel.Up',
        'description': 'Main Zone Other Settings Dialog Level Up'
    },
    'PSDRC AUTO': {
        'event': 'MainZone.OtherSettings.DynamicCompression.Auto',
        'description': 'Main Zone Other Settings Dynamic Compression Auto'
    },
    'PSDRC HI': {
        'event': 'MainZone.OtherSettings.DynamicCompression.Hi',
        'description': 'Main Zone Other Settings Dynamic Compression Hi'
    },
    'PSDRC LOW ': {
        'event': 'MainZone.OtherSettings.DynamicCompression.Low',
        'description': 'Main Zone Other Settings Dynamic Compression Low'
    },
    'PSDRC MID': {
        'event': 'MainZone.OtherSettings.DynamicCompression.Mid',
        'description': 'Main Zone Other Settings Dynamic Compression Mid'
    },
    'PSDRC OFF': {
        'event': 'MainZone.OtherSettings.DynamicCompression.Off',
        'description': 'Main Zone Other Settings Dynamic Compression Off'
    },
    'PSDSX OFF': {
        'event': 'MainZone.OtherSettings.AudysseyDSX.Off',
        'description': 'Main Zone Other Settings Audyssey DSX Off'
    },
    'PSDSX ONH': {
        'event': 'MainZone.OtherSettings.AudysseyDSX.Height',
        'description': 'Main Zone Other Settings Audyssey DSX Height'
    },
    'PSDSX ONHW': {
        'event': 'MainZone.OtherSettings.AudysseyDSX.HeightandWide',
        'description': 'Main Zone Other Settings Audyssey DSX Height and Wide'
    },
    'PSDSX ONW': {
        'event': 'MainZone.OtherSettings.AudysseyDSX.Wide',
        'description': 'Main Zone Other Settings Audyssey DSX Wide'
    },
    'PSDYNEQ OFF': {
        'event': 'MainZone.OtherSettings.DynamicEQ.Off',
        'description': 'Main Zone Other Settings Dynamic EQ Off'
    },
    'PSDYNEQ ON': {
        'event': 'MainZone.OtherSettings.DynamicEQ.On',
        'description': 'Main Zone Other Settings Dynamic EQ On'
    },
    'PSDYNVOL HEV': {
        'event': 'MainZone.OtherSettings.DynamicVolume.Heavy',
        'description': 'Main Zone Other Settings Dynamic Volume Heavy'
    },
    'PSDYNVOL LIT': {
        'event': 'MainZone.OtherSettings.DynamicVolume.Light',
        'description': 'Main Zone Other Settings Dynamic Volume Light'
    },
    'PSDYNVOL MED': {
        'event': 'MainZone.OtherSettings.DynamicVolume.Medium',
        'description': 'Main Zone Other Settings Dynamic Volume Medium'
    },
    'PSDYNVOL OFF': {
        'event': 'MainZone.OtherSettings.DynamicVolume.Off',
        'description': 'Main Zone Other Settings Dynamic Volume Off'
    },
    'PSEFF **': {
        'event': 'MainZone.OtherSettings.EffectLevel.**',
        'description': 'Main Zone Other Settings Effect Level Input'
    },
    'PSEFF DOWN': {
        'event': 'MainZone.OtherSettings.EffectLevel.Down',
        'description': 'Main Zone Other Settings Effect Level Down'
    },
    'PSEFF OFF': {
        'event': 'MainZone.OtherSettings.EffectLevel.Off',
        'description': 'Main Zone Other Settings Effect Level Off'
    },
    'PSEFF ON': {
        'event': 'MainZone.OtherSettings.EffectLevel.On',
        'description': 'Main Zone Other Settings Effect Level On'
    },
    'PSEFF UP': {
        'event': 'MainZone.OtherSettings.EffectLevel.Up',
        'description': 'Main Zone Other Settings Effect Level Up'
    },
    'PSFRONT A+B': {
        'event': 'MainZone.OtherSettings.FrontSpeaker.A+B',
        'description': 'Main Zone Other Settings Front Speaker A + B'
    },
    'PSFRONT SPA': {
        'event': 'MainZone.OtherSettings.FrontSpeaker.A',
        'description': 'Main Zone Other Settings Front Speaker A'
    },
    'PSFRONT SPB': {
        'event': 'MainZone.OtherSettings.FrontSpeaker.B',
        'description': 'Main Zone Other Settings Front Speaker B'
    },
    'PSGEQ OFF': {
        'event': 'MainZone.OtherSettings.GraphicEQ.Off',
        'description': 'Main Zone Other Settings Graphic EQ Off'
    },
    'PSGEQ ON': {
        'event': 'MainZone.OtherSettings.GraphicEQ.On',
        'description': 'Main Zone Other Settings Graphic EQ On'
    },
    'PSHEQ OFF': {
        'event': 'MainZone.OtherSettings.HeadphoneEQ.Off',
        'description': 'Main Zone Other Settings Headphone EQ Off'
    },
    'PSHEQ ON': {
        'event': 'MainZone.OtherSettings.HeadphoneEQ.On',
        'description': 'Main Zone Other Settings Headphone EQ On'
    },
    'PSLFC OFF': {
        'event': 'MainZone.OtherSettings.AudysseyLFC.Off',
        'description': 'Main Zone Other Settings Audyssey LFC Off'
    },
    'PSLFC ON': {
        'event': 'MainZone.OtherSettings.AudysseyLFC.On',
        'description': 'Main Zone Other Settings Audyssey LFC On'
    },
    'PSLFE **': {
        'event': 'MainZone.OtherSettings.LFE.**',
        'description': 'Main Zone Other Settings LFE Input'
    },
    'PSLFE DOWN': {
        'event': 'MainZone.OtherSettings.LFE.Down',
        'description': 'Main Zone Other Settings LFE Down'
    },
    'PSLFE UP': {
        'event': 'MainZone.OtherSettings.LFE.Up',
        'description': 'Main Zone Other Settings LFE Up'
    },
    'PSLFL 00': {
        'event': 'MainZone.OtherSettings.LFELevel.00',
        'description': 'Main Zone Other Settings LFE Level 00'
    },
    'PSLFL 05': {
        'event': 'MainZone.OtherSettings.LFELevel.05',
        'description': 'Main Zone Other Settings LFE Level 05'
    },
    'PSLFL 10': {
        'event': 'MainZone.OtherSettings.LFELevel.10',
        'description': 'Main Zone Other Settings LFE Level 10'
    },
    'PSLFL 15': {
        'event': 'MainZone.OtherSettings.LFELevel.15',
        'description': 'Main Zone Other Settings LFE Level 15'
    },
    'PSMULTEQ:AUDYSSEY': {
        'event': 'MainZone.OtherSettings.MultiEQ.Audyssey',
        'description': 'Main Zone Other Settings Multi EQ Audyssey'
    },
    'PSMULTEQ:BYP.LR': {
        'event': 'MainZone.OtherSettings.MultiEQ.Bypass',
        'description': 'Main Zone Other Settings Multi EQ Bypass'
    },
    'PSMULTEQ:FLAT': {
        'event': 'MainZone.OtherSettings.MultiEQ.Flat',
        'description': 'Main Zone Other Settings Multi EQ Flat'
    },
    'PSMULTEQ:OFF': {
        'event': 'MainZone.OtherSettings.MultiEQ.Off',
        'description': 'Main Zone Other Settings Multi EQ Off'
    },
    'PSNEURAL OFF': {
        'event': 'MainZone.OtherSettings.Neutral:X.Off',
        'description': 'Main Zone Other Settings Neutral:X Off'
    },
    'PSNEURAL ON': {
        'event': 'MainZone.OtherSettings.Neutral:X.On',
        'description': 'Main Zone Other Settings Neutral:X On'
    },
    'PSPSLOM OFF': {
        'event': 'MainZone.OtherSettings.LoudnessManagement.Off',
        'description': 'Main Zone Other Settings Loudness Management Off'
    },
    'PSPSLOM ON': {
        'event': 'MainZone.OtherSettings.LoudnessManagement.On',
        'description': 'Main Zone Other Settings Loudness Management On'
    },
    'PSREFLEV 0': {
        'event': 'MainZone.OtherSettings.ReferenceLevelOffset.0dB',
        'description': 'Main Zone Other Settings Reference Level Offset 0dB'
    },
    'PSREFLEV 10': {
        'event': 'MainZone.OtherSettings.ReferenceLevelOffset.10dB',
        'description': 'Main Zone Other Settings Reference Level Offset 10dB'
    },
    'PSREFLEV 15': {
        'event': 'MainZone.OtherSettings.ReferenceLevelOffset.15dB',
        'description': 'Main Zone Other Settings Reference Level Offset 15dB'
    },
    'PSREFLEV 5': {
        'event': 'MainZone.OtherSettings.ReferenceLevelOffset.5dB',
        'description': 'Main Zone Other Settings Reference Level Offset 5dB'
    },
    'PSRSTR HI': {
        'event': 'MainZone.OtherSettings.AudioRestorer.High',
        'description': 'Main Zone Other Settings Audio Restorer High'
    },
    'PSRSTR LOW': {
        'event': 'MainZone.OtherSettings.AudioRestorer.Low',
        'description': 'Main Zone Other Settings Audio Restorer Low'
    },
    'PSRSTR MED': {
        'event': 'MainZone.OtherSettings.AudioRestorer.Medium',
        'description': 'Main Zone Other Settings Audio Restorer Medium'
    },
    'PSRSTR OFF': {
        'event': 'MainZone.OtherSettings.AudioRestorer.Off',
        'description': 'Main Zone Other Settings Audio Restorer Off'
    },
    'PSRSZ L': {
        'event': 'MainZone.OtherSettings.RoomSize.Large',
        'description': 'Main Zone Other Settings Room Size Large'
    },
    'PSRSZ M': {
        'event': 'MainZone.OtherSettings.RoomSize.Medium',
        'description': 'Main Zone Other Settings Room Size Medium'
    },
    'PSRSZ ML': {
        'event': 'MainZone.OtherSettings.RoomSize.MediumLarge',
        'description': 'Main Zone Other Settings Room Size Medium Large'
    },
    'PSRSZ MS': {
        'event': 'MainZone.OtherSettings.RoomSize.MediumSmall',
        'description': 'Main Zone Other Settings Room Size Medium Small'
    },
    'PSRSZ S': {
        'event': 'MainZone.OtherSettings.RoomSize.Small',
        'description': 'Main Zone Other Settings Room Size Small'
    },
    'PSSP:FL': {
        'event': 'MainZone.OtherSettings.SP.Floor',
        'description': 'Main Zone Other Settings SP Floor'
    },
    'PSSP:FR': {
        'event': 'MainZone.OtherSettings.SP.Front',
        'description': 'Main Zone Other Settings SP Front'
    },
    'PSSP:HF': {
        'event': 'MainZone.OtherSettings.SP.Height&Floor',
        'description': 'Main Zone Other Settings SP Height & Floor'
    },
    'PSSTH **': {
        'event': 'MainZone.OtherSettings.StageHeight.**',
        'description': 'Main Zone Other Settings Stage Height Input'
    },
    'PSSTH DOWN': {
        'event': 'MainZone.OtherSettings.StageHeight.Down',
        'description': 'Main Zone Other Settings Stage Height Down'
    },
    'PSSTH UP': {
        'event': 'MainZone.OtherSettings.StageHeight.Up',
        'description': 'Main Zone Other Settings Stage Height Up'
    },
    'PSSTW **': {
        'event': 'MainZone.OtherSettings.StageWidth.**',
        'description': 'Main Zone Other Settings Stage Width Input'
    },
    'PSSTW DOWN': {
        'event': 'MainZone.OtherSettings.StageWidth.Down',
        'description': 'Main Zone Other Settings Stage Width Down'
    },
    'PSSTW UP': {
        'event': 'MainZone.OtherSettings.StageWidth.Up',
        'description': 'Main Zone Other Settings Stage Width Up'
    },
    'PSSWL **': {
        'event': 'MainZone.OtherSettings.SubwooferLevel.**',
        'description': 'Main Zone Other Settings Subwoofer Level Input'
    },
    'PSSWL DOWN': {
        'event': 'MainZone.OtherSettings.SubwooferLevel.Down',
        'description': 'Main Zone Other Settings Subwoofer Level Down'
    },
    'PSSWL OFF': {
        'event': 'MainZone.OtherSettings.SubwooferLevel.Off',
        'description': 'Main Zone Other Settings Subwoofer Level Off'
    },
    'PSSWL ON': {
        'event': 'MainZone.OtherSettings.SubwooferLevel.On',
        'description': 'Main Zone Other Settings Subwoofer Level On'
    },
    'PSSWL UP': {
        'event': 'MainZone.OtherSettings.SubwooferLevel.Up',
        'description': 'Main Zone Other Settings Subwoofer Level Up'
    },
    'PSSWL2 **': {
        'event': 'MainZone.OtherSettings.Subwoofer2Level.**',
        'description': 'Main Zone Other Settings Subwoofer 2 Level Input'
    },
    'PSSWL2 DOWN': {
        'event': 'MainZone.OtherSettings.Subwoofer2Level.Down',
        'description': 'Main Zone Other Settings Subwoofer 2 Level Down'
    },
    'PSSWL2 UP': {
        'event': 'MainZone.OtherSettings.Subwoofer2Level.Up',
        'description': 'Main Zone Other Settings Subwoofer 2 Level Up'
    },
    'PSSWR OFF': {
        'event': 'MainZone.OtherSettings.Sobwoofer.Off',
        'description': 'Main Zone Other Settings Sobwoofer Off'
    },
    'PSSWR ON': {
        'event': 'MainZone.OtherSettings.Sobwoofer.On',
        'description': 'Main Zone Other Settings Sobwoofer On'
    },
    'PSTONE CTRL OFF': {
        'event': 'MainZone.OtherSettings.Tone.Off',
        'description': 'Main Zone Other Settings Tone Off'
    },
    'PSTONE CTRL ON': {
        'event': 'MainZone.OtherSettings.Tone.On',
        'description': 'Main Zone Other Settings Tone On'
    },
    'PSTRE **': {
        'event': 'MainZone.OtherSettings.Treble.**',
        'description': 'Main Zone Other Settings Treble Input'
    },
    'PSTRE DOWN': {
        'event': 'MainZone.OtherSettings.Treble.Down',
        'description': 'Main Zone Other Settings Treble Down'
    },
    'PSTRE UP': {
        'event': 'MainZone.OtherSettings.Treble.Up',
        'description': 'Main Zone Other Settings Treble Up'
    },
    'PVBR ***': {
        'event': 'MainZone.PictureSettings.Brightness.***',
        'description': 'Main Zone Picture Settings Brightness Input'
    },
    'PVBR DOWN': {
        'event': 'MainZone.PictureSettings.Brightness.Down',
        'description': 'Main Zone Picture Settings Brightness Down'
    },
    'PVBR UP': {
        'event': 'MainZone.PictureSettings.Brightness.Up',
        'description': 'Main Zone Picture Settings Brightness Up'
    },
    'PVCN ***': {
        'event': 'MainZone.PictureSettings.Contrast.***',
        'description': 'Main Zone Picture Settings Contrast Input'
    },
    'PVCN DOWN': {
        'event': 'MainZone.PictureSettings.Contrast.Down',
        'description': 'Main Zone Picture Settings Contrast Down'
    },
    'PVCN UP': {
        'event': 'MainZone.PictureSettings.Contrast.Up',
        'description': 'Main Zone Picture Settings Contrast Up'
    },
    'PVCTM': {
        'event': 'MainZone.PictureSettings.Mode.Cinema',
        'description': 'Main Zone Picture Settings Mode Cinema'
    },
    'PVDAY': {
        'event': 'MainZone.PictureSettings.Mode.Day',
        'description': 'Main Zone Picture Settings Mode Day'
    },
    'PVDNR HI': {
        'event': 'MainZone.PictureSettings.DynamicNoiseReduction.High',
        'description': 'Main Zone Picture Settings Dynamic Noise Reduction High'
    },
    'PVDNR LOW': {
        'event': 'MainZone.PictureSettings.DynamicNoiseReduction.Low',
        'description': 'Main Zone Picture Settings Dynamic Noise Reduction Low'
    },
    'PVDNR MID': {
        'event': 'MainZone.PictureSettings.DynamicNoiseReduction.Middle',
        'description': 'Main Zone Picture Settings Dynamic Noise Reduction Middle'
    },
    'PVDNR OFF': {
        'event': 'MainZone.PictureSettings.DynamicNoiseReduction.Off',
        'description': 'Main Zone Picture Settings Dynamic Noise Reduction Off'
    },
    'PVENH ***': {
        'event': 'MainZone.PictureSettings.Enhancer.***',
        'description': 'Main Zone Picture Settings Enhancer Input'
    },
    'PVENH DOWN': {
        'event': 'MainZone.PictureSettings.Enhancer.Down',
        'description': 'Main Zone Picture Settings Enhancer Down'
    },
    'PVENH UP': {
        'event': 'MainZone.PictureSettings.Enhancer.Up',
        'description': 'Main Zone Picture Settings Enhancer Up'
    },
    'PVMOV': {
        'event': 'MainZone.PictureSettings.Mode.Movie',
        'description': 'Main Zone Picture Settings Mode Movie'
    },
    'PVNGT': {
        'event': 'MainZone.PictureSettings.Mode.Night',
        'description': 'Main Zone Picture Settings Mode Night'
    },
    'PVOFF': {
        'event': 'MainZone.PictureSettings.Mode.Off',
        'description': 'Main Zone Picture Settings Mode Off'
    },
    'PVST ***': {
        'event': 'MainZone.PictureSettings.ChromaLevel.***',
        'description': 'Main Zone Picture Settings Chroma Level Input'
    },
    'PVST DOWN': {
        'event': 'MainZone.PictureSettings.ChromaLevel.Down',
        'description': 'Main Zone Picture Settings Chroma Level Down'
    },
    'PVST UP': {
        'event': 'MainZone.PictureSettings.ChromaLevel.Up',
        'description': 'Main Zone Picture Settings Chroma Level Up'
    },
    'PVSTD': {
        'event': 'MainZone.PictureSettings.Mode.Standard',
        'description': 'Main Zone Picture Settings Mode Standard'
    },
    'PVSTM': {
        'event': 'MainZone.PictureSettings.Mode.Stream',
        'description': 'Main Zone Picture Settings Mode Stream'
    },
    'PVVVD': {
        'event': 'MainZone.PictureSettings.Mode.Vivid',
        'description': 'Main Zone Picture Settings Mode Vivid'
    },
    'PWON': {
        'event': 'Master.Power.On',
        'description': 'Master Power On'
    },
    'PWSTANDBY': {
        'event': 'Master.Power.Standby',
        'description': 'Master Power Standby'
    },
    'RNEND': {
        'event': 'System.RemoteMaintance.End',
        'description': 'System Remote Maintance End'
    },
    'RNSTA': {
        'event': 'System.RemoteMaintance.Start',
        'description': 'System Remote Maintance Start'
    },
    'SD7.1IN': {
        'event': 'MainZone.AudioInput.7.1In',
        'description': 'Main Zone Audio Input 7.1 In'
    },
    'SDANALOG': {
        'event': 'MainZone.AudioInput.Analog',
        'description': 'Main Zone Audio Input Analog'
    },
    'SDAUTO': {
        'event': 'MainZone.AudioInput.Auto',
        'description': 'Main Zone Audio Input Auto'
    },
    'SDDIGITAL': {
        'event': 'MainZone.AudioInput.Optical/Coaxial',
        'description': 'Main Zone Audio Input Optical/Coaxial'
    },
    'SDHDMI': {
        'event': 'MainZone.AudioInput.AudioHDMI',
        'description': 'Main Zone Audio Input Audio HDMI'
    },
    'SDNO': {
        'event': 'MainZone.AudioInput.No',
        'description': 'Main Zone Audio Input No'
    },
    'SIAUX1': {
        'event': 'MainZone.SourceInput.Aux1',
        'description': 'Main Zone Source Input Aux 1'
    },
    'SIAUX2': {
        'event': 'MainZone.SourceInput.Aux2',
        'description': 'Main Zone Source Input Aux 2'
    },
    'SIAUX3': {
        'event': 'MainZone.SourceInput.Aux3',
        'description': 'Main Zone Source Input Aux 3'
    },
    'SIAUX4': {
        'event': 'MainZone.SourceInput.Aux4',
        'description': 'Main Zone Source Input Aux 4'
    },
    'SIAUX5': {
        'event': 'MainZone.SourceInput.Aux5',
        'description': 'Main Zone Source Input Aux 5'
    },
    'SIAUX6': {
        'event': 'MainZone.SourceInput.Aux6',
        'description': 'Main Zone Source Input Aux 6'
    },
    'SIAUX7': {
        'event': 'MainZone.SourceInput.Aux7',
        'description': 'Main Zone Source Input Aux 7'
    },
    'SIBD': {
        'event': 'MainZone.SourceInput.BluRay',
        'description': 'Main Zone Source Input BluRay'
    },
    'SIBT': {
        'event': 'MainZone.SourceInput.BlueTeeth',
        'description': 'Main Zone Source Input Blue Teeth'
    },
    'SICD': {
        'event': 'MainZone.SourceInput.CD',
        'description': 'Main Zone Source Input CD'
    },
    'SIDVD': {
        'event': 'MainZone.SourceInput.DVD',
        'description': 'Main Zone Source Input DVD'
    },
    'SIFAVORITES': {
        'event': 'MainZone.SourceInput.Favorites',
        'description': 'Main Zone Source Input Favorites'
    },
    'SIFVP': {
        'event': 'MainZone.SourceInput.InternetRadio+PlaybackFavorites',
        'description': 'Main Zone Source Input Internet Radio + Playback Favorites'
    },
    'SIGAME': {
        'event': 'MainZone.SourceInput.Game',
        'description': 'Main Zone Source Input Game'
    },
    'SIHDRADIO': {
        'event': 'MainZone.SourceInput.HDRadio',
        'description': 'Main Zone Source Input HD Radio'
    },
    'SIIPD': {
        'event': 'MainZone.SourceInput.IPOD+Playback',
        'description': 'Main Zone Source Input IPOD + Playback'
    },
    'SIIRADIO': {
        'event': 'MainZone.SourceInput.InternetRadio',
        'description': 'Main Zone Source Input Internet Radio'
    },
    'SIIRP': {
        'event': 'MainZone.SourceInput.InternetRadio+PlaybackRecent',
        'description': 'Main Zone Source Input Internet Radio + Playback Recent'
    },
    'SIMPLAY': {
        'event': 'MainZone.SourceInput.MediaPlayer',
        'description': 'Main Zone Source Input Media Player'
    },
    'SINET': {
        'event': 'MainZone.SourceInput.Net',
        'description': 'Main Zone Source Input Net'
    },
    'SIPANDORA': {
        'event': 'MainZone.SourceInput.Pandora',
        'description': 'Main Zone Source Input Pandora'
    },
    'SIPHONO': {
        'event': 'MainZone.SourceInput.Phono',
        'description': 'Main Zone Source Input Phono'
    },
    'SISAT/CBL': {
        'event': 'MainZone.SourceInput.Sat/Cable',
        'description': 'Main Zone Source Input Sat/Cable'
    },
    'SISERVER': {
        'event': 'MainZone.SourceInput.Server',
        'description': 'Main Zone Source Input Server'
    },
    'SISIRIUSXM': {
        'event': 'MainZone.SourceInput.Sirius/XM',
        'description': 'Main Zone Source Input Sirius/XM'
    },
    'SITUNER': {
        'event': 'MainZone.SourceInput.Tuner',
        'description': 'Main Zone Source Input Tuner'
    },
    'SITV': {
        'event': 'MainZone.SourceInput.TV',
        'description': 'Main Zone Source Input TV'
    },
    'SIUSB': {
        'event': 'MainZone.SourceInput.USB+Playback',
        'description': 'Main Zone Source Input USB + Playback'
    },
    'SIUSB/IPOD': {
        'event': 'MainZone.SourceInput.USB/IPOD',
        'description': 'Main Zone Source Input USB/IPOD'
    },
    'SLP***': {
        'event': 'MainZone.SleepTimer.***',
        'description': 'Main Zone Sleep Timer Input'
    },
    'SLPOFF': {
        'event': 'MainZone.SleepTimer.Off',
        'description': 'Main Zone Sleep Timer Off'
    },
    'STBY15M': {
        'event': 'MainZone.AutoStandby.15Minutes',
        'description': 'Main Zone Auto Standby 15 Minutes'
    },
    'STBY30M': {
        'event': 'MainZone.AutoStandby.30Minutes',
        'description': 'Main Zone Auto Standby 30 Minutes'
    },
    'STBY60M': {
        'event': 'MainZone.AutoStandby.60Minutes',
        'description': 'Main Zone Auto Standby 60 Minutes'
    },
    'STBYOFF': {
        'event': 'MainZone.AutoStandby.Off',
        'description': 'Main Zone Auto Standby Off'
    },
    'SVAUX1': {
        'event': 'MainZone.VideoSelect.Aux1',
        'description': 'Main Zone Video Select Aux 1'
    },
    'SVAUX2': {
        'event': 'MainZone.VideoSelect.Aux2',
        'description': 'Main Zone Video Select Aux 2'
    },
    'SVAUX3': {
        'event': 'MainZone.VideoSelect.Aux3',
        'description': 'Main Zone Video Select Aux 3'
    },
    'SVAUX4': {
        'event': 'MainZone.VideoSelect.Aux4',
        'description': 'Main Zone Video Select Aux 4'
    },
    'SVAUX5': {
        'event': 'MainZone.VideoSelect.Aux5',
        'description': 'Main Zone Video Select Aux 5'
    },
    'SVAUX6': {
        'event': 'MainZone.VideoSelect.Aux6',
        'description': 'Main Zone Video Select Aux 6'
    },
    'SVAUX7': {
        'event': 'MainZone.VideoSelect.Aux7',
        'description': 'Main Zone Video Select Aux 7'
    },
    'SVBD': {
        'event': 'MainZone.VideoSelect.BluRay',
        'description': 'Main Zone Video Select BluRay'
    },
    'SVCD': {
        'event': 'MainZone.VideoSelect.CD',
        'description': 'Main Zone Video Select CD'
    },
    'SVDVD': {
        'event': 'MainZone.VideoSelect.DVD',
        'description': 'Main Zone Video Select DVD'
    },
    'SVGAME': {
        'event': 'MainZone.VideoSelect.Game',
        'description': 'Main Zone Video Select Game'
    },
    'SVMPLAY': {
        'event': 'MainZone.VideoSelect.MediaPlayer',
        'description': 'Main Zone Video Select Media Player'
    },
    'SVOFF': {
        'event': 'MainZone.VideoSelect.Off',
        'description': 'Main Zone Video Select Off'
    },
    'SVON': {
        'event': 'MainZone.VideoSelect.On',
        'description': 'Main Zone Video Select On'
    },
    'SVSAT/CBL': {
        'event': 'MainZone.VideoSelect.Sat/Cable',
        'description': 'Main Zone Video Select Sat/Cable'
    },
    'SVTV': {
        'event': 'MainZone.VideoSelect.TV',
        'description': 'Main Zone Video Select TV'
    },
    'SYPANEL LOCK OFF': {
        'event': 'System.Locks.PanelButtons.Off',
        'description': 'System Locks Panel Buttons Off'
    },
    'SYPANEL LOCK ON': {
        'event': 'System.Locks.PanelButtons.EverythingButMasterVolume',
        'description': 'System Locks Panel Buttons Everything But Master Volume'
    },
    'SYPANEL+V LOCK ON': {
        'event': 'System.Locks.PanelButtons.On',
        'description': 'System Locks Panel Buttons On'
    },
    'SYREMOTE LOCK OFF': {
        'event': 'System.Locks.Remote.Off',
        'description': 'System Locks Remote Off'
    },
    'SYREMOTE LOCK ON': {
        'event': 'System.Locks.Remote.On',
        'description': 'System Locks Remote On'
    },
    'TFAN******': {
        'event': 'Tuner.Frequancy.******',
        'description': 'Tuner Frequancy Input'
    },
    'TFANDOWN': {
        'event': 'Tuner.Frequancy.Down',
        'description': 'Tuner Frequancy Down'
    },
    'TFANUP': {
        'event': 'Tuner.Frequancy.Up',
        'description': 'Tuner Frequancy Up'
    },
    'TFHD******': {
        'event': 'HDRadio.Frequancy.******',
        'description': 'HD Radio Frequancy Input'
    },
    'TFHD******MC*': {
        'event': 'HDRadio.Frequancy.MultiCast.FrequancyInput.*******',
        'description': 'HD Radio Frequancy Multi Cast Frequancy Input'
    },
    'TFHDDOWN': {
        'event': 'HDRadio.Frequancy.Down',
        'description': 'HD Radio Frequancy Down'
    },
    'TFHDMC*': {
        'event': 'HDRadio.Frequancy.MultiCast.*',
        'description': 'HD Radio Frequancy Multi Cast Input'
    },
    'TFHDUP': {
        'event': 'HDRadio.Frequancy.Up',
        'description': 'HD Radio Frequancy Up'
    },
    'TMANAM': {
        'event': 'Tuner.Band.AM',
        'description': 'Tuner Band AM'
    },
    'TMANAUTO': {
        'event': 'Tuner.Band.ScanMode.Auto',
        'description': 'Tuner Band Scan Mode Auto'
    },
    'TMANFM': {
        'event': 'Tuner.Band.FM',
        'description': 'Tuner Band FM'
    },
    'TMANMANUAL': {
        'event': 'Tuner.Band.ScanMode.Manual',
        'description': 'Tuner Band Scan Mode Manual'
    },
    'TMHDAM': {
        'event': 'HDRadio.Band.AM',
        'description': 'HD Radio Band AM'
    },
    'TMHDANAAUTO': {
        'event': 'HDRadio.Band.ScanMode.AnalogAuto',
        'description': 'HD Radio Band Scan Mode Analog Auto'
    },
    'TMHDANAMANU': {
        'event': 'HDRadio.Band.ScanMode.AnalogManual',
        'description': 'HD Radio Band Scan Mode Analog Manual'
    },
    'TMHDAUTO': {
        'event': 'HDRadio.Band.ScanMode.DigitalAuto',
        'description': 'HD Radio Band Scan Mode Digital Auto'
    },
    'TMHDAUTOHD': {
        'event': 'HDRadio.Band.ScanMode.HDAuto',
        'description': 'HD Radio Band Scan Mode HD Auto'
    },
    'TMHDFM': {
        'event': 'HDRadio.Band.FM',
        'description': 'HD Radio Band FM'
    },
    'TMHDMANUAL': {
        'event': 'HDRadio.Band.ScanMode.DigitalManual',
        'description': 'HD Radio Band Scan Mode Digital Manual'
    },
    'TPAN**': {
        'event': 'Tuner.Preset.**',
        'description': 'Tuner Preset Input'
    },
    'TPANDOWN': {
        'event': 'Tuner.Preset.Down',
        'description': 'Tuner Preset Down'
    },
    'TPANMEM': {
        'event': 'Tuner.Preset.Memory.Down',
        'description': 'Tuner Preset Memory Down'
    },
    'TPANMEM**': {
        'event': 'Tuner.Preset.Memory.**',
        'description': 'Tuner Preset Memory Input'
    },
    'TPANUP': {
        'event': 'Tuner.Preset.Up',
        'description': 'Tuner Preset Up'
    },
    'TPHD**': {
        'event': 'HDRadio.Preset.**',
        'description': 'HD Radio Preset Input'
    },
    'TPHDDOWN': {
        'event': 'HDRadio.Preset.Down',
        'description': 'HD Radio Preset Down'
    },
    'TPHDMEM': {
        'event': 'HDRadio.Preset.Memory.Down',
        'description': 'HD Radio Preset Memory Down'
    },
    'TPHDMEM**': {
        'event': 'HDRadio.Preset.Memory.**',
        'description': 'HD Radio Preset Memory Input'
    },
    'TPHDUP': {
        'event': 'HDRadio.Preset.Up',
        'description': 'HD Radio Preset Up'
    },
    'TR1 OFF': {
        'event': 'System.Trigger.1.Off',
        'description': 'System Trigger 1 Off'
    },
    'TR1 ON': {
        'event': 'System.Trigger.1.On',
        'description': 'System Trigger 1 On'
    },
    'TR2 OFF': {
        'event': 'System.Trigger.2.Off',
        'description': 'System Trigger 2 Off'
    },
    'TR2 ON': {
        'event': 'System.Trigger.2.On',
        'description': 'System Trigger 2 On'
    },
    'UGIDN': {
        'event': 'System.UpgradeId.DisplayNumber',
        'description': 'System Upgrade Id Display Number'
    },
    'VSASPFUL': {
        'event': 'MainZone.VideoSettings.AspectRatio.16:9',
        'description': 'Main Zone Video Settings Aspect Ratio 16:9'
    },
    'VSASPNRM': {
        'event': 'MainZone.VideoSettings.AspectRatio.4:3',
        'description': 'Main Zone Video Settings Aspect Ratio 4:3'
    },
    'VSAUDIO AMP': {
        'event': 'MainZone.VideoSettings.HDMIAudioOutput.Amp',
        'description': 'Main Zone Video Settings HDMI Audio Output Amp'
    },
    'VSAUDIO TV': {
        'event': 'MainZone.VideoSettings.HDMIAudioOutput.TV',
        'description': 'Main Zone Video Settings HDMI Audio Output TV'
    },
    'VSMONI1': {
        'event': 'MainZone.VideoSettings.HDMIMonitor.Out1',
        'description': 'Main Zone Video Settings HDMI Monitor Out 1'
    },
    'VSMONI2': {
        'event': 'MainZone.VideoSettings.HDMIMonitor.Out2',
        'description': 'Main Zone Video Settings HDMI Monitor Out 2'
    },
    'VSMONIAUTO': {
        'event': 'MainZone.VideoSettings.HDMIMonitor.Auto',
        'description': 'Main Zone Video Settings HDMI Monitor Auto'
    },
    'VSSC10I': {
        'event': 'MainZone.VideoSettings.Resolution.1080i',
        'description': 'Main Zone Video Settings Resolution 1080i'
    },
    'VSSC10P': {
        'event': 'MainZone.VideoSettings.Resolution.1080p',
        'description': 'Main Zone Video Settings Resolution 1080p'
    },
    'VSSC10P24': {
        'event': 'MainZone.VideoSettings.Resolution.1080p:24Hz',
        'description': 'Main Zone Video Settings Resolution 1080p:24Hz'
    },
    'VSSC48P': {
        'event': 'MainZone.VideoSettings.Resolution.480p/576p',
        'description': 'Main Zone Video Settings Resolution 480p/576p'
    },
    'VSSC4K': {
        'event': 'MainZone.VideoSettings.Resolution.4K',
        'description': 'Main Zone Video Settings Resolution 4K'
    },
    'VSSC4KF': {
        'event': 'MainZone.VideoSettings.Resolution.4K(60/50)',
        'description': 'Main Zone Video Settings Resolution 4K(60/50) '
    },
    'VSSC72P': {
        'event': 'MainZone.VideoSettings.Resolution.720p',
        'description': 'Main Zone Video Settings Resolution 720p'
    },
    'VSSCAUTO': {
        'event': 'MainZone.VideoSettings.Resolution.Auto',
        'description': 'Main Zone Video Settings Resolution Auto'
    },
    'VSSCH10I': {
        'event': 'MainZone.VideoSettings.HDMIResolution.1080i',
        'description': 'Main Zone Video Settings HDMI Resolution 1080i'
    },
    'VSSCH10P': {
        'event': 'MainZone.VideoSettings.HDMIResolution.1080p',
        'description': 'Main Zone Video Settings HDMI Resolution 1080p'
    },
    'VSSCH10P24': {
        'event': 'MainZone.VideoSettings.HDMIResolution.1080p:24Hz',
        'description': 'Main Zone Video Settings HDMI Resolution 1080p:24Hz'
    },
    'VSSCH48P': {
        'event': 'MainZone.VideoSettings.HDMIResolution.480p/576p',
        'description': 'Main Zone Video Settings HDMI Resolution 480p/576p'
    },
    'VSSCH4K': {
        'event': 'MainZone.VideoSettings.HDMIResolution.4K',
        'description': 'Main Zone Video Settings HDMI Resolution 4K'
    },
    'VSSCH4KF': {
        'event': 'MainZone.VideoSettings.HDMIResolution.4K(60/50)',
        'description': 'Main Zone Video Settings HDMI Resolution 4K(60/50) '
    },
    'VSSCH72P': {
        'event': 'MainZone.VideoSettings.HDMIResolution.720p',
        'description': 'Main Zone Video Settings HDMI Resolution 720p'
    },
    'VSSCHAUTO': {
        'event': 'MainZone.VideoSettings.HDMIResolution.Auto',
        'description': 'Main Zone Video Settings HDMI Resolution Auto'
    },
    'VSVPMAUTO': {
        'event': 'MainZone.VideoSettings.VideoProcessing.Auto',
        'description': 'Main Zone Video Settings Video Processing Auto'
    },
    'VSVPMBYP': {
        'event': 'MainZone.VideoSettings.VideoProcessing.Bypass',
        'description': 'Main Zone Video Settings Video Processing Bypass'
    },
    'VSVPMGAME': {
        'event': 'MainZone.VideoSettings.VideoProcessing.Game',
        'description': 'Main Zone Video Settings Video Processing Game'
    },
    'VSVPMMOVI': {
        'event': 'MainZone.VideoSettings.VideoProcessing.Movie',
        'description': 'Main Zone Video Settings Video Processing Movie'
    },
    'VSVST OFF': {
        'event': 'MainZone.VideoSettings.VerticalStretch.Off',
        'description': 'Main Zone Video Settings Vertical Stretch Off'
    },
    'VSVST ON': {
        'event': 'MainZone.VideoSettings.VerticalStretch.On',
        'description': 'Main Zone Video Settings Vertical Stretch On'
    },
    'Z2**': {
        'event'      : 'Zone2.Volume.**',
        'description': 'Zone 2 Volume Direct'
    },
    'Z2***': {
        'event': 'Zone2.Volume.***',
        'description': 'Zone 2 Volume Direct'
    },
    'Z2AUX1': {
        'event': 'Zone2.SourceInput.Aux1',
        'description': 'Zone 2 Source Input Aux 1'
    },
    'Z2AUX2': {
        'event': 'Zone2.SourceInput.Aux2',
        'description': 'Zone 2 Source Input Aux 2'
    },
    'Z2AUX3': {
        'event': 'Zone2.SourceInput.Aux3',
        'description': 'Zone 2 Source Input Aux 3'
    },
    'Z2AUX4': {
        'event': 'Zone2.SourceInput.Aux4',
        'description': 'Zone 2 Source Input Aux 4'
    },
    'Z2AUX5': {
        'event': 'Zone2.SourceInput.Aux5',
        'description': 'Zone 2 Source Input Aux 5'
    },
    'Z2AUX6': {
        'event': 'Zone2.SourceInput.Aux6',
        'description': 'Zone 2 Source Input Aux 6'
    },
    'Z2AUX7': {
        'event': 'Zone2.SourceInput.Aux7',
        'description': 'Zone 2 Source Input Aux 7'
    },
    'Z2BD': {
        'event': 'Zone2.SourceInput.BluRay',
        'description': 'Zone 2 Source Input BluRay'
    },
    'Z2BT': {
        'event': 'Zone2.SourceInput.BlueTeeth',
        'description': 'Zone 2 Source Input Blue Teeth'
    },
    'Z2CD': {
        'event': 'Zone2.SourceInput.CD',
        'description': 'Zone 2 Source Input CD'
    },
    'Z2CSMONO': {
        'event': 'Zone2.SoundMode.Mono',
        'description': 'Zone 2 Sound Mode Mono'
    },
    'Z2CSST': {
        'event': 'Zone2.SoundMode.Stereo',
        'description': 'Zone 2 Sound Mode Stereo'
    },
    'Z2CVFL **': {
        'event': 'Zone2.ChannelVolume.FrontLeft.**',
        'description': 'Zone 2 Channel Volume Front Left Input'
    },
    'Z2CVFL DOWN': {
        'event': 'Zone2.ChannelVolume.FrontLeft.Down',
        'description': 'Zone 2 Channel Volume Front Left Down'
    },
    'Z2CVFL UP': {
        'event': 'Zone2.ChannelVolume.FrontLeft.Up',
        'description': 'Zone 2 Channel Volume Front Left Up'
    },
    'Z2CVFR **': {
        'event': 'Zone2.ChannelVolume.FrontRight.**',
        'description': 'Zone 2 Channel Volume Front Right Input'
    },
    'Z2CVFR DOWN': {
        'event': 'Zone2.ChannelVolume.FrontRight.Down',
        'description': 'Zone 2 Channel Volume Front Right Down'
    },
    'Z2CVFR UP': {
        'event': 'Zone2.ChannelVolume.FrontRight.Up',
        'description': 'Zone 2 Channel Volume Front Right Up'
    },
    'Z2DOWN': {
        'event': 'Zone2.Volume.Down',
        'description': 'Zone 2 Volume Down'
    },
    'Z2DVD': {
        'event': 'Zone2.SourceInput.DVD',
        'description': 'Zone 2 Source Input DVD'
    },
    'Z2FAVORITES': {
        'event': 'Zone2.SourceInput.Favorites',
        'description': 'Zone 2 Source Input Favorites'
    },
    'Z2FVP': {
        'event': 'Zone2.SourceInput.InternetRadio+FavoritesPlayback',
        'description': 'Zone 2 Source Input Internet Radio + Favorites Playback'
    },
    'Z2GAME': {
        'event': 'Zone2.SourceInput.Game',
        'description': 'Zone 2 Source Input Game'
    },
    'Z2HADPCM': {
        'event': 'Zone2.HDMIAudioMode.PCM',
        'description': 'Zone 2 HDMI Audio Mode PCM'
    },
    'Z2HADTHR': {
        'event': 'Zone2.HDMIAudioMode.PassThru',
        'description': 'Zone 2 HDMI Audio Mode Pass Thru'
    },
    'Z2HDRADIO': {
        'event': 'Zone2.SourceInput.HDRadio',
        'description': 'Zone 2 Source Input HD Radio'
    },
    'Z2HPFOFF': {
        'event': 'Zone2.HighPassFilter.Off',
        'description': 'Zone 2 High Pass Filter Off'
    },
    'Z2HPFON': {
        'event': 'Zone2.HighPassFilter.On',
        'description': 'Zone 2 High Pass Filter On'
    },
    'Z2IPD': {
        'event': 'Zone2.SourceInput.IPOD+Playback',
        'description': 'Zone 2 Source Input IPOD + Playback'
    },
    'Z2IRADIO': {
        'event': 'Zone2.SourceInput.InternetRadio',
        'description': 'Zone 2 Source Input Internet Radio'
    },
    'Z2IRP': {
        'event': 'Zone2.SourceInput.InternetRadio+RecentPlayback',
        'description': 'Zone 2 Source Input Internet Radio + Recent Playback'
    },
    'Z2MPLAY': {
        'event': 'Zone2.SourceInput.MediaPlayer',
        'description': 'Zone 2 Source Input Media Player'
    },
    'Z2MUOFF': {
        'event': 'Zone2.Mute.Off',
        'description': 'Zone 2 Mute Off'
    },
    'Z2MUON': {
        'event': 'Zone2.Mute.On',
        'description': 'Zone 2 Mute On'
    },
    'Z2NET': {
        'event': 'Zone2.SourceInput.Net',
        'description': 'Zone 2 Source Input Net'
    },
    'Z2OFF': {
        'event': 'Zone2.Power.Off',
        'description': 'Zone 2 Power Off'
    },
    'Z2ON': {
        'event': 'Zone2.Power.On',
        'description': 'Zone 2 Power On'
    },
    'Z2PANDORA': {
        'event': 'Zone2.SourceInput.Pandora',
        'description': 'Zone 2 Source Input Pandora'
    },
    'Z2PHONO': {
        'event': 'Zone2.SourceInput.Phono',
        'description': 'Zone 2 Source Input Phono'
    },
    'Z2PSBAS **': {
        'event': 'Zone2.Tone.Bass.**',
        'description': 'Zone 2 Tone Bass Input'
    },
    'Z2PSBAS DOWN': {
        'event': 'Zone2.Tone.Bass.Down',
        'description': 'Zone 2 Tone Bass Down'
    },
    'Z2PSBAS UP': {
        'event': 'Zone2.Tone.Bass.Up',
        'description': 'Zone 2 Tone Bass Up'
    },
    'Z2PSTRE **': {
        'event': 'Zone2.Tone.Treble.**',
        'description': 'Zone 2 Tone Treble Input'
    },
    'Z2PSTRE DOWN': {
        'event': 'Zone2.Tone.Treble.Down',
        'description': 'Zone 2 Tone Treble Down'
    },
    'Z2PSTRE UP': {
        'event': 'Zone2.Tone.Treble.Up',
        'description': 'Zone 2 Tone Treble Up'
    },
    'Z2QUCIK4 MEMORY': {
        'event': 'Zone2.QuickMemorySelect.4',
        'description': 'Zone 2 Source Input Quick Memory Select 4'
    },
    'Z2QUICK1': {
        'event': 'Zone2.QuickSelect.1',
        'description': 'Zone 2 Source Input Quick Select 1'
    },
    'Z2QUICK2': {
        'event': 'Zone2.QuickSelect.2',
        'description': 'Zone 2 Source Input Quick Select 2'
    },
    'Z2QUICK2 MEMORY': {
        'event': 'Zone2.QuickMemorySelect.2',
        'description': 'Zone 2 Source Input Quick Memory Select 2'
    },
    'Z2QUICK3': {
        'event': 'Zone2.QuickSelect.3',
        'description': 'Zone 2 Source Input Quick Select 3'
    },
    'Z2QUICK3 MEMORY': {
        'event': 'Zone2.QuickMemorySelect.3',
        'description': 'Zone 2 Source Input Quick Memory Select 3'
    },
    'Z2QUICK4': {
        'event': 'Zone2.QuickSelect.4',
        'description': 'Zone 2 Source Input Quick Select 4'
    },
    'Z2QUICK5': {
        'event': 'Zone2.QuickSelect.5',
        'description': 'Zone 2 Source Input Quick Select 5'
    },
    'Z2QUICK5 MEMORY': {
        'event': 'Zone2.QuickMemorySelect.5',
        'description': 'Zone 2 Source Input Quick Memory Select 5'
    },
    'Z2SAT/CBL': {
        'event': 'Zone2.SourceInput.Sat/Cable',
        'description': 'Zone 2 Source Input Sat/Cable'
    },
    'Z2SERVER': {
        'event': 'Zone2.SourceInput.Server',
        'description': 'Zone 2 Source Input Server'
    },
    'Z2SIRIUSXM': {
        'event': 'Zone2.SourceInput.Sirius/XM',
        'description': 'Zone 2 Source Input Sirius/XM'
    },
    'Z2SLP***': {
        'event': 'Zone2.SleepTimer.***',
        'description': 'Zone 2 Sleep Timer Input'
    },
    'Z2SLPOFF': {
        'event': 'Zone2.SleepTimer.Off',
        'description': 'Zone 2 Sleep Timer Off'
    },
    'Z2SOURCE': {
        'event': 'Zone2.MainZone.SourceInput',
        'description': 'Zone 2 Source Input Main Zone'
    },
    'Z2STBY2H': {
        'event': 'Zone2.AutoStandby.2Hours',
        'description': 'Zone 2 Auto Standby 2 Hours'
    },
    'Z2STBY4H': {
        'event': 'Zone2.AutoStandby.4Hours',
        'description': 'Zone 2 Auto Standby 4 Hours'
    },
    'Z2STBY8H': {
        'event': 'Zone2.AutoStandby.8Hours',
        'description': 'Zone 2 Auto Standby 8 Hours'
    },
    'Z2STBYOFF': {
        'event': 'Zone2.AutoStandby.Off',
        'description': 'Zone 2 Auto Standby Off'
    },
    'Z2TUNER': {
        'event': 'Zone2.SourceInput.Tuner',
        'description': 'Zone 2 Source Input Tuner'
    },
    'Z2TV': {
        'event': 'Zone2.SourceInput.TV',
        'description': 'Zone 2 Source Input TV'
    },
    'Z2UP': {
        'event': 'Zone2.Volume.Up',
        'description': 'Zone 2 Volume Up'
    },
    'Z2USB': {
        'event': 'Zone2.SourceInput.USB+Playback',
        'description': 'Zone 2 Source Input USB + Playback'
    },
    'Z2USB/IPOD': {
        'event': 'Zone2.SourceInput.USB/IPOD',
        'description': 'Zone 2 Source Input USB/IPOD'
    },
    'Z3**': {
        'event'      : 'Zone3.Volume.**',
        'description': 'Zone 3 Volume Direct'
    },
    'Z3***': {
        'event': 'Zone3.Volume.***',
        'description': 'Zone 3 Volume Direct'
    },
    'Z3AUX1': {
        'event': 'Zone3.SourceInput.Aux1',
        'description': 'Zone 3 Source Input Aux 1'
    },
    'Z3AUX2': {
        'event': 'Zone3.SourceInput.Aux2',
        'description': 'Zone 3 Source Input Aux 2'
    },
    'Z3AUX3': {
        'event': 'Zone3.SourceInput.Aux3',
        'description': 'Zone 3 Source Input Aux 3'
    },
    'Z3AUX4': {
        'event': 'Zone3.SourceInput.Aux4',
        'description': 'Zone 3 Source Input Aux 4'
    },
    'Z3AUX5': {
        'event': 'Zone3.SourceInput.Aux5',
        'description': 'Zone 3 Source Input Aux 5'
    },
    'Z3AUX6': {
        'event': 'Zone3.SourceInput.Aux6',
        'description': 'Zone 3 Source Input Aux 6'
    },
    'Z3AUX7': {
        'event': 'Zone3.SourceInput.Aux7',
        'description': 'Zone 3 Source Input Aux 7'
    },
    'Z3BD': {
        'event': 'Zone3.SourceInput.BluRay',
        'description': 'Zone 3 Source Input BluRay'
    },
    'Z3BT': {
        'event': 'Zone3.SourceInput.BlueTeeth',
        'description': 'Zone 3 Source Input Blue Teeth'
    },
    'Z3CD': {
        'event': 'Zone3.SourceInput.CD',
        'description': 'Zone 3 Source Input CD'
    },
    'Z3CSMONO': {
        'event': 'Zone3.SoundMode.Mono',
        'description': 'Zone 3 Sound Mode Mono'
    },
    'Z3CSST': {
        'event': 'Zone3.SoundMode.Stereo',
        'description': 'Zone 3 Sound Mode Stereo'
    },
    'Z3CVFL **': {
        'event': 'Zone3.ChannelVolume.FrontLeft.**',
        'description': 'Zone 3 Channel Volume Front Left Input'
    },
    'Z3CVFL DOWN': {
        'event': 'Zone3.ChannelVolume.FrontLeft.Down',
        'description': 'Zone 3 Channel Volume Front Left Down'
    },
    'Z3CVFL UP': {
        'event': 'Zone3.ChannelVolume.FrontLeft.Up',
        'description': 'Zone 3 Channel Volume Front Left Up'
    },
    'Z3CVFR **': {
        'event': 'Zone3.ChannelVolume.FrontRight.**',
        'description': 'Zone 3 Channel Volume Front Right Input'
    },
    'Z3CVFR DOWN': {
        'event': 'Zone3.ChannelVolume.FrontRight.Down',
        'description': 'Zone 3 Channel Volume Front Right Down'
    },
    'Z3CVFR UP': {
        'event': 'Zone3.ChannelVolume.FrontRight.Up',
        'description': 'Zone 3 Channel Volume Front Right Up'
    },
    'Z3DOWN': {
        'event': 'Zone3.Volume.Down',
        'description': 'Zone 3 Volume Down'
    },
    'Z3DVD': {
        'event': 'Zone3.SourceInput.DVD',
        'description': 'Zone 3 Source Input DVD'
    },
    'Z3FAVORITES': {
        'event': 'Zone3.SourceInput.Favorites',
        'description': 'Zone 3 Source Input Favorites'
    },
    'Z3FVP': {
        'event': 'Zone3.SourceInput.InternetRadio+FavoritesPlayback',
        'description': 'Zone 3 Source Input Internet Radio + Favorites Playback'
    },
    'Z3GAME': {
        'event': 'Zone3.SourceInput.Game',
        'description': 'Zone 3 Source Input Game'
    },
    'Z3HDRADIO': {
        'event': 'Zone3.SourceInput.HDRadio',
        'description': 'Zone 3 Source Input HD Radio'
    },
    'Z3HPFOFF': {
        'event': 'Zone3.HighPassFilter.Off',
        'description': 'Zone 3 High Pass Filter Off'
    },
    'Z3HPFON': {
        'event': 'Zone3.HighPassFilter.On',
        'description': 'Zone 3 High Pass Filter On'
    },
    'Z3IPD': {
        'event': 'Zone3.SourceInput.IPOD+Playback',
        'description': 'Zone 3 Source Input IPOD + Playback'
    },
    'Z3IRADIO': {
        'event': 'Zone3.SourceInput.InternetRadio',
        'description': 'Zone 3 Source Input Internet Radio'
    },
    'Z3IRP': {
        'event': 'Zone3.SourceInput.InternetRadio+RecentPlayback',
        'description': 'Zone 3 Source Input Internet Radio + Recent Playback'
    },
    'Z3MPLAY': {
        'event': 'Zone3.SourceInput.MediaPlayer',
        'description': 'Zone 3 Source Input Media Player'
    },
    'Z3MUOFF': {
        'event': 'Zone3.Mute.Off',
        'description': 'Zone 3 Mute Off'
    },
    'Z3MUON': {
        'event': 'Zone3.Mute.On',
        'description': 'Zone 3 Mute On'
    },
    'Z3NET': {
        'event': 'Zone3.SourceInput.Net',
        'description': 'Zone 3 Source Input Net'
    },
    'Z3OFF': {
        'event': 'Zone3.Power.Off',
        'description': 'Zone 3 Power Off'
    },
    'Z3ON': {
        'event': 'Zone3.Power.On',
        'description': 'Zone 3 Power On'
    },
    'Z3PANDORA': {
        'event': 'Zone3.SourceInput.Pandora',
        'description': 'Zone 3 Source Input Pandora'
    },
    'Z3PHONO': {
        'event': 'Zone3.SourceInput.Phono',
        'description': 'Zone 3 Source Input Phono'
    },
    'Z3PSBAS **': {
        'event': 'Zone3.Tone.Bass.**',
        'description': 'Zone 3 Tone Bass Input'
    },
    'Z3PSBAS DOWN': {
        'event': 'Zone3.Tone.Bass.Down',
        'description': 'Zone 3 Tone Bass Down'
    },
    'Z3PSBAS UP': {
        'event': 'Zone3.Tone.Bass.Up',
        'description': 'Zone 3 Tone Bass Up'
    },
    'Z3PSTRE **': {
        'event': 'Zone3.Tone.Treble.**',
        'description': 'Zone 3 Tone Treble Input'
    },
    'Z3PSTRE DOWN': {
        'event': 'Zone3.Tone.Treble.Down',
        'description': 'Zone 3 Tone Treble Down'
    },
    'Z3PSTRE UP': {
        'event': 'Zone3.Tone.Treble.Up',
        'description': 'Zone 3 Tone Treble Up'
    },
    'Z3QUCIK4 MEMORY': {
        'event': 'Zone3.QuickMemorySelect.4',
        'description': 'Zone 3 Source Input Quick Memory Select 4'
    },
    'Z3QUICK1': {
        'event': 'Zone3.QuickSelect.1',
        'description': 'Zone 3 Source Input Quick Select 1'
    },
    'Z3QUICK2': {
        'event': 'Zone3.QuickSelect.2',
        'description': 'Zone 3 Source Input Quick Select 2'
    },
    'Z3QUICK2 MEMORY': {
        'event': 'Zone3.QuickMemorySelect.2',
        'description': 'Zone 3 Source Input Quick Memory Select 2'
    },
    'Z3QUICK3': {
        'event': 'Zone3.QuickSelect.3',
        'description': 'Zone 3 Source Input Quick Select 3'
    },
    'Z3QUICK3 MEMORY': {
        'event': 'Zone3.QuickMemorySelect.3',
        'description': 'Zone 3 Source Input Quick Memory Select 3'
    },
    'Z3QUICK4': {
        'event': 'Zone3.QuickSelect.4',
        'description': 'Zone 3 Source Input Quick Select 4'
    },
    'Z3QUICK5': {
        'event': 'Zone3.QuickSelect.5',
        'description': 'Zone 3 Source Input Quick Select 5'
    },
    'Z3QUICK5 MEMORY': {
        'event': 'Zone3.QuickMemorySelect.5',
        'description': 'Zone 3 Source Input Quick Memory Select 5'
    },
    'Z3SAT/CBL': {
        'event': 'Zone3.SourceInput.Sat/Cable',
        'description': 'Zone 3 Source Input Sat/Cable'
    },
    'Z3SERVER': {
        'event': 'Zone3.SourceInput.Server',
        'description': 'Zone 3 Source Input Server'
    },
    'Z3SIRIUSXM': {
        'event': 'Zone3.SourceInput.Sirius/XM',
        'description': 'Zone 3 Source Input Sirius/XM'
    },
    'Z3SLP***': {
        'event': 'Zone3.SleepTimer.***',
        'description': 'Zone 3 Sleep Timer Input'
    },
    'Z3SLPOFF': {
        'event': 'Zone3.SleepTimer.Off',
        'description': 'Zone 3 Sleep Timer Off'
    },
    'Z3SOURCE': {
        'event': 'Zone3.MainZone.SourceInput',
        'description': 'Zone 3 Source Input Main Zone'
    },
    'Z3STBY2H': {
        'event': 'Zone3.AutoStandby.2Hours',
        'description': 'Zone 3 Auto Standby 2 Hours'
    },
    'Z3STBY4H': {
        'event': 'Zone3.AutoStandby.4Hours',
        'description': 'Zone 3 Auto Standby 4 Hours'
    },
    'Z3STBY8H': {
        'event': 'Zone3.AutoStandby.8Hours',
        'description': 'Zone 3 Auto Standby 8 Hours'
    },
    'Z3STBYOFF': {
        'event': 'Zone3.AutoStandby.Off',
        'description': 'Zone 3 Auto Standby Off'
    },
    'Z3TUNER': {
        'event': 'Zone3.SourceInput.Tuner',
        'description': 'Zone 3 Source Input Tuner'
    },
    'Z3TV': {
        'event': 'Zone3.SourceInput.TV',
        'description': 'Zone 3 Source Input TV'
    },
    'Z3UP': {
        'event': 'Zone3.Volume.Up',
        'description': 'Zone 3 Volume Up'
    },
    'Z3USB': {
        'event': 'Zone3.SourceInput.USB+Playback',
        'description': 'Zone 3 Source Input USB + Playback'
    },
    'Z3USB/IPOD': {
        'event': 'Zone3.SourceInput.USB/IPOD',
        'description': 'Zone 3 Source Input USB/IPOD'
    },
    'ZMOFF': {
        'event': 'MainZone.Power.Off',
        'description': 'Main Zone Power Off'
    },
    'ZMON': {
        'event': 'MainZone.Power.On',
        'description': 'Main Zone Power On'
    }
}


def GetEventList():
    return sorted(
        list(
            [event['event'], event['description']]
            for event in EVENTS.values()
            if '*' not in event['event']
        )
    )


def GetEvent(response):

    if response in EVENTS:
        return EVENTS[response]['event'], None
    digitChange = re.sub('\d', '*', response)
    if digitChange in EVENTS:

        volumeItems = ['Main Zone Volume', 'Zone 2 Volume', 'Zone 3 Volume']
        while volumeItems:
            vItem = volumeItems.pop(0)
            if EVENTS[digitChange]['description'].find(vItem) > -1:
                if response[-3:].isdigit():
                    event = EVENTS[digitChange]['event'][:-3] + '%.2fDb'
                    volume = float(response[-3:-1] + '.' + response[-1:])
                else:
                    event = EVENTS[digitChange]['event'][:-2] + '%.2fDb'
                    volume = float(response[-2:] + '.0')
                from eg.WinApi.Utils import GetMonitorDimensions

                width = GetMonitorDimensions()[0][2]

                if width > 1800:
                    fontSize = -48
                elif width > 1500:
                    fontSize = -38
                elif width > 1100:
                    fontSize = -28
                else:
                    fontSize = -18

                volumeDb = (volume * (18.0 - -80.0) / 98.0) + -80.0

                osdFill = unicode('⁄', 'utf8')
                osdEmpty = unicode('˛', 'utf8')

                osdText = 'Volume %s%s  %.2f dB' % (
                    osdFill * int(volume),
                    osdEmpty * (98 - int(volume)),
                    volumeDb
                )

                payload = 'Volume %s%s  %.2f dB' % (
                    '/' * int(volume),
                    '.' * (98 - int(volume)),
                    volumeDb
                )

                eg.plugins.EventGhost.ShowOSD(
                    osdText,
                    u'0;%d;0;0;0;700;255;0;0;0;0;2;1;66;Pristina' % fontSize,
                    (37, 251, 32),
                    (0, 0, 0),
                    5,
                    (0, 0),
                    0,
                    5.0,
                    False
                )
                return event % volumeDb, [volumeDb, payload]

        event = re.sub('\*', '%d', EVENTS[digitChange]['event'])
        avrInput = ()
        payload = ['']
        for i, char in enumerate(digitChange):
            if char == '*':
                char = response[i]
                avrInput += (int(char),)
                payload[len(payload) - 1] += char
            elif payload[-1]:
                payload.append('')

        for i, item in enumerate(payload):
            try:
                item = int(item)
            except ValueError:
                pass
            payload[i] = item
        return event % avrInput, payload
    else:
        eg.PrintNotice('Marantz: Unknown message, %r' % response)
        return None, None
