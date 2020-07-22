from struct import unpack_from, unpack, pack

prontoClock = 0.241246
SignalFree = 10000
SignalFreeRC6 = 2700
RC6Start = [2700, -900, 450, -900, 450, -450, 450, -450, 450, -450]
RC6AStart = [3150, -900, 450, -450, 450, -450, 450, -900, 450]

def ConvertIrCodeToProntoRaw(freq,data):
    if freq <= 0:
        freq = 36000

    prontoCarrier = int(1000000/(freq*prontoClock))
    carrier = prontoCarrier * prontoClock

    prontoData = [0x0000, prontoCarrier, 0x0000, 0x0000]
    for val in data:
        duration = abs(val)
        prontoData.append(round(duration / carrier))

    if len(prontoData) % 2 != 0:
        prontoData.append(SignalFree)

    prontoData[3] = ( len(prontoData)-4 )/ 2
    out = '%04X'%int(prontoData[0])
    for v in prontoData[1:]:
        out = out + ' %04X'%int(v)
    return out

def ConvertProntoRawToIrCode(prontoData,nRepeat): #nRepeat is ignored for Raw
    if len(prontoData) < 6 or not (prontoData[0] == 0x0000 or prontoData[0] == 0x0100): #Raw or Learned
        raise Exception("Invalid Raw data %s"%str(prontoData))
    prontoCarrier = prontoData[1];
    if prontoCarrier == 0:
        prontoCarrier = int(1000000/(36000 * prontoClock))
    pw = prontoCarrier*prontoClock
    firstSeq = 2*prontoData[2]
    repeatSeq = 2*prontoData[3]
    pulse = True
    repeatCount = 0
    start = 4
    done = False
    index = start
    sequence = firstSeq
    if firstSeq == 0:
        if repeatSeq == 0:
            return None
        sequence = repeatSeq
        repeatCount = 1
    timingData = []
    while not done:
        time = (int) (prontoData[index] * pw)
        if pulse:
            timingData.append(time)
        else:
            timingData.append(-time)
        index = index + 1
        pulse = not pulse

        if index == start + sequence:
            if repeatCount == 0:
                if repeatSeq != 0:
                    start += firstSeq
                    sequence = repeatSeq
                    index = start
                    pulse = True
                    repeatCount += 1
                else:
                    done = True
            elif repeatCount == 1:
                done = True
            else:
                index = start
                pulse = True
                repeatCount += 1
    freq = int(1000000/(prontoCarrier*prontoClock))
    return (freq,timingData)

def EncodeBits(data,start,stop,s_false,s_true):
    out = ""
    for i in range(start,stop-1,-1):
        if data & (1 << i) > 0:
            out = out + s_true
        else:
            out = out + s_false
    return out

def ZeroOneSequences(String, Delay):
    finalData = []
    ind = 0
    n = len(String)
    while True:
        countUp = 0
        countDown = 0
        while  ind < n and String[ind] == "0":
            ind += 1
        while ind < n and String[ind] == "1":
            countUp += 1
            ind += 1
        while ind < n and String[ind] == "0":
            countDown += 1
            ind += 1
        finalData.extend([Delay*countUp,-Delay*countDown])
        if ind >= n:
            break
    if finalData[-1] == 0:
        finalData[-1] = -10000
    else:
        finalData[-1] -= 10000
    return finalData

def ConvertProntoRC5ToIrCode(prontoData, nRepeat = 0):
    if len(prontoData) != 6 or prontoData[0] != 0x5000: #CodeType RC5
        raise Exception("Invalid RC5 data %s"%str(prontoData))

    prontoCarrier = prontoData[1]
    if prontoCarrier == 0x0000:
        prontoCarrier = int(1000000/(36000*prontoClock))

    RC5String = ''

    for j in range(nRepeat+1):
        toggle = nRepeat % 2 == 0
        if prontoData[5] > 63:
            RC5String = RC5String + EncodeBits(2, 1, 0, '10', '01')
        else:
            RC5String = RC5String + EncodeBits(3, 1, 0, '10', '01')
        if toggle:
            RC5String = RC5String + EncodeBits(1, 0, 0, '10', '01')
        else:
            RC5String = RC5String + EncodeBits(0, 0, 0, '10', '01')
        RC5String = RC5String + EncodeBits(prontoData[4], 4, 0, '10', '01')
        RC5String = RC5String + EncodeBits(prontoData[5], 5, 0, '10', '01')

    finalData = ZeroOneSequences(RC5String, 900)

    freq = int(1000000/(prontoCarrier*prontoClock))
    return freq,finalData

