###
### Pioneer Ethernet
### ================

### Public Domain
###
###
### Revision history:
### -----------------
### 0.1 - initial
### 0.2 - Added: 	variable commands (Volume)
###					parsing of received hex additional data
###					standby and resume states working
###					comments into code
###					socket is now managed into the listener
###					debug support
### 0.3 - Modified:	responses from power commands
###					Added: control of excepctions if receiver is disconnected
###					messages indicating connection status 
###

help = """\
Plugin to control Pioneer Receivers via Ethernet.
Note that not all commands work with every model."""

eg.RegisterPlugin(
	name = "Pioneer AV Ethernet",
	author = "sergiensergien (based on Onkyo development by prostetnic, Bartman, Fiasco, FoLLgoTT)",
	version = "0.3." + "$LastChangedRevision: 1246 $".split()[1],
	kind = "external",
	guid = "{50e42894-579e-4ae2-9d9e-3b67c2c338cf}",
	description= "Control Pioneer A/V Receivers via Ethernet",
	help = help,
	canMultiLoad = True,
	createMacrosOnAdd = True,
	icon = (
		"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAA"
		"AAd0SU1FB9YDBAsPCqtpoiUAAAAWdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCAyLjZsqHS1"
		"AAADe0lEQVQ4T02TXVCUZRSAPyZsxpnqoovum+miq+6qFUJYQP7cogS2VpGFAAlKpyAC"
		"EVh+4k80WGADQWlxZRfZACH5ECVY5TdHiEbAIQVkHRzUCZK/ZWGXp10SxjPzXrzvvM9z"
		"zpw5xwUQXg7ndX1jw3VkYmrzycK/gusrgrB3z17hvXfffv2tN99YcXHEi///g07Bznkw"
		"+9i1yvAbqvJKolRJhJ2KQp4ZQWTWd5wsV9Ni6sWybn3tZWYXvjt531V1tgJF8lcEZbij"
		"MLgRbTpAVHcgyk5/QnSefHrmc7QdV1hbX9+VbAvuTk67ZpfVIDsWgu/ZfURfD+TElVBy"
		"m4+TooshvDaAL697EPOHLzK1L9prbayuWbYlwsLzFZfCql+Qx8XhqfoAZUsIhsEGLGsW"
		"Nm12FlZtTM0/w2DSEmn0dEgclRSFcFG8wcamTRAqtO0kpRficdQLpV5Gr7mf3qFHzC1u"
		"YF61MvrIztD0OsP3F6m/ZUDZ7klosxfxJZn0j04hpJ+uIvZ4EpJvJKhvFWOzW1lc2qT/"
		"zznuzdnoGnlG+8BDWnvMDE7M8q1eQcygN6GFkWj0nQgp+WUcilTyUaIHzRPtWKx2rLYt"
		"5hfXHBnMNIjDtHbfY3RmmcdLdkrEfKIHDyDLPYS6vhnhh9wSgiPCcYvbT+3gNQbGluib"
		"WOTG8EOaTGOY/nrKwPgynXdm+H3gCZkNeQ6BP0GnZGgMRoTUnDMcSfgaiUJKWuPP6MRx"
		"LhjvUN3Qh671NnVNQ1y9Oe2YgUmaeqY4WnMEpSgl5ORhzhmaEFRFpSTnOpool+GXFoa6"
		"sQNNXReVupucv9zHeWM3Gl0HNY0mci7VEtF2EJ+8fSTkpSP23EaYmpl1ySgowk8ehiTc"
		"i6iiExRcNKC+0IlG20m5XqRCK5J9qYxoMZSgail+scEUn6vn+bJFImxtbQkl5dWoCkvx"
		"Cg3k/Uh3grKCSahJJln3E8n1BSQ2JhArHuSTUgneET6kFWno6h3GyW5P4sqqRUhMLSCn"
		"uJQA+cdIFYF8GC3F/Xs3vDM8kaZ4sP+YD/4RX5B+Wk1l3SXnkG2zu7uwZrHuqa1rILuw"
		"hNSsfOSxsQQoPkN2WI4iPp7EzBx+dPRLb7zK0orl1Z2FEmwvTM4HZ0kzZvM7hqZfMbaJ"
		"jEw8YHh8kvrGFmr1euaf/iPZAW12uzD2t1n4DwtSpLoLWTYZAAAAAElFTkSuQmCC"
	),
)


import socket
import asynchat
import asyncore
import re
import binascii
import itertools
import operator
import time


