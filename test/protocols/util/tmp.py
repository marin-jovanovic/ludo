def bracketed_split(string):
    # match first left bracket with matching right bracket
    # header is prefix that starts with left bracket and starts at position 0

    # no header
    if not string.__contains__("{"):
        return 0, "", string

    depth = 0
    for i, c in enumerate(string):
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1

        if depth == 0:
            return 0, string[1:i], string[i+1:]

    if depth != 0:
        return -1, "", ""


if __name__ == '__main__':

    t = bracketed_split("{p: {a:b, c:d}, f:g}fjrfjfjejw")
    print(t)

    t = bracketed_split("f f dddd dddd")
    print(t)

    t = bracketed_split("asdfg")
    print(t)

    # err
    print(bracketed_split("{{h}abc"))

    print(bracketed_split("{{h}}}abc"))

    print(bracketed_split("}}}abc"))

    print(bracketed_split("h}}}abc"))

    print(bracketed_split("{h}"))

    print(bracketed_split("{h}{a}{b}"))

    print(bracketed_split("aaa{h}abc"))
    print(bracketed_split("aaa{{h}abc"))
    print(bracketed_split("aaa{h}}}abc"))
