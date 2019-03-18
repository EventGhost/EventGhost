"""
speech recognition and voice synthesis module.

Please let me know if you like or use this module -- it would make my day!

speech.py: Copyright 2008 Michael Gundlach  (gundlach at gmail)
License: Apache 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

For this module to work, you'll need pywin32 (http://tinyurl.com/5ezco9
for Python 2.5 or http://tinyurl.com/5uzpox for Python 2.4) and
the Microsoft Speech kit (http://tinyurl.com/br8ysh).


Classes:
    Listener: represents a command to execute when phrases are heard.

Functions:
    say(phrase): Say the given phrase out loud.
    input(prompt, phraselist): Block until input heard, then return text.
    stoplistening(): Like calling stoplistening() on all Listeners.
    islistening(): True if any Listener is listening.
    listenforanything(callback): Run a callback when any text is heard.
    listenfor(phraselist, callback): Run a callback when certain text is heard.


Very simple usage example:

import speech

speech.say("Say something.")

print "You said " + speech.input()

def L1callback(phrase, listener):
    print phrase

def L2callback(phrase, listener):
    if phrase == "wow":
        listener.stoplistening()
    speech.say(phrase)

# callbacks are executed on a separate events thread.
L1 = speech.listenfor(["hello", "good bye"], L1callback)
L2 = speech.listenforanything(L2callback)

assert speech.islistening()
assert L2.islistening()

L1.stoplistening()
assert not L1.islistening()

speech.stoplistening()
"""

from win32com.client import constants as _constants
import win32com.client
import pythoncom
import time
import thread