cmdList = (
	('Power / Sleep', None, None, None, None),
		('Power.Off',				'Power Off',					'PF',	 None,	'PWR1'  ),
		('Power.On',				'Power On',						'PO',	 None,	'PWR0'  ),	   
	('Master Volume', None, None, None, None),
		('Volume.Up',				'Master Volume Up',				'VU',	 None,	None	),
		('Volume.Down',				'Master Volume Down',			'VD',	 None,	None	),
		('Volume.Set',				'Set Master Volume (00-99)',	'VL',	 '0-99',None  ),
		('Mute.On',					'Mute On',						'MF',	 None,	'MUT0'  ),
		('Mute.Off',				'Mute Off',						'MO',	 None,	'MUT1'  ),
	('Input Select Command', None, None, None, None),
		('Input.DVD',				'DVD',							'04FN',   None, 'FN04'  ),
		('Input.BD',				'BD',							'25FN',   None, 'FN25'  ),
		('Input.TV/SAT',			'TV / SAT',						'05FN',   None, 'FN05'  ),
		('Input.DVR/BRD',			'DVR / BRD',					'15FN',   None, 'FN15'  ),
		('Input.Video',				'Video',						'10FN',   None, 'FN10'  ),
		('Input.HDMI1',				'HDMI 1',						'19FN',   None, 'FN19'  ),
		('Input.HDMI2',				'HDMI 2',						'20FN',   None, 'FN20'  ),
		('Input.HDMI3',				'HDMI 3',						'21FN',   None, 'FN21'  ),
		('Input.HDMI4',				'HDMI 4',						'22FN',   None, 'FN22'  ),
		('Input.HDMIFront',			'HDMI Front',					'23FN',   None, 'FN23'  ),
		('Input.iRadio',			'Internet Radio',				'26FN',   None, 'FN26'  ),
		('Input.IPOD/USB',			'iPOD / USB',					'17FN',   None, 'FN17'  ),
		('Input.XMRadio',			'XM Radio',						'18FN',   None, 'FN18'  ),
		('Input.CD',				'CD',							'01FN',   None, 'FN01'  ),
		('Input.CDR/Tape',			'CD-R / Tape',					'03FN',   None, 'FN03'  ),
		('Input.Tuner',				'Tuner',						'02FN',   None, 'FN02'  ),
		('Input.Adapter',			'Adapter',						'33FN',   None, 'FN33'  ),
		('Input.Sirius',			'Sirius',						'27FN',   None, 'FN27'  ),
		('Input.HDMI.Cycle',		'HDMI Input (Cycle)',			'31FN',   None, None	),
		('Input.Up',				'Next Input',					'FU',	 None, None	),
		('Input.Down',				'Previous Input',				'FD',	 None, None	),
	('Stereo Front Stage Mode', None, None, None, None),
		('Stereo.Cycle',			'Stereo Mode(Cycle)',			'0001SR', None, None	),
		('Stereo.Stereo',			'Stereo',						'0009SR', None, 'LM0001'),
		('Stereo.FrontStageWide',	'Front Stage Wide',				'0004SR', None, 'LM0003'),
		('Stereo.FrontStageNarrow',	'Front Stage Narrow',			'0003SR', None, 'LM0002'),
	('Stream Direct Mode', None, None, None, None),
		('Stream.Cycle',			'Stream Direct Mode (Cycle)',	'0005SR', None, None	),
		('Stream.Direct',			'2 Channel',					'0007SR', None, 'LM0601'),
		('Stream.PureDirect',		'2 Channel',					'0008SR', None, 'LM0701'),
		('Stream.ALC',				'2 Channel',					'0151SR', None, 'LM0501'),
		('Stream.Auto Surround',	'2 Channel',					'0006SR', None, 'LM0401'),
	('Surround Mode', None, None, None, None),
		('Surround.Cycle',			'Dolby Surround Mode (Cycle)',	'0010SR', None, None),
		('Surround.ProLogic',		'Dolby ProLogic',				'0012SR', None, 'LM0107'),
		('Surround.PLIIxMovie',		'Dolby ProLogic IIx Movie',		'0013SR', None, 'LM0102'),
		('Surround.PLIIxMusic',		'Dolby ProLogic IIx Music',		'0014SR', None, 'LM0104'),
		('Surround.PLIIxGame',		'Dolby ProLogic IIx Game',		'0015SR', None, 'LM0106'),
		('Surround.Neo6Cinema',		'Neo:6 Cinema',					'0016SR', None, 'LM0108'),
		('Surround.Neo6Music',		'Neo:6 Music',					'0017SR', None, 'LM0109'),
		('Surround.PLIIz',			'Dolby ProLogic IIz Height (*)',None	, None, None	),
		('Surround.WideSrndMovie',	'Wide Surround Movie (*)',		None	, None, None	),
		('Surround.WideSrndMusic',	'Wide Surround Music (*)',		None	, None, None	),
		('Surround.NeuralSrnd',		'Neural Surround (*)',			None	, None, None	),
		('Surround.DolbyDigitalEX',	'Dolby Digital EX (*)',			None	, None, None	),
		('Surround.DTS.ES',			'DTS ES (*)',					None	, None, None	),
		('Surround.DTS.Neo6',		'DTS Neo:6 (*)',				None	, None, None	),
		('Surround.NeuralSrnd',		'Neural Surround (*)',			None	, None, None	),
	('Advanced Surround', None, None, None, None),
		('Advanced.Cycle',			'Wide Surround Movie',			'0100SR', None, None	),
		('Advanced.Action',			'Adv. Surround: Action',		'0101SR', None, 'LM0201'),
		('Advanced.Sci-Fi',			'Adv. Surround: Sci-Fi',		'0102SR', None, 'LM0203'),
		('Advanced.Drama',			'Adv. Surround: Drama',			'0103SR', None, 'LM0202'),
		('Advanced.Show',			'Adv. Surround: Show',			'0104SR', None, 'LM0202'),
		('Advanced.MonoFilm',		'Adv. Surround: Mono Film',		'0105SR', None, 'LM0205'),
		('Advanced.Expanded',		'Adv. Surround: Expanded',		'0106SR', None, 'LM0204'),
		('Advanced.Classical',		'Adv. Surround: Classical',		'0107SR', None, 'LM0206'),
		('Advanced.Unplugged',		'Adv. Surround: Unplugged',		'0109SR', None, 'LM020a'),
		('Advanced.Pop/Rock',		'Adv. Surround: Pop/Rock',		'0110SR', None, 'LM020c'),
		('Advanced.ExpStereo',		'Adv. Surround: Exp. Stereo',	'0111SR', None, 'LM020b'),
		('Advanced.TVSurround',		'Adv. Surround: TV Surround',	'0112SR', None, 'LM020d'),
		('Advanced.AdvancedGame',	'Adv. Surround: Advanced Game',	'0116SR', None, 'LM0207'),
		('Advanced.Sports',			'Adv. Surround: Sports',		'0118SR', None, 'LM0208'),
		('Advanced.PhonesSrnd',		'Adv. Surround: Phones Srnd. (*)', None,	 None, None	),
	('State Queries', None, None, None, None),
		('Power.State',				'Returns Power State',			'?P',	None,	'PWR'   ),
		('Volume.State',			'Returns Master Volume level',	'?V',	None,	'VOL'   ),
		('Mute.State',				'Returns Mute State',			'?M',	None,	'MUT'   ),
		('Video.State',				'Returns Video State',			'?VST',	None,	'VST'   ),
		('Audio.State',				'Returns Audio State',			'?AST',	None,	'AST'   ),
		('Input.State',				'Returns Current Input',		'?F',	None,	'FN'	),
		('Listening.Mode',			'Returns Listening Mode',		'?S',	None,	'SR'	),
		('Listening.Info',			'Returns Listening Info',		'?L',	None,	'LM'	),
	(None, None, None, None, None),	   
)


