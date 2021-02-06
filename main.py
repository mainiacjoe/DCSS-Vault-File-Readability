'''
Dungeon Crawl Stone Soup
Vault Map Visualizer

This module adds spaces in between the map glyphs of .des files to
make their appearance in text editor more closely match the 1:1 
aspect ratio of Crawl tiles.  All of the .des files in crawl/data/des 
of 0.26.0 stable are pre-widened within their subfolders at left.

There are two functions. Run the module using the green Run button above,
then type the function calls in the console.

widen(filename,spaceChar=' ')
    Creates a new file in which spaceChar is pleced between each character, 
    in each line that falls between the MAP and ENDMAP tags.  The new 
    filename adds the prefix 'widened-' to the given filename, overwriting 
    that file if it already exists.

    spaceChar defaults to the spacebar character.  Uncode U2000 through U200A
    are spaces of varying widths.  spaceChar can be a string of any length, 
    despite its name.  For my own text editor and its font, the ideal spaceChar 
    is 'u\2004\u2004\u2006' which equals 5/6 em.

    Repl.it's syntax for folders is 'foldername/filename'.  Do include
    '.des' in your filename.  Examples:
        These use the default spaceChar:
            widen('sample.des')
            widen('altar/overflow.des')
        These specify a spaceChar:
            widen('sample.des','\u2002')
            widen('altar/overflow.des','\u2005\u2006')

process(folderName,spaceChar=' ')
    This will apply widen to every filename in folderName which does not already
    have the 'widened-' prefix.  spaceChar defaults to the spacebar character as
    in widen and can be specified as a string of any length.

    Do not include the '/' in the folder name.  Example:
        process('arrival')
        process('branches','\u2003')

    process has not been written for nor tested with nested folders.  I don't
    expect that the results would be desirable, but I also don't expect this
    functionality to be needed.
'''




import os

def applyTags(filename):
    '''
    Parse a file by whether each line is part of the map or part of the code. 
    Return a list of (bool,line) tuples, where True means the line is in the map.
    '''
    with open(filename,encoding='utf-8') as f:
        lines = [line.rstrip() for line in f]
    tagged = []
    inMap = False
    for line in lines:
        if line == 'ENDMAP':
            inMap = False
        tagged.append((inMap,line))
        if line == 'MAP':
            inMap = True
    return tagged

def widen(filename,spaceChar=' '):
    '''
    Write a file that puts spaceChar in between every character of those lines
    which are part of a map.
    To match this to a particular font, use one or more of U-2000 through U-200A.
    ''' 
    tagged = applyTags(filename)
    if '/' in filename:  # in a folder
        folders = filename[:filename.rfind('/')+1]
        filename = filename[filename.rfind('/')+1:]
        newFilename = f'{folders}widened-{filename}'
    else:
        newFilename = f'widened-{filename}'
    with open(newFilename,'w',encoding='utf-8') as f:
        for inMap,line in tagged:
            if inMap:
                f.write(f'{spaceChar.join(line)}\n')
            else:
                f.write(f'{line}\n')


def process(folderName,spaceChar=' '):
    '''
    Apply widen to every .des file in the designated folder
       which does not already begin with 'widened-'.
    folderName ought not include '/' at the end, just the
       folder name.
    Does not necessarily support nested folders.  Written
       for those in this repl.it's root folder and nested
       folders not pursued.
    '''
    filenames = [f for f in os.listdir(f'./{folderName}')
                 if '.des' in f and 'widened-' not in f]
    for filename in filenames:
        widen(f'{folderName}/{filename}',spaceChar) 
