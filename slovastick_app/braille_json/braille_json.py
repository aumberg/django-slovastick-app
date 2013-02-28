# ~*~ coding: utf-8 ~*~

import json, os

theDir = os.path.abspath(os.path.dirname(__file__))
theFile = open(os.path.join(theDir, "braille.json"), "r")
braille_json = json.loads(theFile.read())
theFile.close()

def get(symbols, strWhat="", listWhere=[], canSomeMiss=True):
    """
        Return list with available information about symbols.
        Info returns in unicode and can be filtered by strWhat and listWhere.

        symbols: can pass by iterable object, where every element is a symbol
    """

    result = []
    whereSymbol = braille_json

    if listWhere :
        for key in listWhere :
            if key not in whereSymbol :
                if canSomeMiss :
                    return []
                else :
                    return False

            whereSymbol = whereSymbol[key]

    if isinstance(symbols, str) :
        symbols = list(symbols.decode('utf8'))
    elif not isinstance(symbols, unicode) :
        uniList = []

        for symbol in symbols :
            if isinstance(symbol, str) :
                uniList.append(symbol.decode('utf8'))
            else :
                uniList.append(symbol)

        symbols = uniList
    # 
    for symbol in symbols :
        # all symbols are lowercase
        symbol = symbol.lower()
        # 
        if symbol in whereSymbol :
            finded = dict(whereSymbol[symbol])
            # union global info with local symbol info
            if u"info" in finded :
                finded.update(finded.pop(u"info"))
            # 
            if strWhat :
                if strWhat in finded :
                    result.append(finded[strWhat])
                elif canSomeMiss :
                    continue
                else :
                    return False
            else :
                result.append(finded)
        elif canSomeMiss :
            continue
        else :
            return False

    return result

def _init_addition_():
    result = dict(braille_json)

    groups = {
        u"language": [u"en", u"ru"],
        u"articulatoryPhonetics": [u"consonant", u"vowel"]
    }

    def get_by_path(path):
        parentObj = result
        key = path[-1:][0]

        for k in path[:-1] :
            parentObj = parentObj[k]

        return parentObj, key

    def add_info(path):
        pObj, key   = get_by_path(path)
        braille     = pObj[key]
        obj         = pObj[key] = {}
        obj[u"path"] = path
        obj[u"self"] = key

        # but what do with complex symbols?
        if braille in result[u"braille"] :
            info = result[u"braille"][braille][u"info"]
            info[u"relations"].append(path)
            obj[u"info"] = info

        for key in path :
            for group in groups :
                if key in groups[group] :
                    obj[group] = key

        # save to global object
        result[key] = obj

    def recursive_search(where, path=[]):
        for key in where :
            if isinstance(where[key], unicode) :
                path2 = list(path)
                path2.append(key)
                add_info(path2)
            elif isinstance(where[key], dict) :
                path2 = list(path)
                path2.append(key)
                recursive_search(where[key], path2)

    def get_dots(i):
        result = u""
        digit = 1

        for j in bin(i)[::-1] :
            if '1' == j:
                result = result + unicode(digit)

            digit = digit + 1

        return result
    # create dict braille and save to global object
    temp = {}
    index = -1

    for braille in result[u"braille"] :
        index = index + 1
        # info key is a global information for all related symbols
        temp[braille] = {
            u"info" : {u"braille":braille, u"relations": []},
            u"path" : [u"braille", braille],
            u"index": index,
            u"self" : braille,
        }
    #
    result[u"braille"] = temp
    # save to global object
    result.update(temp)
    # add dots
    for braille in result[u"braille"] :
        obj  = result[u"braille"][braille]
        dots = get_dots(obj[u"index"])
        path = [u"dots", dots]

        obj[u"info"][u"dots"] = dots
        obj[u"info"][u"relations"].append(path)
        result[u"dots"][dots] = {
            u"info": obj[u"info"],
            u"path": path,
            u"self": dots
        }
    # add symbols
    recursive_search(result[u"symbols"], path=[u"symbols"])
    # delete some descriptions
    # for key in result :
    #     if isinstance(result[key], list) :
    #         del result[key]
    for key, value in result.items():
        if isinstance(value, list) :
            result.pop(key)

    return result

braille_json = _init_addition_()

# import pprint
# print
# print "1. Test one: "
# print
# pprint.pprint(get("d"))
# print
# print "2. Test two: "
# print
# pprint.pprint(get("Hello Мир", "dots"))
# print
# print "3. Test tree (must return False): "
# print
# pprint.pprint(get("G", listWhere=[u"symbols", "r"], canSomeMiss=False))