FN_List = (
	('04' , 'DVD'),
	('25' , 'BD'),
	('05' , 'TV/SAT'),
	('15' , 'DVR/BDR'),
	('10' , 'VIDEO 1(VIDEO)'),
	('14' , 'VIDEO 2'),
	('19' , 'HDMI 1'),
	('20' , 'HDMI 2'),
	('21' , 'HDMI 3'),
	('22' , 'HDMI 4'),
	('23' , 'HDMI 5'),
	('26' , 'HOME MEDIA GALLERY(Internet Radio)'),
	('17' , 'iPod/USB'),
	('18' , 'XM RADIO'),
	('01' , 'CD'),
	('03' , 'CD-R/TAPE'),
	('02' , 'TUNER'),
	('00' , 'PHONO'),
	('12' , 'MULTI CH IN'),
	('33' , 'ADAPTER PORT'),
	('27' , 'SIRIUS'),
	('31' , 'HDMI (cyclic)'),
)

SR_List= (
	('0001' , 'STEREO (cyclic)'),
	('0009' , 'STEREO (direct set)'),
	('0151' , 'Auto Level Control (A.L.C.)'),
	('0003' , 'Front Stage Surround Advance Focus'),
	('0004' , 'Front Stage Surround Advance Wide'),
	('0153' , 'RETRIEVER AIR'),
	('0010' , 'STANDARD'),
	('0011' , '(2ch source)'),
	('0013' , 'PRO LOGIC2 MOVIE'),
	('0018' , 'PRO LOGIC2x MOVIE'),
	('0014' , 'PRO LOGIC2 MUSIC'),
	('0019' , 'PRO LOGIC2x MUSIC'),
	('0015' , 'PRO LOGIC2 GAME'),
	('0020' , 'PRO LOGIC2x GAME'),
	('0031' , 'PRO LOGIC2z Height'),
	('0032' , 'WIDE SURROUND MOVIE'),
	('0033' , 'WIDE SURROUND MUSIC'),
	('0012' , 'PRO LOGIC'),
	('0016' , 'Neo:6 CINEMA'),
	('0017' , 'Neo:6 MUSIC'),
	('0028' , 'XM HD SURROUND'),
	('0029' , 'NEURAL SURROUND'),
	('0021' , '(Multi ch source)'),
	('0022' , '(Multi ch source)+DOLBY EX'),
	('0023' , '(Multi ch source)+PRO LOGIC2x MOVIE'),
	('0024' , '(Multi ch source)+PRO LOGIC2x MUSIC'),
	('0034' , '(Multi-ch Source)+PRO LOGIC2z HEIGHT'),
	('0035' , '(Multi-ch Source)+WIDE SURROUND MOVIE'),
	('0036' , '(Multi-ch Source)+WIDE SURROUND MUSIC'),
	('0025' , 'DTS-ES Neo:6'),
	('0026' , 'DTS-ES matrix'),
	('0027' , 'DTS-ES discrete'),
	('0030' , 'DTS-ES 8ch discrete'),
	('0100' , 'ADVANCED SURROUND (cyclic)'),
	('0101' , 'ACTION'),
	('0103' , 'DRAMA'),
	('0102' , 'SCI-FI'),
	('0105' , 'MONO FILM'),
	('0104' , 'ENTERTAINMENT SHOW'),
	('0106' , 'EXPANDED THEATER'),
	('0116' , 'TV SURROUND'),
	('0118' , 'ADVANCED GAME'),
	('0117' , 'SPORTS'),
	('0107' , 'CLASSICAL'),
	('0110' , 'ROCK/POP'),
	('0109' , 'UNPLUGGED'),
	('0112' , 'EXTENDED STEREO'),
	('0113' , 'PHONES SURROUND'),
	('0050' , 'THX (cyclic)'),
	('0051' , 'PROLOGIC + THX CINEMA'),
	('0052' , 'PL2 MOVIE + THX CINEMA'),
	('0053' , 'Neo:6 CINEMA + THX CINEMA'),
	('0054' , 'PL2x MOVIE + THX CINEMA'),
	('0092' , 'PL2z HEIGHT + THX CINEMA'),
	('0055' , 'THX SELECT2 GAMES'),
	('0068' , 'THX CINEMA (for 2ch)'),
	('0069' , 'THX MUSIC (for 2ch)'),
	('0070' , 'THX GAMES (for 2ch)'),
	('0071' , 'PL2 MUSIC + THX MUSIC'),
	('0072' , 'PL2x MUSIC + THX MUSIC'),
	('0093' , 'PL2z HEIGHT + THX MUSIC'),
	('0073' , 'Neo:6 MUSIC + THX MUSIC'),
	('0074' , 'PL2 GAME + THX GAMES'),
	('0075' , 'PL2x GAME + THX GAMES'),
	('0094' , 'PL2z HEIGHT + THX GAMES'),
	('0076' , 'THX ULTRA2 GAMES'),
	('0077' , 'PROLOGIC + THX MUSIC'),
	('0078' , 'PROLOGIC + THX GAMES'),
	('0056' , 'THX CINEMA (for multi ch)'),
	('0057' , 'THX SURROUND EX (for multi ch)'),
	('0058' , 'PL2x MOVIE + THX CINEMA (for multi ch)'),
	('0095' , 'PL2z HEIGHT + THX CINEMA (for multi ch)'),
	('0059' , 'ES Neo:6 + THX CINEMA (for multi ch)'),
	('0060' , 'ES MATRIX + THX CINEMA (for multi ch)'),
	('0061' , 'ES DISCRETE + THX CINEMA (for multi ch)'),
	('0067' , 'ES 8ch DISCRETE + THX CINEMA (for multi ch)'),
	('0062' , 'THX SELECT2 CINEMA (for multi ch)'),
	('0063' , 'THX SELECT2 MUSIC (for multi ch)'),
	('0064' , 'THX SELECT2 GAMES (for multi ch)'),
	('0065' , 'THX ULTRA2 CINEMA (for multi ch)'),
	('0066' , 'THX ULTRA2 MUSIC (for multi ch)'),
	('0079' , 'THX ULTRA2 GAMES (for multi ch)'),
	('0080' , 'THX MUSIC (for multi ch)'),
	('0081' , 'THX GAMES (for multi ch)'),
	('0082' , 'PL2x MUSIC + THX MUSIC (for multi ch)'),
	('0096' , 'PL2z HEIGHT + THX MUSIC (for multi ch)'),
	('0083' , 'EX + THX GAMES (for multi ch)'),
	('0097' , 'PL2z HEIGHT + THX GAMES (for multi ch)'),
	('0084' , 'Neo:6 + THX MUSIC (for multi ch)'),
	('0085' , 'Neo:6 + THX GAMES (for multi ch)'),
	('0086' , 'ES MATRIX + THX MUSIC (for multi ch)'),
	('0087' , 'ES MATRIX + THX GAMES (for multi ch)'),
	('0088' , 'ES DISCRETE + THX MUSIC (for multi ch)'),
	('0089' , 'ES DISCRETE + THX GAMES (for multi ch)'),
	('0090' , 'ES 8CH DISCRETE + THX MUSIC (for multi ch)'),
	('0091' , 'ES 8CH DISCRETE + THX GAMES (for multi ch)'),
	('0005' , 'AUTO SURR/STREAM DIRECT (cyclic)'),
	('0006' , 'AUTO SURROUND'),
	('0152' , 'OPTIMUM SURROUND'),
	('0151' , 'Auto Level Control (A.L.C.)'),
	('0007' , 'DIRECT'),
	('0008' , 'PURE DIRECT'),
)