def ConvertProntoRC5XToIrCode(prontoData,nRepeat):
    if not (len(prontoData) == 7 or (len(prontoData) == 8 and prontoData[7] == 0x0000)) or prontoData[0] != 0x5001: #CodeType RC5X
        raise Exception("Invalid RC5X data %s"%str(prontoData))

    prontoCarrier = prontoData[1]
    if prontoCarrier == 0x0000:
        prontoCarrier = int(1000000/(36000*prontoClock))

    if prontoData[2] + prontoData[3] != 2:
        raise Exception("Invalid RC5X data %s"%str(prontoData))

    RC5XString = ''

    for j in range(nRepeat+1):
        toggle = nRepeat % 2 == 0
        if prontoData[5] > 63:
            RC5XString = RC5XString + EncodeBits(2, 1, 0, '10', '01')
        else:
            RC5XString = RC5XString + EncodeBits(3, 1, 0, '10', '01')
        if toggle:
            RC5XString = RC5XString + EncodeBits(1, 0, 0, '10', '01')
        else:
            RC5XString = RC5XString + EncodeBits(0, 0, 0, '10', '01')
        RC5XString = RC5XString + EncodeBits(prontoData[4], 4, 0, '10', '01')
        RC5XString = RC5XString + '0000'
        RC5XString = RC5XString + EncodeBits(prontoData[5], 5, 0, '10', '01')
        RC5XString = RC5XString + EncodeBits(prontoData[6], 5, 0, '10', '01')

    finalData = ZeroOneSequences(RC5XString, 900)

    freq = int(1000000/(prontoCarrier*prontoClock))
    return freq,finalData

def ConvertProntoRC6ToIrCode(prontoData, nRepeat):
    if len(prontoData) != 6 or prontoData[0] != 0x6000: # CodeType RC6
        raise Exception("Invalid RC6 data %s"%str(prontoData))

    prontoCarrier = prontoData[1]
    if prontoCarrier == 0x0000:
        prontoCarrier = int(1000000/(36000*prontoClock))

    if prontoData[2] + prontoData[3] != 1:
        raise Exception("Invalid RC6 data %s"%str(prontoData))

    RC6String = ""
    for j in range(nRepeat+1):
        toggle = nRepeat % 2 == 0
        RC6String = RC6String + '1111110010010101'
        if toggle:
            RC6String = RC6String + '1100'
        else:
            RC6String = RC6String + '0011'
        RC6String = RC6String + EncodeBits(prontoData[4], 7, 0, '01', '10')
        RC6String = RC6String + EncodeBits(prontoData[5], 7, 0, '01', '10')

    finalData = ZeroOneSequences(RC6String, 450)

    freq = int(1000000/(prontoCarrier*prontoClock))
    return freq,finalData

def ConvertProntoRC6AToIrCode(prontoData, nRepeat):
    if len(prontoData) != 8 or prontoData[0] != 0x6001: # CodeType RC6A
        raise Exception("Invalid RC6A data %s"%str(prontoData))

    prontoCarrier = prontoData[1]
    if prontoCarrier == 0x0000:
        prontoCarrier = int(1000000/(36000*prontoClock))

    if prontoData[2] + prontoData[3] != 2:
        raise Exception("Invalid RC6A data %s"%str(prontoData))

    RC6AString = ""
    for j in range(nRepeat+1):
        toggle = nRepeat % 2 == 0
        RC6AString = RC6AString + '11111110010101001'
        if toggle:
            RC6AString = RC6AString + '1100'
        else:
            RC6AString = RC6AString + '0011'
        if prontoData[4] > 127:
            RC6AString = RC6AString + EncodeBits(1, 0, 0, '01', '10')
            RC6AString = RC6AString + EncodeBits(prontoData[4], 14, 0, '01', '10')
        else:
            RC6AString = RC6AString + EncodeBits(0, 0, 0, '01', '10')
            RC6AString = RC6AString + EncodeBits(prontoData[4], 6, 0, '01', '10')
        RC6AString = RC6AString + EncodeBits(prontoData[5], 7, 0, '01', '10')
        RC6AString = RC6AString + EncodeBits(prontoData[6], 7, 0, '01', '10')

    finalData = ZeroOneSequences(RC6AString, 450)

    freq = int(1000000/(prontoCarrier*prontoClock))
    return freq,finalData

prontoHandlers = { "0000" : ConvertProntoRawToIrCode,
                   "0100" : ConvertProntoRawToIrCode,
                   "5000" : ConvertProntoRC5ToIrCode,
                   "5001" : ConvertProntoRC5XToIrCode,
                   "6000" : ConvertProntoRC6ToIrCode,
                   "6001" : ConvertProntoRC6AToIrCode,
                 }

def Pronto2MceTimings(pronto,nRepeat = 0):
    vals = pronto.split(" ")
    try:
        myFunc = prontoHandlers[vals[0]]
    except:
        raise Exception("Don't have a decoder for pronto format %s"%vals[0])
        return
    prontoData = []
    for v in vals:
        prontoData.append(int(v,16))
    freq, timings = myFunc(prontoData,nRepeat)
    try:
        freq, timings = myFunc(prontoData,nRepeat)
    except Exception, exc:
        raise exc
    return freq, timings