# Make sure that we've got our COM wrappers generated.
from win32com.client import gencache
gencache.EnsureModule('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 0, 5, 0)

_voice = win32com.client.Dispatch("SAPI.SpVoice")
_recognizer = win32com.client.Dispatch("SAPI.SpInProcRecognizer")
_recognizer.AudioInputStream = win32com.client.Dispatch("SAPI.SpMMAudioIn")
_listeners = []
_handlerqueue = []
_eventthread=None

class Listener(object):

    """Listens for speech and calls a callback on a separate thread."""

    _all = set()

    def __init__(self, context, grammar, callback):
        """
        This should never be called directly; use speech.listenfor()
        and speech.listenforanything() to create Listener objects.
        """
        self._grammar = grammar
        Listener._all.add(self)

        # Tell event thread to create an event handler to call our callback
        # upon hearing speech events
        _handlerqueue.append((context, self, callback))
        _ensure_event_thread()

    def islistening(self):
        """True if this Listener is listening for speech."""
        return self in Listener._all

    def stoplistening(self):
        """Stop listening for speech.  Returns True if we were listening."""

        try:
            Listener._all.remove(self)
        except KeyError:
            return False

        # This removes all refs to _grammar so the event handler can die
        self._grammar = None

        if not Listener._all:
            global _eventthread
            _eventthread = None # Stop the eventthread if it exists

        return True

_ListenerBase = win32com.client.getevents("SAPI.SpInProcRecoContext")
class _ListenerCallback(_ListenerBase):

    """Created to fire events upon speech recognition.  Instances of this
    class automatically die when their listener loses a reference to
    its grammar.  TODO: we may need to call self.close() to release the
    COM object, and we should probably make goaway() a method of self
    instead of letting people do it for us.
    """

    def __init__(self, oobj, listener, callback):
        _ListenerBase.__init__(self, oobj)
        self._listener = listener
        self._callback = callback

    def OnRecognition(self, _1, _2, _3, Result):
        # When our listener stops listening, it's supposed to kill this
        # object.  But COM can be funky, and we may have to call close()
        # before the object will die.
        if self._listener and not self._listener.islistening():
            self.close()
            self._listener = None

        if self._callback and self._listener:
            newResult = win32com.client.Dispatch(Result)
            phrase = newResult.PhraseInfo.GetText()
            engineConfidence = 0
            actualConfidence = 0
            numWords = 0
            for elements in newResult.PhraseInfo.Elements:
                engineConfidence = engineConfidence + elements.EngineConfidence
                actualConfidence = actualConfidence + elements.ActualConfidence
                numWords = numWords + 1
            engineConfidence = engineConfidence / numWords
            actualConfidence = actualConfidence / numWords
            #print "'"+phrase +"' with engine conf="+str(engineConfidence)+" and actual conf="+str(actualConfidence)
            self._callback(phrase, self._listener,engineConfidence,actualConfidence)

def say(phrase):
    """Say the given phrase out loud."""
    _voice.Speak(phrase)


def input(prompt=None, phraselist=None):
    """
    Print the prompt if it is not None, then listen for a string in phraselist
    (or anything, if phraselist is None.)  Returns the string response that is
    heard.  Note that this will block the thread until a response is heard or
    Ctrl-C is pressed.
    """
    def response(phrase, listener):
        if not hasattr(listener, '_phrase'):
            listener._phrase = phrase # so outside caller can find it
        listener.stoplistening()

    if prompt:
        print prompt

    if phraselist:
        listener = listenfor(phraselist, response)
    else:
        listener = listenforanything(response)

    while listener.islistening():
        time.sleep(.1)

    return listener._phrase # hacky way to pass back a response...

def stoplistening():
    """
    Cause all Listeners to stop listening.  Returns True if at least one
    Listener was listening.
    """
    listeners = set(Listener._all) # clone so stoplistening can pop()
    returns = [l.stoplistening() for l in listeners]
    return any(returns) # was at least one listening?

def islistening():
    """True if any Listeners are listening."""
    return not not Listener._all

def listenforanything(callback):
    """
    When anything resembling English is heard, callback(spoken_text, listener)
    is executed.  Returns a Listener object.

    The first argument to callback will be the string of text heard.
    The second argument will be the same listener object returned by
    listenforanything().

    Execution takes place on a single thread shared by all listener callbacks.
    """
    return _startlistening(None, callback)

def listenfor(phraselist, callback):
    """
    If any of the phrases in the given list are heard,
    callback(spoken_text, listener) is executed.  Returns a Listener object.

    The first argument to callback will be the string of text heard.
    The second argument will be the same listener object returned by
    listenfor().

    Execution takes place on a single thread shared by all listener callbacks.
    """
    return _startlistening(phraselist, callback)

def _startlistening(phraselist, callback):
    """
    Starts listening in Command-and-Control mode if phraselist is
    not None, or dictation mode if phraselist is None.  When a phrase is
    heard, callback(phrase_text, listener) is executed.  Returns a
    Listener object.

    The first argument to callback will be the string of text heard.
    The second argument will be the same listener object returned by
    listenfor().

    Execution takes place on a single thread shared by all listener callbacks.
    """
    # Make a command-and-control grammar        
    context = _recognizer.CreateRecoContext()
    grammar = context.CreateGrammar()

    if phraselist:
        grammar.DictationSetState(0)
        # dunno why we pass the constants that we do here
        rule = grammar.Rules.Add("rule",
                _constants.SRATopLevel + _constants.SRADynamic, 0)
        rule.Clear()

        for phrase in phraselist:
            rule.InitialState.AddWordTransition(None, phrase)

        # not sure if this is needed - was here before but dupe is below
        grammar.Rules.Commit()

        # Commit the changes to the grammar
        grammar.CmdSetRuleState("rule", 1) # active
        grammar.Rules.Commit()
    else:
        grammar.DictationSetState(1)

    return Listener(context, grammar, callback)

def _ensure_event_thread():
    """
    Make sure the eventthread is running, which checks the handlerqueue
    for new eventhandlers to create, and runs the message pump.
    """
    global _eventthread
    if not _eventthread:
        def loop():
            while _eventthread:
                pythoncom.PumpWaitingMessages()
                if _handlerqueue:
                    (context,listener,callback) = _handlerqueue.pop()
                    # Just creating a _ListenerCallback object makes events
                    # fire till listener loses reference to its grammar object
                    _ListenerCallback(context, listener, callback)
                time.sleep(.5)
        _eventthread = 1 # so loop doesn't terminate immediately
        _eventthread = thread.start_new_thread(loop, ())