LM_List = (
	('0001' , 'STEREO'),
	('0002' , 'F.S.SURR FOCUS'),
	('0003' , 'F.S.SURR WIDE'),
	('0004' , 'RETRIEVER AIR'),
	('0101' , '[)(]PLIIx MOVIE'),
	('0102' , '[)(]PLII MOVIE'),
	('0103' , '[)(]PLIIx MUSIC'),
	('0104' , '[)(]PLII MUSIC'),
	('0105' , '[)(]PLIIx GAME'),
	('0106' , '[)(]PLII GAME'),
	('0107' , '[)(]PROLOGIC'),
	('0108' , 'Neo:6 CINEMA'),
	('0109' , 'Neo:6 MUSIC'),
	('010a' , 'XM HD Surround'),
	('010b' , 'NEURAL SURR'),
	('010c' , '2ch Straight Decode'),
	('010d' , '[)(]PLIIz HEIGHT'),
	('010e' , 'WIDE SURR MOVIE'),
	('010f' , 'WIDE SURR MUSIC'),
	('1101' , '[)(]PLIIx MOVIE'),
	('1102' , '[)(]PLIIx MUSIC'),
	('1103' , '[)(]DIGITAL EX'),
	('1104' , 'DTS +Neo:6 / DTS-HD +Neo:6'),
	('1105' , 'ES MATRIX'),
	('1106' , 'ES DISCRETE'),
	('1107' , 'DTS-ES 7.1'),
	('1108' , 'multi ch Straight Decode'),
	('1109' , '[)(]PLIIz HEIGHT'),
	('110a' , 'WIDE SURR MOVIE'),
	('110b' , 'WIDE SURR MUSIC'),
	('0201' , 'ACTION'),
	('0202' , 'DRAMA'),
	('0203' , 'SCI-FI'),
	('0204' , 'MONOFILM'),
	('0205' , 'ENT.SHOW'),
	('0206' , 'EXPANDED'),
	('0207' , 'TV SURROUND'),
	('0208' , 'ADVANCEDGAME'),
	('0209' , 'SPORTS'),
	('020a' , 'CLASSICAL'),
	('020b' , 'ROCK/POP'),
	('020c' , 'UNPLUGGED'),
	('020d' , 'EXT.STEREO'),
	('020e' , 'PHONES SURR.'),
	('0301' , '[)(]PLIIx MOVIE +THX'),
	('0302' , '[)(]PLII MOVIE +THX'),
	('0303' , '[)(]PL +THX CINEMA'),
	('0304' , 'Neo:6 CINEMA +THX'),
	('0305' , 'THX CINEMA'),
	('0306' , '[)(]PLIIx MUSIC +THX'),
	('0307' , '[)(]PLII MUSIC +THX'),
	('0308' , '[)(]PL +THX MUSIC'),
	('0309' , 'Neo:6 MUSIC +THX'),
	('030a' , 'THX MUSIC'),
	('030b' , '[)(]PLIIx GAME +THX'),
	('030c' , '[)(]PLII GAME +THX'),
	('030d' , '[)(]PL +THX GAMES'),
	('030e' , 'THX ULTRA2 GAMES'),
	('030f' , 'THX SELECT2 GAMES'),
	('0310' , 'THX GAMES'),
	('0311' , '[)(]PLIIz +THX CINEMA'),
	('0312' , '[)(]PLIIz +THX MUSIC'),
	('0313' , '[)(]PLIIz +THX GAMES'),
	('1301' , 'THX Surr EX'),
	('1302' , 'Neo:6 +THX CINEMA'),
	('1303' , 'ES MTRX +THX CINEMA'),
	('1304' , 'ES DISC +THX CINEMA'),
	('1305' , 'ES7.1 +THX CINEMA'),
	('1306' , '[)(]PLIIx MOVIE +THX'),
	('1307' , 'THX ULTRA2 CINEMA'),
	('1308' , 'THX SELECT2 CINEMA'),
	('1309' , 'THX CINEMA'),
	('130a' , 'Neo:6 +THX MUSIC'),
	('130b' , 'ES MTRX +THX MUSIC'),
	('130c' , 'ES DISC +THX MUSIC'),
	('130d' , 'ES7.1 +THX MUSIC'),
	('130e' , '[)(]PLIIx MUSIC +THX'),
	('130f' , 'THX ULTRA2 MUSIC'),
	('1310' , 'THX SELECT2 MUSIC'),
	('1311' , 'THX MUSIC'),
	('1312' , 'Neo:6 +THX GAMES'),
	('1313' , 'ES MTRX +THX GAMES'),
	('1314' , 'ES DISC +THX GAMES'),
	('1315' , 'ES7.1 +THX GAMES'),
	('1316' , '[)(]EX +THX GAMES'),
	('1317' , 'THX ULTRA2 GAMES'),
	('1318' , 'THX SELECT2 GAMES'),
	('1319' , 'THX GAMES'),
	('131a' , '[)(]PLIIz +THX CINEMA'),
	('131b' , '[)(]PLIIz +THX MUSIC'),
	('131c' , '[)(]PLIIz +THX GAMES'),
	('0401' , 'STEREO'),
	('0402' , '[)(]PLII MOVIE'),
	('0403' , '[)(]PLIIx MOVIE'),
	('0404' , 'Neo:6 CINEMA'),
	('0405' , 'AUTO SURROUND Straight Decode'),
	('0406' , '[)(]DIGITAL EX'),
	('0407' , '[)(]PLIIx MOVIE'),
	('0408' , 'DTS +Neo:6'),
	('0409' , 'ES MATRIX'),
	('040a' , 'ES DISCRETE'),
	('040b' , 'DTS-ES 7.1'),
	('040c' , 'XM HD Surround'),
	('040d' , 'NEURALSURR'),
	('040e' , 'RETRIEVER AIR'),
	('0501' , 'STEREO'),
	('0502' , '[)(]PLII MOVIE'),
	('0503' , '[)(]PLIIx MOVIE'),
	('0504' , 'Neo:6 CINEMA'),
	('0505' , 'ALC Straight Decode'),
	('0506' , '[)(]DIGITAL EX'),
	('0507' , '[)(]PLIIx MOVIE'),
	('0508' , 'DTS +Neo:6'),
	('0509' , 'ES MATRIX'),
	('050a' , 'ES DISCRETE'),
	('050b' , 'DTS-ES 7.1'),
	('050c' , 'XM HD Surround'),
	('050d' , 'NEURAL SURR'),
	('050e' , 'RETRIEVER AIR'),
	('0601' , 'STEREO'),
	('0602' , '[)(]PLII MOVIE'),
	('0603' , '[)(]PLIIx MOVIE'),
	('0604' , 'Neo:6 CINEMA'),
	('0605' , 'STREAM DIRECT NORMAL Straight Decode'),
	('0606' , '[)(]DIGITAL EX'),
	('0607' , '[)(]PLIIx MOVIE'),
	('0608' , '(nothing)'),
	('0609' , 'ES MATRIX'),
	('060a' , 'ES DISCRETE'),
	('060b' , 'DTS-ES 7.1'),
	('0701' , 'STREAM DIRECT PURE 2ch'),
	('0702' , '[)(]PLII MOVIE'),
	('0703' , '[)(]PLIIx MOVIE'),
	('0704' , 'Neo:6 CINEMA'),
	('0705' , 'STREAM DIRECT PURE Straight Decode'),
	('0706' , '[)(]DIGITAL EX'),
	('0707' , '[)(]PLIIx MOVIE'),
	('0708' , '(nothing)'),
	('0709' , 'ES MATRIX'),
	('070a' , 'ES DISCRETE'),
	('070b' , 'DTS-ES 7.1'),
	('0881' , 'OPTIMUM'),
	('0e01' , 'HDMI THROUGH'),
	('0f01' , 'MULTI CH IN'),
)

