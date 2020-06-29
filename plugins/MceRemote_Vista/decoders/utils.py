
def clean_code(ir_code, threshold):
    low_threshold = 1.0 - (threshold / 100.0)
    high_threshold = 1.0 + (threshold / 100.0)
    marks = []
    spaces = []
    cleaned_code = []

    for timing in ir_code:
        if timing < 0:
            for space in spaces:
                avg = sum(space) / len(space)

                low = int(avg * high_threshold)
                high = int(avg * low_threshold)
                if low <= timing <= high:
                    space += [timing]
                    break
            else:
                spaces += [[timing]]
        else:
            for mark in marks:
                avg = sum(mark) / len(mark)

                high = int(avg * high_threshold)
                low = int(avg * low_threshold)

                if low <= timing <= high:
                    mark += [timing]
                    break
            else:
                marks += [[timing]]
                
    marks2 = []
    spaces2 = []

    # double check the groups for any possible straglers
    while marks:
        mark = marks.pop(0)
        avg_mark = sum(mark) / len(mark)
        for m in marks:
            avg = sum(m) / len(m)
            high = int(avg * high_threshold)
            low = int(avg * low_threshold)
            if low <= avg_mark <= high:
                m.extend(mark[:])
                break
        else:
            for m in marks2:
                avg = sum(m) / len(m)
                high = int(avg * high_threshold)
                low = int(avg * low_threshold)

                if low <= avg_mark <= high:

                    m.extend(mark[:])
                    break
            else:
                marks2 += [mark[:]]

    while spaces:
        space = spaces.pop(0)
        avg_space = sum(space) / len(space)
        for s in spaces:
            avg = sum(s) / len(s)
            high = int(avg * high_threshold)
            low = int(avg * low_threshold)

            if low <= avg_space <= high:
                s.extend(space[:])
                break
        else:
            for s in spaces2:
                avg = sum(s) / len(s)
                high = int(avg * high_threshold)
                low = int(avg * low_threshold)

                if low <= avg_space <= high:
                    s.extend(space[:])
                    break
            else:
                spaces2 += [space[:]]

    del marks[:]
    del spaces[:]

    # normalize the marks and spaces to a 50us tolerance
    for mark in marks2:
        mark = sum(mark) / len(mark)

        dif = mark % 50

        # print dif, mark
        if dif < 25:
            dif = -dif
        else:
            dif = 50 - dif

        mark += dif
        marks += [mark]

    for space in spaces2:
        space = sum(space) / len(space)

        dif = space % 50

        if dif > 25:
            dif = 50 - dif
        else:
            dif = -dif

        space += dif
        spaces += [space]

    for timing in ir_code:
        for mark in marks:
            low = int(mark * low_threshold)
            high = int(mark * high_threshold)
            if low <= timing <= high:
                cleaned_code += [mark]
                break
        else:
            for space in spaces:
                high = int(space * low_threshold)
                low = int(space * high_threshold)
                if low <= timing <= high:
                    cleaned_code += [space]
                    break
            else:
                cleaned_code += [timing]

    return cleaned_code
