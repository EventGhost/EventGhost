eg.RegisterPlugin(
    name = "Meedio",
    author = "jorel1969",
    version = "0.1.1093",
    kind = "program",
    guid = "{B20B058A-613D-4695-98F0-D55408555361}",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control <a href="http://www.meedio.com/">Meedio</a>.'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=260",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1wgDEBgNAaYl"
        "jAAAABd0RVh0U29mdHdhcmUAR0xEUE5HIHZlciAzLjRxhaThAAAACHRwTkdHTEQzAAAA"
        "AEqAKR8AAAAEZ0FNQQAAsY8L/GEFAAACDElEQVR4nGNgAIIn27favjp+VIGBSPBk6ybb"
        "D9evSoA58yNDYlcIcf5Zqyh579vzZ5yEND/euskSqP73BnX5q90N9ewMParyLcsFOf4B"
        "Bf/dnDEljJABB0J854HUrxTjfdxRXsbLcOzgQZZLbU2JO+zM9uwP9Jrw+8sXJlyagc4W"
        "3ulotelYanz723NnpDEU3J43y221tNDbNXJiV9aryx8DGrhrk57aISD/HBA/XSHC/fbT"
        "ndvcOJ337vJFNaBX/m7WEvh/xE/m/8kohf/n01T+Xy3R+H80UPY/0JCHeP338eZ1MaAB"
        "Py5mq/77vtv+/7dddnD6QoYKyIDThAzgAhrw5Xq55n+QRmR8Ilz+/y4X2z1EGXC3WRfD"
        "BQfcJP+DwoSQAfxAA7496jfEcMEOU5H/221M9xEyQBpowK/7HXr/nkwy+n+rTvvfhUyV"
        "/8dD5f6tluIGhcFZvAY82bbZGBQLQPwdGGVfgBo+AqP1E5D/FWTwGlnRp1g1ApOn+ZH4"
        "iO693i79b06fVAO6ROjz/XvsILnfX78yAfk8INc9XLfKareb/SJgwkv58ughP1jzBEPt"
        "Cqit/8/VlBfhdSIQbNJXPwFSu1KM71FjaooIw2QL4xpo2v705twZKUIGXGyqywGpXyUp"
        "+LI5K0OU4djhw8zXJ/dHPli9woaQZhD48+M7y8XmuvRXJ45pgvgAfoQui0aPQukAAAAA"
        "SUVORK5CYII="
    ),
)

# changelog:
# 0.1 by jorel1969
#     - initial version


import win32gui


# function for controlling meedio using SendMessage
def controlMeedio(inputVal):
    try:
      hMeedioWnd = win32gui.FindWindow('H2-WM-COMMAND', None)
      return win32gui.SendMessage(hMeedioWnd, 273, inputVal, 0)
    except Exception:
      pass



class MeedioPlugin(eg.PluginClass):

  def __init__(self):
    self.AddAction(Up)
    self.AddAction(Down)
    self.AddAction(Left)
    self.AddAction(Right)
    self.AddAction(Select)
    self.AddAction(Back)
    self.AddAction(ChannelUp)
    self.AddAction(ChannelDn)
    self.AddAction(Num0)
    self.AddAction(Num1)
    self.AddAction(Num2)
    self.AddAction(Num3)
    self.AddAction(Num4)
    self.AddAction(Num5)
    self.AddAction(Num6)
    self.AddAction(Num7)
    self.AddAction(Num8)
    self.AddAction(Num9)
    self.AddAction(Enter)
    self.AddAction(Play)
    self.AddAction(Pause)
    self.AddAction(Next)
    self.AddAction(Previous)
    self.AddAction(FFwd)
    self.AddAction(Rew)
    self.AddAction(Stop)
    self.AddAction(Record)
    self.AddAction(Display)
    self.AddAction(VolUp)
    self.AddAction(VolDn)
    self.AddAction(PrevCh)
    self.AddAction(Guide)
    self.AddAction(Menu)
    self.AddAction(Info)
    self.AddAction(Exit)
    self.AddAction(Power)
    self.AddAction(Clear)
    self.AddAction(Top)
    self.AddAction(Bottom)
    self.AddAction(First)
    self.AddAction(Last)
    self.AddAction(Home)
    self.AddAction(GotoMusic)
    self.AddAction(GotoPhotos)
    self.AddAction(GotoDVD)
    self.AddAction(GotoTV)
    self.AddAction(GotoVideo)
    self.AddAction(Show)
    self.AddAction(Teletext)
    self.AddAction(Red)
    self.AddAction(Green)
    self.AddAction(Yellow)
    self.AddAction(Blue)
    self.AddAction(Focus)



class Up(eg.ActionClass):

  def __call__(self):
    controlMeedio(1)