# AST #############################################################################################
AST_signal = (					# Input Data 1-2		Output 
	('00' , 'ANALOG'),
	('01' , 'ANALOG'),
	('02' , 'ANALOG'),
	('03' , 'PCM'),
	('04' , 'PCM'),
	('05' , 'DOLBY DIGITAL'),
	('06' , 'DTS'),
	('07' , 'DTS-ES Matrix'),
	('08' , 'DTS-ES Discrete'),
	('09' , 'DTS 96/24'),
	('10' , 'DTS 96/24 ES Matrix'),
	('11' , 'DTS 96/24 ES Discrete'),
	('12' , 'MPEG-2 AAC'),
	('13' , 'WMA9 Pro'),
	('14' , 'DSD->PCM'),
	('15' , 'HDMI THROUGH'),
	('16' , 'DOLBY DIGITAL PLUS'),
	('17' , 'DOLBY TrueHD'),
	('18' , 'DTS EXPRESS'),
	('19' , 'DTS-HD Master Audio'),
	('20' , 'DTS-HD High Resolution'),
	('21' , 'DTS-HD High Resolution'),
	('22' , 'DTS-HD High Resolution'),
	('23' , 'DTS-HD High Resolution'),
	('24' , 'DTS-HD High Resolution'),
	('25' , 'DTS-HD High Resolution'),
	('26' , 'DTS-HD High Resolution'),
	('27' , 'DTS-HD Master Audio'),
)
AST_frequency = (				# Input Data 3-4		Output 
	('00' , '32kHz'),
	('01' , '44.1kHz'),
	('02' , '48kHz'),
	('03' , '88.2kHz'),
	('04' , '96kHz'),
	('05' , '176.4kHz'),
	('06' , '192kHz'),
)

