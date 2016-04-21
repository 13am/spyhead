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
    '''
    
    parser = OptionParser(usage=userinfo)
    option_names = ['sep']
    for o in option_names:
        parser.add_option('--' + o,
            type='string',
            action='store',
            dest=o.upper(),
            default=None)
    (options, args) = parser.parse_args()
    return options

def main():
    options = parse_options()
          
    ip = None
    ipname = None
    # no args
    if len(sys.argv) == 1:
        ip = sys.stdin
    # only --sep sep
    elif len(sys.argv) == 3 and options.SEP is not None:
         ip = sys.stdin
    # file name given
    else:
        ipname = sys.argv[-1]
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

    if options.SEP != None:
        sep = options.SEP
        if sep == 'tab':
            sep = '\t'
    else:
        sep = None
    header = header.split(sep)
    
    for i in enumerate(header):
        opline = str(i[0]+1) + ' : ' + i[1] + '\n'
        sys.stderr.write(opline)
    
if __name__ == '__main__':
    main()



