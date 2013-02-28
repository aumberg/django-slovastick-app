note = {
    "C2": "65.406391",
    "D2": "73.416192",
    "E2": "82.406889",
    "F2": "87.307058",
    "G2": "97.998859",
    "A2": "110.000000",
    "B2": "123.470905",
    "C3": "130.812783",
    "D3": "146.832384",
    "E3": "164.813778",
    "F3": "174.614116",
    "G3": "195.997718",
    "A3": "220.000000",
    "B3": "246.941811",
    "C4": "261.625565",
    "D4": "293.664768",
    "E4": "329.627557",
    "F4": "349.228231",
    "G4": "391.995436",
    "A4": "440.000000",
    "B4": "493.883621",
    "C5": "523.251131",
    "D5": "587.329536",
    "E5": "659.255114",
    "F5": "698.456463",
    "G5": "783.990872",
    "A5": "880.000000",
    "B5": "987.767243",
    "C6": "1046.502261",
    "D6": "1174.659072",
    "E6": "1318.510228",
    "F6": "1396.912926",
    "G6": "1567.981744",
    "A6": "1760.000000",
    "B6": "1975.534485",
    "C7": "2093.004522",
    "D7": "2349.318143",
    "E7": "2637.020455",
    "F7": "2793.825851",
    "G7": "3135.963488",
    "A7": "3520.000000",
    "B7": "3951.068970",
    "C8": "4186.009045",
    "D8": "4698.636287",
    "E8": "5274.040911",
    "F8": "5587.651703",
    "G8": "6271.926976",
    "A8": "7040.000000",
    "B8": "7902.137940",
}


dots_standart = {
    "insPrefix":"1",

    "iInsName" :"1",

    # start time
    "iStart": 0,

    "startAppend": {
        "1": 0,
        "2": 0.05,
        "3": 0.1,
        "4": 0.005,
        "5": 0.055,
        "6": 0.105,
        "7": 0.15,
        "8": 0.155
    },      
    # 
    "iDur": {
        "1": 0.15,
        "2": 0.2,
        "3": 0.25,
        "4": 0.16,
        "5": 0.21,
        "6": 0.26,
        "7": 0.3,
        "8": 0.31
    },

    "iFreq": {
        "1": note["F4"],
        "2": note["A4"],
        "3": note["C5"],
        "4": note["C6"],
        "5": note["E6"],
        "6": note["G6"],
        "7": note["D4"],
        "8": note["B6"] 
    },

    "iPan": {
        "1": 0.3,
        "2": 0.2,
        "3": 0.1,
        "4": 0.7,
        "5": 0.8,
        "6": 0.9,
        "7": 0,
        "8": 1  
    },

    "iVol": {
        "1": 0.9,
        "2": 0.7,
        "3": 0.4,
        "4": 0.9,
        "5": 0.7,
        "6": 0.4,
        "7": 0.3,
        "8": 0.3     
    },

    "addition": ""
}


"""
     predefined values:

    iInsFullName    = p1
    iStart          = p2
    iDur            = p3
    iFreq           = p4
    iPan            = p5   
    iVol            = p6

    ;addition:

    ;---
"""

dots_standart_template = "i %(insPrefix)s%(iInsName)s %(iStart)s %(iDur)s " + \
    "%(iFreq)s %(iPan)s %(iVol)s %(addition)s\n "

def get_score_standart(info, settings={}):
    if "dots" not in info :
        return ""

    dots    = info["dots"]
    result  = ";--- dots - %s\n" % dots
    st      = dict(dots_standart)
    st.update(settings)

    for dot in dots :
        values = {}

        for key in dots_standart :
            if isinstance(st[key], dict) :
                values[key] = st[key][dot]
            else :
                values[key] = st[key]

        values["iStart"] = values["iStart"] + values["startAppend"]

        result = result + dots_standart_template % values

    return result