#VST DATA #########################################################################################
#Data 2-3	Output Resolution Data 8-9
VST_resolution = (
	('00' , '---'),
	('01' , '480/60i'),
	('02' , '576/50i'),
	('03' , '480/60p'),
	('04' , '576/50p'),
	('05' , '720/60p'),
	('06' , '720/50p'),
	('07' , '1080/60i'),
	('08' , '1080/50i'),
	('09' , '1080/60p'),
	('10' , '1080/50p'),
	('11' , '1080/24p'),
)
VST_aspect = (			# Data 4	Output Data 10
	('0' , '---'),
	('1' , '4:3'),
	('2' , '16:9'),
	('3' , '14:9'),
)
VST_color_format = (		# Data 5	Output Data 11
	('0' , '---'),
	('1' , 'RGB Limit'),
	('2' , 'RGB Full'),
	('3' , 'YcbCr444'),
	('4' , 'YcbCr422'),
)
VST_bit = (				# Data 6	Output Data 12
	('0' , '---'),
	('1' , '24bit (8bit*3)'),
	('2' , '30bit (10bit*3)'),
	('3' , '36bit (12bit*3)'),
	('4' , '48bit (16bit*3)'),
)
VST_extend_color_space = (		#Data 7		Output Data 13
	('0' , '---'),
	('1' , 'Standard'),
	('2' , 'xvYCC601'),
	('3' , 'xvYCC709'),
	('4' , 'sYCC'),
	('5' , 'AdobeYCC601'),
	('6' , 'AdobeRGB'),
)


