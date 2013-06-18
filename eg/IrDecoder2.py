
def MakeTimeRange(tvalue):
    return int(round((tvalue * 0.66))), int(round((tvalue * 1.33)))

def MakeTime(tvalue):
    return int(round(tvalue))



SHARP_TIME = 320
SHARP_PULSE_RANGE   = MakeTimeRange(SHARP_TIME)
SHARP_SPACE0_RANGE  = MakeTimeRange(2 * SHARP_TIME)
SHARP_SPACE1_RANGE  = MakeTimeRange(5 * SHARP_TIME)
SHARP_THRESHOLD     = MakeTime(3.5 * SHARP_TIME)


def InRange(value, rangeTuple):
    if value >= rangeTuple[0] and value <= rangeTuple[1]:
        return True
    else:
        return False
    
    
def ShiftInBits(data, start, end, threshold):
    buffer = 0
    for i in xrange(start, end + 1, 2):
        buffer <<= 1
        if data[i] >= threshold:
            buffer |= 1
    return buffer
            
            
def ShiftInBitsReverse(data, start, end, threshold):
    buffer = 0
    for i in xrange(end - 1, start - 1, -2):
        buffer <<= 1
        if data[i] >= threshold:
            buffer |= 1
    return buffer
            
            
def Rc5Decode(data, start, end, threshold):
    state = 0
    buffer = 1L
    length = 0
    for i in xrange(start, end):
        value = data[i]
        if state == 0: # Mid1
            if value < threshold:
                state = 1
            else:
                state = 2
                buffer <<= 1
                length += 1
        elif state == 1: # Start1
            if value < threshold:
                state = 0
                buffer <<= 1
                buffer |= 1
                length += 1
            else:
                return None
        elif state == 2: # Mid0
            if value < threshold:
                state = 3
            else:
                state = 0
                buffer <<= 1
                buffer |= 1
                length += 1
        else: # Start0
            if value < threshold:
                state = 2
                buffer <<= 1
                length += 1
            else:
                return None
    return buffer
                
            
import threading
import thread
import collections

class IrDecoder2:
    
    def __init__(self, sampleTime, plugin):
        self.sampleTime = sampleTime
        self.plugin = plugin
        self.buffer = collections.deque()
        self.event = threading.Event()
        self.shouldStop = False
        self.thread = threading.Thread(target=self.Thread)
        self.thread.start()
        
        SHARP_TIME = 320  # 320 micro-seconds
        self.SHARP_PULSE_MIN   = self.MakeMinTime(SHARP_TIME)
        self.SHARP_PULSE_MAX   = self.MakeMaxTime(SHARP_TIME)
        self.SHARP_SPACE0_MIN  = self.MakeMinTime(2 * SHARP_TIME)
        self.SHARP_SPACE0_MAX  = self.MakeMaxTime(2 * SHARP_TIME)
        self.SHARP_SPACE1_MIN  = self.MakeMinTime(5 * SHARP_TIME)
        self.SHARP_SPACE1_MAX  = self.MakeMaxTime(5 * SHARP_TIME)
        self.SHARP_THRESHOLD   = self.MakeTime(3.5 * SHARP_TIME)
        
        SIRC_TIME = 600   # 600 micro-seconds
        self.SIRC_PREPULSE_MIN = self.MakeMinTime(4 * SIRC_TIME)
        self.SIRC_PREPULSE_MAX = self.MakeMaxTime(4 * SIRC_TIME)
        self.SIRC_SPACE_MIN    = self.MakeMinTime(SIRC_TIME)
        self.SIRC_SPACE_MAX    = self.MakeMaxTime(SIRC_TIME)
        self.SIRC_PULSE0_MIN   = self.MakeMinTime(SIRC_TIME)
        self.SIRC_PULSE0_MAX   = self.MakeMaxTime(SIRC_TIME)
        self.SIRC_PULSE1_MIN   = self.MakeMinTime(2 * SIRC_TIME)
        self.SIRC_PULSE1_MAX   = self.MakeMaxTime(2 * SIRC_TIME)
        self.SIRC_THRESHOLD    = self.MakeTime(1.5 * SIRC_TIME)

        RC5_TIME = 889    # 889 micro-seconds
        self.RC5_PULSE_MIN	   = self.MakeMinTime(RC5_TIME)
        self.RC5_PULSE_MAX	   = self.MakeMaxTime(RC5_TIME * 2.0)
        self.RC5_SPACE_MIN	   = self.MakeMinTime(RC5_TIME)
        self.RC5_SPACE_MAX	   = self.MakeMaxTime(RC5_TIME * 2.0)
        self.RC5_THRESHOLD	   = self.MakeTime(RC5_TIME * 1.50)
        self.suppressRc5ToggleBit = True


    def MakeMinTime(self, tvalue):
        return int(round((tvalue * 0.66) - 2))


    def MakeMaxTime(self, tvalue):
        return int(round((tvalue * 1.33) + 2))


    def MakeTime(self, tvalue):
        return int(round(tvalue))
    
    
    def Decode(self, data):
        self.buffer.append(data)
        self.event.set()
            
            
    def Stop(self):
        self.shouldStop = True
        self.event.set()
        
        
    def Thread(self):
        buffer = []
        shouldIgnore = False
        while not self.shouldStop:
            self.event.wait()
            
            self.event.clear()
            while(len(self.buffer)):
                value = self.buffer.popleft()
                if not shouldIgnore:
                    buffer.append(value)
                else:
                    shouldIgnore = False
                if value > 20000:
                    result = self.TestBuffer(buffer, len(buffer)-1)
                    if result is not None:
                        self.plugin.TriggerEvent(result)
                    buffer = []
            self.event.wait(0.05)
            if not self.event.isSet():
                buffer.append(200000)
                result = self.TestBuffer(buffer, len(buffer)-1)
                if result is not None:
                    self.plugin.TriggerEvent(result)
                shouldIgnore = True
                buffer = []
             
        
    def TestBuffer(self, data, dataLen):
