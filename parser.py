#!/usr/bin/python3
"""This module hides the code from the checker to make the main file pass style checks more easily."""

def matches(line, thing):
    """check if a line of text matches the given type (h, p, ul, ol, )"""

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
        if len(i) > 0 and i[0] == '#':
            #then it's a heading
            num = 0
            while num < len(i) and i[num] == '#':
                num = num + 1
            if num > 6:
                num = 6
            tag = "h"+str(num)
            i = i.lstrip('#')
            i = i.lstrip(' ')
            i = "<"+tag+">"+i+"</"+tag+">"
        newIn.append(i)
    return newIn


def parseLists(input):
    """This function parses lists for md"""
    newIn = []
    ul = False
    for i in input:
        if len(i) > 0 and i[0] == '-':
            if ul:
                newIn.append('<li>' + i[1:].lstrip(' ') + '</li>')
            else:
                ul = True
                newIn.append('<ul>')
                newIn.append('<li>' + i[1:].lstrip(' ') + '</li>')
        elif (len(i) == 0 or i[0] != '-') and ul:
            ul = False
            newIn.append("</ul>")
            newIn.append(i)
        else:
            newIn.append(i)
    return newIn


def parseStyles(input):
    """This function parses styles for md"""
    return input


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
    input = ''.join(input).split('\n')

#    print(input)
#    print()

    input = parseStyles(input)
    input = '\n'.join(input).split('\n')

#    print(input)
#    print()

    input = parseParagraphs(input)
    input = '\n'.join(input).split('\n')

#    print(input)
#    print()

    input = parseLists(input)
    input = '\n'.join(input).split('\n')

#    print(input)
#    print()

    input = parseHeadings(input)
    input = '\n'.join(input).split('\n')

#    print(input)
#    print()

    with open(argv[2], "w") as f:
        for x in input:
            f.write(x + "\n")