# Coding ##########################################################################################
class PioneerEventer(asynchat.async_chat):
	"""Pioneer engine class. Implements command line user interface."""

	### Initializing all the variables and open the tcp connection..
	###
	def __init__(self, host, port, plugin): 
		asynchat.async_chat.__init__(self)   
		self.set_terminator("\x0d\x0a")
		self.reading_headers = False
		self.data = ""
		self.host = host
		self.port = port
		self.plugin = plugin
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.socket.connect((self.host, self.port))
			connected = True
		except socket.error, exc:
			print 'PIONEER: Connect fail:', (self.host, self.port)
			connected = False
		if connected == True:
			asynchat.async_chat.__init__(self, sock=self.socket)   
			self.plugin.TriggerEvent("connected")
		eg.RestartAsyncore()
		
	### This will be run if the connections is succesful
	###
	def handle_connect(self):
		# connection succeeded
		connected = True
		print "PIONEER: Listening to device started"
		
	### This will be run if the tcp connection is disconnected
	### or if we want to close it ourselves.
	###
	def handle_close(self):
		print "PIONEER: Listener Close"
		# self.handler.reader = None
		connected = False
		self.plugin.TriggerEvent("disconnected")
		self.close()
		
	### This will be run if there is a problem opening the connection
	###
	def handle_expt(self):
		# connection failed
		# if eg.debugLevel:
		eg.PrintTraceback()
		connected = False
		print "PIONEER: Listener Failed"
		self.plugin.TriggerEvent("disconnected")
		self.close()

	### This gets run whenever asynchat detects there is data waiting
	### for us to be read at the socket, to put it in our buffer
	###
	def collect_incoming_data(self, data):
		# received a chunk of incoming data
		self.data = self.data + data
		if eg.debugLevel:
			print "PIONEER (Debug): Eventer Collecting"

	### This gets run whenever asynchat detects there is data waiting
	### for us to be examined, so this is where it's all at..
	###
	def found_terminator(self):
		# got a response line
		data = self.data
		self.data = ""
		
		#COMMAND Handling
		command = data[:3]
		try:
			test = int(command[-1:])
			command = command[:2]
			payload = data[-(len(data)-2):]
		except:
			command = command[:3]
			payload = data[-(len(data)-3):]

		if command == 'VOL':
			payload = payload
		elif command == 'LM':
			try:
				payload = dict(LM_List)[payload]
			except:
				payload = ''
		elif command == 'SR':
			try:
				payload = dict(SR_List)[payload]
			except:
				payload = ''
		elif command == 'FN':
			try:
				payload = dict(FN_List)[payload]
			except:
				payload = ''
		elif command == 'AST':
			try:
				ast_evt_channels	= str(int(payload[4])+int(payload[5])+int(payload[6])+int(payload[7])+int(payload[8])+int(payload[9])+int(payload[10])+int(payload[11])) + '.' + str(int(payload[12]))
				ast_evt_signal		= dict(AST_signal)[payload[0:2]]
				ast_evt_frequency	= dict(AST_frequency)[payload[2:4]]
			except:
				ast_evt_channels	= ''
				ast_evt_signal		= ''
				ast_evt_frequency	= ''
		elif command == 'VST':
			try:
				VST_evt_in_resolution			= dict(VST_resolution)[payload[1:3]] #2-3
				VST_evt_out_resolution			= dict(VST_resolution)[payload[7:9]] #8-9
				VST_evt_in_aspect				= dict(VST_aspect)[payload[3:4]] #4
				VST_evt_out_aspect				= dict(VST_aspect)[payload[9:10]] #10
				VST_evt_in_color_format			= dict(VST_color_format)[payload[4:5]] #5
				VST_evt_out_color_format		= dict(VST_color_format)[payload[10:11]] #11
				VST_evt_in_bit					= dict(VST_bit)[payload[5:6]] #6
				VST_evt_out_bit					= dict(VST_bit)[payload[11:12]] #12
				VST_evt_in_extend_color_space	= dict(VST_extend_color_space)[payload[6:7]] #7
				VST_evt_out_extend_color_space	= dict(VST_extend_color_space)[payload[12:13]] #13
			except:
				VST_evt_in_resolution			= '' #2-3
				VST_evt_out_resolution			= '' #8-9
				VST_evt_in_aspect				= '' #4
				VST_evt_out_aspect				= '' #10
				VST_evt_in_color_format			= '' #5
				VST_evt_out_color_format		= '' #11
				VST_evt_in_bit					= '' #6
				VST_evt_out_bit					= '' #12
				VST_evt_in_extend_color_space	= '' #7
				VST_evt_out_extend_color_space	= '' #13
		else:
			payload = payload

		if eg.debugLevel:
			print "PIONEER (Debug): Received " + str(data)
		
		### The PIONEER device sends a keep-alive consisting only in the terminator
		### So if "data" is not empty, we want to process it.
		if len(data):
			### First we search through our known fixed responses for a match 
			response = operator.itemgetter(4)
			try:
				datum = map(response, cmdList).index(str(command))
				if command <> 'AST' and command <> 'VST':
					self.plugin.TriggerEvent("Received." + cmdList[datum][0], str(payload))
				elif command == 'AST':
					self.plugin.TriggerEvent("Received.AST.Channels", str(ast_evt_channels))
					self.plugin.TriggerEvent("Received.AST.Signal", str(ast_evt_signal))
					self.plugin.TriggerEvent("Received.AST.Frequency", str(ast_evt_frequency))
				elif command == 'VST':
					self.plugin.TriggerEvent("Received.VST.in.Resolution", str(VST_evt_in_resolution))
					self.plugin.TriggerEvent("Received.VST.out.Resolution", str(VST_evt_out_resolution))
					self.plugin.TriggerEvent("Received.VST.in.Aspect", str(VST_evt_in_aspect))
					self.plugin.TriggerEvent("Received.VST.out.Aspect", str(VST_evt_out_aspect))
					self.plugin.TriggerEvent("Received.VST.in.Color_Format", str(VST_evt_in_color_format))
					self.plugin.TriggerEvent("Received.VST.out.Color_Format", str(VST_evt_out_color_format))
					self.plugin.TriggerEvent("Received.VST.in.Bit", str(VST_evt_in_bit))
					self.plugin.TriggerEvent("Received.VST.out.Bit", str(VST_evt_out_bit))
					self.plugin.TriggerEvent("Received.VST.in.extend_color_space", str(VST_evt_in_extend_color_space))
					self.plugin.TriggerEvent("Received.VST.out.extend_color_space", str(VST_evt_out_extend_color_space))
			except ValueError:
				### If not fixed match, it can be a long info message ...
				if len(data) > 6:
					print "PIONEER: Says " + data[:4] + " : " + binascii.unhexlify(data[4:])
				### Or, perhaps, it's a big hole in our knowledge of Pioneer devices ...
				else:
					self.plugin.TriggerEvent("Received.Unknown", str(data))
		else:
			if eg.debugLevel:
				print "PIONEER (Debug): Keep alive"

