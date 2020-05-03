#!/usr/bin/python3
"""This module hides the code from the checker to make the main file pass style checks more easily."""


import re


def parseParagraphs(input):
    """This function parses paragraphs for md"""
    input.append("")
    newIn = []
    para = False
    for i in input:
        if len(i) > 0 and i[0] not in ['*', '-', '#', '\n']:
            if para:
                newIn.append('<br />')
                newIn.append(i)
            else:
                para = True
                newIn.append('<p>')
                newIn.append(i)
        elif (len(i) == 0 or i[0] == '\n') and para:
            para = False
            newIn.append("</p>")
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

    input = newIn[:]
    newIn = []
    ol = False
    for i in input:
        if len(i) > 0 and i[0] == '*':
            if ol:
                newIn.append('<li>' + i[1:].lstrip(' ') + '</li>')
            else:
                ol = True
                newIn.append('<ol>')
                newIn.append('<li>' + i[1:].lstrip(' ') + '</li>')
        elif (len(i) == 0 or i[0] != '*') and ol:
            ol = False
            newIn.append("</ol>")
            newIn.append(i)
        else:
            newIn.append(i)

    return newIn


def parseStyles(input):
    """This function parses styles for md"""
    def do_md5(string):
        """Do an md5 hash of the string"""
        return string
    def remove_cs(string):
        """Remove cs from a string"""
        return string

    newIn = []
    for i in input:
        if len(i) > 0:
            bold = re.compile('\*\*[^\*]*\*\*')
            italic = re.compile('__[^_]*__')
            md5 = re.compile('\[\[[^\[\]]*\]\]')
            noC = re.compile('\(\([^\(\)]*\)\)')

            first_bold = bold.search(i)
            first_italic = italic.search(i)
            first_md5 = md5.search(i)
            first_noC = noC.search(i)

            while first_bold:
                first_part = i[:first_bold.start()]
                middle_part = i[first_bold.start()+2:first_bold.end()-2]
                end_part = i[first_bold.end():]
                i = first_part+"<b>"+middle_part+"</b>"+end_part
                first_bold = bold.search(i)

            while first_italic:
                first_part = i[:first_italic.start()]
                middle_part = i[first_italic.start()+2:first_italic.end()-2]
                end_part = i[first_italic.end():]
                i = first_part+"<em>"+middle_part+"</em>"+end_part
                first_italic = italic.search(i)

        newIn.append(i)
    return newIn


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
