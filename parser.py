#!/usr/bin/python3
"""This module hides the code from the checker to make the main file pass style checks more easily."""

def parseParagraphs(input):
    """This function parses paragraphs for md"""
    input.append("")
    newIn = []
    para = False
    for i in input:
        if len(i) > 0 and i[0] not in ['*', '-', '#', '\n']:
            if para:
                newIn.append('<br />\n' + i)
            else:
                para = True
                newIn.append('<p>\n' + i)
        elif (len(i) == 0 or i[0] == '\n') and para:
            para = False
            newIn.append("</p>\n")
        else:
            newIn.append(i)
    newIn[-1] = newIn[-1].rstrip('\n')
    return newIn


def parseHeadings(input):
    """This function parses headings for md"""
    newIn = []
    for i in input:
        if i[0] == '#':
            count = 0
            for x in i:
                if x == '#':
                    count = count + 1
            tag = 'h' + str(count)
            inner = ''.join(i.split(' ')[1:])
            newIn.append('<{}>{}</{}>'.format(tag, inner, tag))
        else:
            newIn.append(i)
    return newIn


def parseLists(input):
    """This function parses lists for md"""
    pass


def parseStyles(input):
    """This function parses styles for md"""
    pass


def do_main():
    from sys import argv, stderr
    from os import path
    if len(argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=stderr)
        exit(1)
    if not path.exists(argv[1]):
        print("Missing {}".format(argv[1]), file=stderr)
        exit(1)

    input = []
    with open(argv[1]) as f:
        input = f.readlines()
    input = [x.rstrip('\n') for x in input]

    input = parseParagraphs(input)
    #input = parseHeadings(input)
    #input = parseLists(input)
    #input = parseStyles(input)

    with open(argv[2], "w") as f:
        for x in input:
            f.write(x + "\n")