### Sends data to our device when called (with no additional argument)
###
class CmdAction(eg.ActionClass):
	"""Base class for all argumentless actions"""

	def __call__(self):
		if self.plugin.eventer == 0:
			self.plugin.InitConnection()	
		if self.plugin.eventer.connected == True:
			datum = self.plugin.eventer.socket.send(str(self.cmd) + '\x0d')
			if eg.debugLevel:
				print "PIONEER (Debug): Send (" + repr(datum) + ") : " + str(self.cmd)
		else:
			self.plugin.TriggerEvent("disconnected")

### Sends data to our device when called (with additional argument)
###
class ValueAction(eg.ActionWithStringParameter):
	"""Base class for all actions with adjustable argument"""

	def __call__(self, data):
		if self.plugin.eventer == 0:
			self.plugin.InitConnection()	
		if self.plugin.eventer.connected == True:
			datum = self.plugin.eventer.socket.send(str(data) + str(self.cmd) + '\x0d')
			if eg.debugLevel:
				print "PIONEER (Debug): Send (" + repr(datum) + ") : " + str(self.cmd) + " = " + data
		else:
			self.plugin.TriggerEvent("disconnected")


### Sends RAW data to our device when called (with no additional argument)
###
class Raw(eg.ActionWithStringParameter):
	name = 'Send Raw command'

	def __call__(self, data):
		if self.plugin.eventer == 0:
			self.plugin.InitConnection()	
		if self.plugin.eventer.connected == True:
			datum = self.plugin.eventer.socket.send(str(data) + '\x0d')
			if eg.debugLevel:
				print "PIONEER (Debug): RAW Send (" + repr(datum) + ") : " + str(data)
		else:
			self.plugin.TriggerEvent("disconnected")

### The EventGhost classes and functions are over here..
###
###
class PioneerEthernet(eg.PluginClass):

	### Initialization of the plugin.
	### We load all the commands from the command table.
	###
	def __init__(self):
		self.serial = None
		group = self

		for cmd_name, cmd_text, cmd_cmd, cmd_rangespec, cmd_answer in cmdList:
			if cmd_text is None:
				# New subgroup, or back up
				if cmd_name is None:
					group = self
				else:
					group = self.AddGroup(cmd_name)
			elif cmd_rangespec is not None:
				# Command with argument
				actionName, paramDescr = cmd_text.split("(")
				actionName = actionName.strip()
				paramDescr = paramDescr[:-1]
				minValue, maxValue = cmd_rangespec.split("-")

				class Action(ValueAction):
					name = actionName
					cmd = cmd_cmd
					parameterDescription = "Value: (%s)" % paramDescr
				Action.__name__ = cmd_name
				group.AddAction(Action)
			else:
				# Argumentless command
				class Action(CmdAction):
					name = cmd_text
					cmd = cmd_cmd
				Action.__name__ = cmd_name
				group.AddAction(Action)

		group.AddAction(Raw)

	def __start__(self, host, port):
		self.host = host
		self.port = port
		self.InitConnection()

	def __stop__(self):
		if self.eventer:
			self.eventer.close()
		self.eventer = None
		return

	### Listener Initialization. It is called when the plugin starts and
	### when the system cames back from a suspended state.
	###
	def InitConnection(self):
		try:
			self.eventer = PioneerEventer(self.host, self.port, self)			
		except socket.error, exc:
			self.eventer = 0
			raise self.Exception(exc[1])

		#Send useful Queries to start macros if needed
		if self.eventer.connected != 0:
			datum = self.eventer.socket.send('?M\x0d')
			datum = self.eventer.socket.send('?F\x0d')
			datum = self.eventer.socket.send('?L\x0d')
			datum = self.eventer.socket.send('?S\x0d')
			datum = self.eventer.socket.send('?V\x0d')
			datum = self.eventer.socket.send('?AST\x0d')
			datum = self.eventer.socket.send('?VST\x0d')
	
	### When we suspend the systems we close down the connection
	### to the device.
	###
	def OnComputerSuspend(self, suspendType):
		if self.eventer:
			self.eventer.handle_close()
			print "PIONEER: Disconnected from the PIONEER device!"
		self.eventer = None

	### When we resume from a suspended state we have to wait for the
	### interfaces to came back in line and restablish the connections ...
	### the waiting time can be up to 20 secs in wireless enviroment.
	###
	def OnComputerResume(self, suspendType):
		print "PIONEER: Resuming connection to PIONEER device"
		time.sleep(20)
		self.InitConnection()

	### Plugin configuration.
	### Change "host" with the IP of the PIONEER device.
	###
	def Configure(self, host="192.168.178.20", port=8102):
		panel = eg.ConfigPanel()
		hostCtrl = panel.TextCtrl(host)
		portCtrl = panel.SpinIntCtrl(port, max=65535)

		panel.AddLine("Host:", hostCtrl)
		panel.AddLine("Port:", portCtrl)

		while panel.Affirmed():
			panel.SetResult(
				hostCtrl.GetValue(),
				portCtrl.GetValue()
			)
