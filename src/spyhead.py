#!/usr/bin/python

from optparse import OptionParser
import sys
import gzip

def parse_options():

    userinfo = ''' 
    \nUse this program to list the column indexes and names of some input. E.g.:
    
    spyhead.py my_input.txt
    spyhead.py --sep ";" my_input.txt
    cat my_input.txt | spyhead.py
    cat my_input.txt | spyhead.py --sep ";"
    spyhead.py --sep tab my_input.txt
    
    The --sep options understands two special keywords "tab" and "space"
    for tab or space delimited files.
    '''
    
    parser = OptionParser(usage=userinfo)

    parser.add_option('--sep',
        type='string',
        action='store',
        dest='SEP',
        default=None)
    (options, args) = parser.parse_args()
    
    return options, args

def main():
    options, args = parse_options()
          
    ip = None
    ipname = None
    if len(args) == 0:
        ip = sys.stdin
    else:
        ipname = args[-1]
        zipped = False
        try:
            if ipname[-3:].lower() == '.gz':
                zipped = True
        except:
            pass
        if zipped:
            ip = gzip.open(ipname, 'r')
        else:
            ip = open(ipname, 'r')
    
    try:
        header = ip.readline()
        if ipname is not None:
            ip.close()
    except IOError:
        sys.stderr.write('Error: the input could not be read\n')
        sys.exit()

    if options.SEP is not None:
        sep = options.SEP
        if sep == 'tab':
            sep = '\t'
        if sep == 'space':
            sep = ' '
    else:
        sep = None
    header = header.split(sep)
    
    for i in enumerate(header):
        opline = str(i[0]+1) + ' : ' + i[1] + '\n'
        sys.stderr.write(opline)
    
if __name__ == '__main__':
    main()



