import eg

eg.RegisterPlugin(
    name = "Meedio",
    author = "jorel1969",
    version = "0.0.1",
    kind = "program",
    description = (
        'Adds actions to control <a href="http://www.meedio.com/">Meedio</a>.'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wD/AP83WBt9"
        "AAACG0lEQVR42nVSTU8TURQ982aGaSnYgUYMVCB+BKlKIBpXJG5YYDSEuHCpG3+CJvwB"
        "l5q4g4XrSoykxugCjMYFkWqIbkxMDVJTPxA6nX4N05l58951QUEI9Wxu7k3OOTk3B8Lj"
        "TnrdX7bpMKpEnIhIitDJ5P3VChGh/OjzfHd08eI4Vel/KBesp4ljr8evivUGK3FXSln6"
        "tmo9fo9WIMjNB/OBqIReNWiE6sPns73dk5puiIaf6L9ETJAQisogIENBniA7tJc/9Y5N"
        "jt67bwxHFSICABv2nY8r7253Rk8BMEfPc172t6teeYMCOTH9CncJugJAaxqbiN0adJ8V"
        "/Phaz0i8ZmeNLr1jQOe+4/w4CoB0UrCPQExqqRhT9dNTiaHpvr0AuYVfTg6oQQHbuTSH"
        "IpnkMno8qUXU/YmD7fCEehNVkKADBIKgLa4wRLr0/YTKmgMA/VBU5aADU7WTMbSzw2+1"
        "OrJi2NtbdzNIIZzA+5nzykn7a90tBe6Wv/3bs77Uk4NQrQhkU7xJUKDSFgewvqhqbSpF"
        "IuS0hQFF4m0AYAEu0LGTVoR8pfZn6Y3wG8mpa9rZTuikqKxqVcy+hHS5ny0VXi7EB0bM"
        "KxeMVAxOJv+kpz1tGmuzH1oWSXLxduJ62jReDI05mTxrbG6GgThinkleTrXskqKxczdm"
        "ALAYAwDx3S/OZd2ljX+agogTFYnquyYkinPZcsGSJP4Cq6FlCpeS/scAAAAASUVORK5C"
        "YII="
    ),
)


import win32gui


# function for controlling meedio using SendMessage
def controlMeedio(inputVal):
    try:
      hMeedioWnd = win32gui.FindWindow('H2-WM-COMMAND', None)
      eg.result = win32gui.SendMessage(hMeedioWnd, 273, inputVal, 0)
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
    self.AddAction(Down)
    


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
    
