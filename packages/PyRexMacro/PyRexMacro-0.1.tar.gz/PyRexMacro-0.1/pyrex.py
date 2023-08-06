#!/usr/bin/env python3
'''
Try "pyrex -h" for information.
(Or "pyrex.py -h")
'''

import sys, re, os, datetime
from io import StringIO


debugmask   = 0x0000
DBG_BASE    = 0x0001    # Base level messages.
DBG_INPUT   = 0x0002    # Trace reading input lines.
DBG_PARSE   = 0x0004    # Trace macro call parse.
DBG_DEFS    = 0x0008    # Trace macro definitions.

# regex for start of macro
startPat = re.compile( r'{#(\w*)(?=[,}])' )

# regex for reference to arg of user macro
# note: (?<!...) is a "negative lookbehind assertion"
argRefPat = re.compile( r'(?<!\\)#[1-9]' );

searchpath = ['.']
infilenames = []
outfilename = '<stdout>'
outbuf = []
symbols = {}

##
## Builtins:
##

# Expand {#} or {#WHERE} into  filename:linenum
def macWhere(minfo,finfo):
  (head,tail) = os.path.split(finfo.path)
  return '%s:%d ' % (tail,finfo.linenum)
symbols['WHERE'] = macWhere

# Expand {#DATE} into, e.g. 2017-10-01
def macDate(minfo,finfo):
    return '%s' % (datetime.datetime.today().strftime("%Y-%m-%d"),)
symbols['DATE'] = macDate

# Expand {#TIME} into, e.g. 2017-10-01
def macTime(minfo,finfo):
    return '%s' % (datetime.datetime.today().strftime("%H:%M:%S"),)
symbols['TIME'] = macTime

# Expand {#DEFINE,macname,macvalue} to '', defining new macro.
def macDefine(minfo,finfo):
    if len(minfo.macroargs) != 2:
        raise RuntimeError( "#DEFINE of %r has wrong # args: %r -- should be 2!" \
              % (minfo.macroname, minfo.macroargs,) )
    symbols[minfo.macroargs[0]] = minfo.macroargs[1]
    dumpSymbols()
    return '';
symbols['DEFINE'] = macDefine

# Expand {#IFEQ,macroname,val,trueval,falseval}
def macIfEq(minfo,finfo):
    if len(minfo.macroargs) != 4:
        raise RuntimeError( "#IFEQ must have four arguments; args: %r." \
              % (minfo.macroargs,) )
    return minfo.macroargs[2] \
        if getSymVal( minfo.macroargs[0]) == minfo.macroargs[1] \
        else minfo.macroargs[3]
symbols['IFEQ'] = macIfEq

##
## Debug & Error output
##

def dbg( bits, msg):
    if debugmask & bits:
        errout( msg)  
def errout(msg):
    print(">>> "+msg, file=sys.stderr)

def dumpSymbols():
    dbg(DBG_DEFS,"Symbol Table:")
    for key, value in symbols.items():
        dbg(DBG_DEFS, "  Macro %r = %s" % (key,value))

class FileInfo:
    def __init__(self, infilename):
        '''
        infilename is one of 
          '<stdin>'                 
                returns ('<stdin>', sys.stdin)
          An absolute-file-path     
                returns (absolute-file-path,  file-object) 
          A relative-file-path
                returns (absolute-file-path,  file-object) 
        '''
        self.path = None
        self.linenum = 0
        self.file = None
        if infilename == '<stdin>':
            self.path = '<stdin>'
            self.file = sys.stdin
        elif infilename[0] == '/':
            self.path = infilename
            self.file = open(infilename,'r')
        else:
            for p in searchpath:
                ftry = os.path.join(p, infilename)
                #errout("_get_file_name trying %r" % ftry)
                if os.path.isfile(ftry):
                    try:
                        self.path = ftry
                        self.file = open(ftry, 'r')
                    except FileNotFoundError:
                        continue
        if not self.file:
            raise RuntimeError( "FileInfo constructor: %r not found" % infilename )
        self.linenum = 0

    def __repr__(self):
        return "<FileInfo path %r, file %r, linenum %r>" \
        % (self.path,self.file,self.linenum)


class MacInfo:
    def __init__(self, start, end, macroname, macroargs):
        self.start = start
        self.end = end
        self.macroname = macroname
        self.macroargs = macroargs

    def __repr__(self):
        return "<MacInfo start %r, end %r, macroname %r, macroargs %r>" \
        % (self.start,self.end,self.macroname,self.macroargs)