class Down(eg.ActionClass):

  def __call__(self):
    controlMeedio(2)



class Left(eg.ActionClass):

  def __call__(self):
    controlMeedio(3)



class Right(eg.ActionClass):

  def __call__(self):
    controlMeedio(4)



class Select(eg.ActionClass):

  def __call__(self):
    controlMeedio(5)



class Back(eg.ActionClass):

  def __call__(self):
    controlMeedio(6)



class ChannelUp(eg.ActionClass):

  def __call__(self):
    controlMeedio(7)



class ChannelDn(eg.ActionClass):

  def __call__(self):
    controlMeedio(8)



class Num0(eg.ActionClass):

  def __call__(self):
    controlMeedio(10)



class Num1(eg.ActionClass):

  def __call__(self):
    controlMeedio(11)



class Num2(eg.ActionClass):

  def __call__(self):
    controlMeedio(12)



class Num3(eg.ActionClass):

  def __call__(self):
    controlMeedio(13)



class Num4(eg.ActionClass):

  def __call__(self):
    controlMeedio(14)



class Num5(eg.ActionClass):

  def __call__(self):
    controlMeedio(15)



class Num6(eg.ActionClass):

  def __call__(self):
    controlMeedio(16)



class Num7(eg.ActionClass):

  def __call__(self):
    controlMeedio(17)



class Num8(eg.ActionClass):

  def __call__(self):
    controlMeedio(18)



class Num9(eg.ActionClass):

  def __call__(self):
    controlMeedio(19)



class Enter(eg.ActionClass):

  def __call__(self):
    controlMeedio(20)



class Play(eg.ActionClass):

  def __call__(self):
    controlMeedio(21)



class Pause(eg.ActionClass):

  def __call__(self):
    controlMeedio(22)



class Next(eg.ActionClass):

  def __call__(self):
    controlMeedio(23)



class Previous(eg.ActionClass):

  def __call__(self):
    controlMeedio(24)



class FFwd(eg.ActionClass):

  def __call__(self):
    controlMeedio(25)



class Rew(eg.ActionClass):

  def __call__(self):
    controlMeedio(26)



class Stop(eg.ActionClass):

  def __call__(self):
    controlMeedio(27)



class Record(eg.ActionClass):

  def __call__(self):
    controlMeedio(28)



class Display(eg.ActionClass):

  def __call__(self):
    controlMeedio(29)



class VolUp(eg.ActionClass):

  def __call__(self):
    controlMeedio(30)



class VolDn(eg.ActionClass):

  def __call__(self):
    controlMeedio(31)



class Mute(eg.ActionClass):

  def __call__(self):
    controlMeedio(32)



class PrevCh(eg.ActionClass):

  def __call__(self):
    controlMeedio(33)



class Guide(eg.ActionClass):

  def __call__(self):
    controlMeedio(34)



class Menu(eg.ActionClass):

  def __call__(self):
    controlMeedio(35)



class Info(eg.ActionClass):

  def __call__(self):
    controlMeedio(36)



class Exit(eg.ActionClass):

  def __call__(self):
    controlMeedio(37)



class Power(eg.ActionClass):

  def __call__(self):
    controlMeedio(38)



class Clear(eg.ActionClass):

  def __call__(self):
    controlMeedio(39)



class Top(eg.ActionClass):

  def __call__(self):
    controlMeedio(40)



class Bottom(eg.ActionClass):

  def __call__(self):
    controlMeedio(41)



class First(eg.ActionClass):

  def __call__(self):
    controlMeedio(42)



class Last(eg.ActionClass):

  def __call__(self):
    controlMeedio(43)



class Home(eg.ActionClass):

  def __call__(self):
    controlMeedio(44)



class Focus(eg.ActionClass):

  def __call__(self):
    controlMeedio(45)



class GotoMusic(eg.ActionClass):

  def __call__(self):
    controlMeedio(46)



class GotoPhotos(eg.ActionClass):

  def __call__(self):
    controlMeedio(47)



class GotoDVD(eg.ActionClass):

  def __call__(self):
    controlMeedio(48)



class GotoTV(eg.ActionClass):

  def __call__(self):
    controlMeedio(49)



class GotoVideo(eg.ActionClass):

  def __call__(self):
    controlMeedio(50)



class Show(eg.ActionClass):

  def __call__(self):
    controlMeedio(51)



class Teletext(eg.ActionClass):

  def __call__(self):
    controlMeedio(52)



class Red(eg.ActionClass):

  def __call__(self):
    controlMeedio(53)



class Green(eg.ActionClass):

  def __call__(self):
    controlMeedio(54)



class Yellow(eg.ActionClass):

  def __call__(self):
    controlMeedio(55)



class Blue(eg.ActionClass):

  def __call__(self):
    controlMeedio(56)

