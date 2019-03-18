import eg

eg.RegisterPlugin(
    name="VoiceRecognition",
    guid='{D7D26E66-0EC6-447C-8404-6C49C9FE0C8F}',
    author="wacind",
    version="0.0.1",
    kind="other",
    description="Uses built in speech recognition of windows 7 to convert words to events.",

)

import speech
import time
from threading import Event, Thread
import wx

WORDS1 = 'roger,notepad,command,system,help,lock,shutdown,reboot,cancel,save'
WORDS2 = 'roger play movie,roger stop movie,roger start notepad'
FILLER = "again,best,cat,drain,edge,foreign,great,how,imagine,jump,kite,lamp,man,naught,order,quick,reboot,sole,ten,uncle,velocity,yellow,Are you okay,Be careful,Do you feel better,everyday,follow me,Give me a call,Have a good trip,I Don't Care,Just a little,Let's go,My son,No Problem,over here,Please sit down,Right here,See you later,Thank you,Very good,What are you doing,yes you look tired"


class VoiceRecognition(eg.PluginBase):
    counter = 0

    def __init__(self):
        self.AddEvents()
        self.AddAction(Speaker)

    def __start__(self, words1, level1, words2, level2, fillerWords, logging):
        fillerWordList = fillerWords.split(',')
        wordList1 = words1.split(',')
        wordList2 = words2.split(',')
        self.wordList = fillerWordList + wordList1 + wordList2

        if logging:
            for word in self.wordList:
                print word

        def followUp(plugin):
            Event().wait(3)
            plugin.counter -= 1
            if plugin.counter <= 0:
                plugin.TriggerEvent("DIE")
                plugin.counter = 0

        def callback(phrase, listener, engineConfidence, actualConfidence):
            self.counter += 1
            if phrase in wordList1:
                if engineConfidence * 100 >= level1 and actualConfidence >= 0:
                    print phrase + " " + str(engineConfidence * 100)
                    self.TriggerEvent(phrase)
                else:
                    if logging:
                        print phrase + " " + str(engineConfidence * 100)
            elif phrase in wordList2:
                if engineConfidence * 100 >= level2 and actualConfidence >= 0:
                    print phrase + " " + str(engineConfidence * 100)
                    self.TriggerEvent(phrase)
                else:
                    if logging:
                        print phrase + " " + str(engineConfidence * 100)
            Thread(target=followUp, args=(self,)).start()

        speech.listenfor(self.wordList, callback)

    def __stop__(self):
        speech.stoplistening()

    def Configure(self, words1=WORDS1, level1=90, words2=WORDS2, level2=80, fillerWords=FILLER, logging=False):
        panel = eg.ConfigPanel()
        conf1Ctrl = panel.TextCtrl(words1)
        level1Ctrl = panel.SpinIntCtrl(level1, max=100)
        conf2Ctrl = panel.TextCtrl(words2)
        level2Ctrl = panel.SpinIntCtrl(level2, max=100)
        label1Field = wx.StaticText(panel, -1, 'Word Group 1:')
        label2Field = wx.StaticText(panel, -1, 'Word Group 1 Confidence:')
        panel.sizer.Add(label1Field)
        panel.sizer.Add(conf1Ctrl, 0, wx.EXPAND)
        panel.sizer.Add(label2Field)
        panel.sizer.Add(level1Ctrl)
        blank = wx.StaticText(panel, -1, '       ')
        panel.sizer.Add(blank)
        label3Field = wx.StaticText(panel, -1, 'Word Group 2:')
        label4Field = wx.StaticText(panel, -1, 'Word Group 2 Confidence:')
        panel.sizer.Add(label3Field)
        panel.sizer.Add(conf2Ctrl, 0, wx.EXPAND)
        panel.sizer.Add(label4Field)
        panel.sizer.Add(level2Ctrl)
        blank2 = wx.StaticText(panel, -1, '       ')
        panel.sizer.Add(blank2)
        fillerCtrl = panel.TextCtrl(fillerWords)
        label5Field = wx.StaticText(panel, -1, 'Filler Words:')
        panel.sizer.Add(label5Field)
        panel.sizer.Add(fillerCtrl, 0, wx.EXPAND)
        blank3 = wx.StaticText(panel, -1, '       ')
        panel.sizer.Add(blank3)
        check1Box = panel.CheckBox(logging, " Enable extra logging")
        panel.sizer.Add(check1Box)
        while panel.Affirmed():
            panel.SetResult(
                conf1Ctrl.GetValue(),
                level1Ctrl.GetValue(),
                conf2Ctrl.GetValue(),
                level2Ctrl.GetValue(),
                fillerCtrl.GetValue(),
                check1Box.GetValue(),
            )


class Speaker(eg.ActionBase):

    def __call__(self, word):
        speech.say(word)

    def Configure(self, word=""):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, word)
        panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