def getMacInfo(subject):
    '''
    Return None if no match, else returns an instance of MacInfo,
    (containing start/end/macroname/macroargs).
    '''
    ix = 0
    while True:
        mo = re.search( startPat, subject)
        if not mo:
            return None

        start = mo.start()
        macroname = mo.group(1) if mo.group(1) else 'WHERE'
        dbg( DBG_PARSE, "start %r, macroname: %r" % (start, macroname))
        ix = mo.end()
        if subject[ix] == ',':
            ix += 1
        macroargs = []
        arg = ''
        bracketCnt = 1
        while True:
            ch = subject[ix]
            ix += 1
            if ch == '\\' and subject[ix] in ',{}\\':
                arg += subject[ix]
                ix += 1
            elif ch == '{':
                bracketCnt += 1
                arg += ch
            elif ch == '}':
                bracketCnt -= 1
                if( bracketCnt == 0 ):
                    macroargs.append(arg)
                    macinfo = MacInfo( start, ix, macroname, macroargs)
                    dbg(DBG_PARSE, "macroinfo %r" % macinfo)
                    return macinfo
                arg += ch
            elif ch == ',' and bracketCnt==1:       #end arg
                macroargs.append(arg)
                arg = ''
            else:             # ch not escaped char and not ',' ...
                arg += ch     # ... or '}' inside nested brackets.
                continue

def expandString( minfo, finfo, line):
    '''
    Expand and return a single string or line.
    ''' 
    dbg(DBG_INPUT,"=====%s:%d %r" \
                  % ( finfo.path, finfo.linenum, line,))
    while True:
        minfo = getMacInfo(line)
        if minfo is None:
            break
        else:
            symval = getSymVal( minfo.macroname)
            if isinstance(symval, str):             # symval is a string
                s = symval
                dbg(DBG_PARSE, "Call user macro, %r: %s" % (minfo.macroname,s))
                while True:
                    mo = re.search( argRefPat, s)
                    if not mo:
                        break
                    argidx = int( mo.group()[1] ) - 1
                    #dbg(0xFFFF,"argidx", argidx)
                    args = minfo.macroargs
                    #dbg(0xFFFF,"args", args)
                    substitute = expandString( minfo, finfo, args[argidx]) \
                                 if argidx < len(args)    else ''
                    #dbg(0xFFFF,"substitute", substitute)
                    s = s[0:mo.start()] + substitute + s[mo.end():]
                    #dbg(0xFFFF,"s", s)
            else:                                   # symval is a builtin function
                s = symval( minfo, finfo)
                if not s:
                    s = ''
            line = line[0:minfo.start] + s + line[minfo.end:]
    return line

# Find and return the value of symName in `symbol` or in the OS environment.
# If not found, return ''.
def getSymVal(symName):
    val = symbols.get( symName, None)
    if val is None:
        try:
          val = os.environ[ symName]
        except KeyError:
          val = ''
    dbg(DBG_BASE, "getSymVal %r ==> %r" % (symName, val))
    return val

class PyRex:
    def __init__(self, infilename):
        self.finfo = FileInfo(infilename)
        self.minfo = None

    def expandFile(self):
        '''
        Expand the input file.
        '''
        global outbuf
        condState = None
        dbg(DBG_BASE, "expanding file, %r." % self.finfo.path)
        for line in self.finfo.file:
            self.finfo.linenum += 1

            mo = re.search( r'^(#if|#ifnot) +(\w+) +(\S+) *$', line)
            if mo:
                if condState != None:
                    raise "Nested #if/#ifnot"
                symval = getSymVal(mo.group(2))
                val = mo.group(3)
                if mo.group(1)=='#if':
                  condState = 'do_it' if symval==val else 'skip_it'
                else:     # mo.group(1)=='#ifnot'
                  condState = 'do_it' if symval!=val else 'skip_it'
                #print(f"{mo.group(1)} symval {symval} val {val} condState {condState}")
                outbuf.append('\n')
                continue

            if re.search( r'#endif *$', line):
                condState = None
                outbuf.append('\n')
                continue

            if condState == None or condState == 'do_it':
                outbuf.append( expandString( self.minfo, self.finfo, line))
                continue
            else:       # condState=='skipit'
                outbuf.append('\n')
                continue
        self.finfo.file.close()

