# Text debugger
import string


def exactSearch(query, db):
    out = []
    for data in db:
        if query in data:
            out.append(data)
    return out


def charAt(ch, text, start=0):
    # text.index(ch), but it raise exception
    for i in range(start, len(text)):
        if ch in text[i]:
            return i
    return -1


def charsAt(chars, text):
    out = []
    firstChar = charAt(chars[0], text)
    out.append(firstChar)
    for i in range(1, len(chars)):
        max_out = max(out)
        out.append(charAt(chars[i], text, max_out))
    return out


def isAllNumber(text):
    for ch in text:
        if ch in string.digits + '. ':
            pass
        else:
            return False
    return True