#        for i, value in enumerate(data):
#            if i % 2:
#                print "L" + str(value) + ",",
#            else:
#                print "H" + str(value) + ",",
#        print
        if dataLen < 8:
            return None
        min_high = 100000
        min_low = 100000
        max_high = 0
        max_low = 0
        lows = []
        highs = []
        for i in xrange(2, dataLen):
            value = data[i]
            if i % 2:
                lows.append(value)
                if value > max_low:
                    max_low = value
                if value < min_low:
                    min_low = value
            else:
                highs.append(value)
                if value > max_high:
                    max_high = value
                if value < min_high:
                    min_high = value
                    
        lows.sort()
        highs.sort()
        max_high = max(highs[1:-1])
        min_high = min(highs[1:-1])
        max_low = max(lows[1:-1])
        min_low = min(lows[1:-1])
        
        prePulse = data[0]
        preSpace = data[1]
        
        if (
            dataLen == 31 and
            prePulse >= self.SHARP_PULSE_MIN and 
            prePulse <= self.SHARP_PULSE_MAX and 
            preSpace >= self.SHARP_SPACE0_MIN and 
            preSpace <= self.SHARP_SPACE1_MAX and 
            min_high >= self.SHARP_PULSE_MIN and 
            max_high <= self.SHARP_PULSE_MAX and 
            min_low >= self.SHARP_SPACE0_MIN and 
            max_low <= self.SHARP_SPACE1_MAX
            ):
                code = ShiftInBits(data, 1, 30, self.SHARP_THRESHOLD)
                if (code & 256):
                    code ^= 0x03ff
                return "Sharp_%0.4X" % code
            
        if (
            prePulse >= self.SIRC_PREPULSE_MIN and 
            prePulse <= self.SIRC_PREPULSE_MAX and 
            (
                (dataLen == 25) or 
                (dataLen == 31) or 
                (dataLen == 41)
            ) and 
            min_high >= self.SIRC_PULSE0_MIN and 
            max_high <= self.SIRC_PULSE1_MAX and 
            min_low >= self.SIRC_SPACE_MIN and 
            max_low <= self.SIRC_SPACE_MAX and 
            preSpace >= self.SIRC_SPACE_MIN and 
            preSpace <= self.SIRC_SPACE_MAX
        ):
            code = ShiftInBitsReverse(data, 2, dataLen, self.SIRC_THRESHOLD)
            return "SIRC%d_%0.4X" % (dataLen / 2, code)
            
        if (
            prePulse >= self.RC5_PULSE_MIN and 
            prePulse <= self.RC5_PULSE_MAX and 
            preSpace >= self.RC5_SPACE_MIN and 
            preSpace <= self.RC5_SPACE_MAX and 
            min_high >= self.RC5_PULSE_MIN and 
            max_high <= self.RC5_PULSE_MAX and 
            min_low >= self.RC5_SPACE_MIN and 
            max_low <= self.RC5_SPACE_MAX
        ):
            code = Rc5Decode(data, 0, dataLen, self.RC5_THRESHOLD)
            if code is not None:
                if self.suppressRc5ToggleBit:
                    code &= 0xF7FF
                return "RC5_%0.4X" % code

        level_high = (min_high + max_high) / 2
        level_low = (min_low + max_low) / 2
        if (max_high - min_high) < 0.4 * min_high:
            level_high += 0.25 * min_high
        if (max_low - min_low) < 0.4 * min_low:
            level_low += 0.25 * min_low
            
        code = 3L
        for i in xrange(0, dataLen):
            value = data[i]
            code = code << 1
            if i % 2:
                if value > level_low:
                    code |= 1
            else:
                if value > level_high:
                    code |= 1
        return "U%X" % code