def usage(msg=''):
    '''
    Help for command line usage.
    '''
    if(msg):
        sys.stderr.write(msg+'\n')
    sys.stderr.write(
'''Usage:  python pytem.py [options] infile, ...

PyRex is a macro processor that expands infiles, in order, to stdout
or the specified output file. If no infiles specified, or if one of
the infiles is '-', use stdin.

Options
  (-h | --help)         This help message.
  (-d | --debug)        debug mask bits
                        0x0001    # Base level messages.
                        0x0002    # Trace reading input lines.
                        0x0004    # Trace macro call parse.
                        0x0008    # Trace macro definitions.
  (-s | --searchpath)   path1,path2,...
  (-o | --out)          Out file name. Defaults to '<stdout>' if
                        not specified.
  (-Dname value)        add to macro symbol table

Macro Calls:
  {#} or {#WHERE}
      Replaced by name-of-source-file:line-number
  {#DATE}
      Replaced by date, e.g. 2017-12-25
  {#TIME}
      Replaced by 24 hour time, e.g. 14:27:05
  {#DEFINE, macroname, definition of user macro}
      The definition can contain embedded macro calls or'{', 
      '}', and ',' characters, escaped with a backslash.
      (See NOTES below.)
  {#macroname}  or {#macroname,arg1,arg2...}
      Replaced by macroname's definition.
      Arg regs, #1 ... #9, meaningful only inside a macroname,
      are replaced by value of arg of enclosing macro value.
      The macroname can be either define in #DEFINE call or
      can be defined as an OS environment variable.
  {#IFEQ,macroname,val,thenval,elseval}
      Replaced by thenval if the value of macroname == val
      else replaced by elseval.

Conditional Compilation:
  #if name word       include until #endif, iff name's value is word
  #ifnot name word    include until #endif, iff name's value is not word
  #endif              end if included/excluded section
  (These three operations must start at the beginning of a line,
  and can not be nested.)

NOTES:
  Inside the macro brackets, embedded balanced brackets (for example
  embedded macro calls) may be nested; similarly a comma separator
  is only recognized when it is not nested inside internal brackets.

  After a macro's value replaces the macro call, scanning continues at
  the beginning of the substituted text, supporting user macros whose
  definition contain macro calls.
''')

    sys.exit(1)
    
def run():
    '''
    Command line use.  Get options from sys.argv.
    '''
    global debugmask, searchpath, infilenames, outfilename, outbuf, symbols

    args = sys.argv
    args.pop(0)
    dbg(DBG_BASE, "args list is %r" % (args,))

    while len(args):
        arg = args.pop(0)
        if arg[0] == '-':       # flag argument

            # Show usage info.
            if arg == '-h' or arg == '--help':
                usage()

            # Set debug mask, e.g.   -d 0x0001
            elif arg == '-d' or arg == '--debug':
                debugmask = int( args.pop(0), 16)
                dbg(0xFFFF,"debugmask now: %x" % (debugmask,))

            # Set searchpath, e.g. -s "/my,/home/sdb , /tmp/work/me"
            elif arg == '-s' or arg == '--searchpath':
                searchpath = re.split(r' *, *', args.pop())

            # Set output file
            elif arg == '-o' or arg == '--out':
                outfilename = args.pop(0)

            # Add to macro symbol table
            elif arg[0:2] == '-D':
                symbols[arg[2:]] = args.pop(0)
                dumpSymbols()
                
            # Use stdin for next in infilenames          
            else:  # '-' char w/o flag... input from <stdin>.
                infilenames.append( '-' )

        # Use arg for next in infilenames              
        else:                    # non-flag argument (input file name)
            infilenames.append( arg)

    # If no infiles specified use stdin
    if( len(infilenames)==0 ):
        infilenames.append( '-' )    

    # Make sure searchpath includes current directory.
    if not '.' in searchpath:
        searchpath += ['.']


    dbg(DBG_BASE, "infilenames is %r" % (infilenames,))
    dbg(DBG_BASE, "outfilename is %r" % (outfilename,))

    while len(infilenames):
        filearg = infilenames.pop(0)
        infilename = '<stdin>' if filearg == '-' else filearg
        pyrex = PyRex( infilename)
        pyrex.expandFile()

    outfile = ( sys.stdout
                if outfilename == '<stdout>'
                else open(outfilename, 'w'))
    outfile.write( ''.join( outbuf))
    outfile.close()

if __name__ == '__main__':
    run();
    sys.exit(0)