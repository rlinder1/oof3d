# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

import os
import re
import sys

# Flag that says whether to generate missing reference data files.
# Should be false unless you really know what you're doing.
generate=False
# Max number to report from one file.
maxerrors = 10

errorcount = 0
filename1 = None
filename2 = None
silent = False

# globals, because we can afford to be quick and dirty here.
def print_header():
    global filename1, filename2, silent
    if not silent:
        print >> sys.stderr, "Error comparing files", filename1, "and", filename2

def print_mismatch(line, v1, v2):
    global errorcount
    if errorcount==0:
        print_header()
    if errorcount == maxerrors and not silent:
        print >> sys.stderr, "[Skipping further errors]"
    if errorcount < maxerrors and not silent:
        print >> sys.stderr, "   line %5d: %s != %s" % (line+1, v1, v2)
    errorcount += 1

def conversion_error(line, v1, v2):
    global errorcount
    if not errorcount:
        print_header()
    if not silent:
        print >> sys.stderr, ("   line %5d: %s // %s  (conversion error!)"
                              % (line+1, v1, v2))
    errorcount += 1
        
def eof_error(line, filename):
    global errorcount
    if not errorcount:
        print_header()
    if not silent:
        print >> sys.stderr, ("   line %5d: Premature EOF in file %s!" 
                              % (line+1, filename))
    errorcount += 1

def fp_file_compare(file1, file2, tolerance, comment="#", pdfmode=False,
                    ignoretime=False, quiet=False):
    # Regexp for matching floating-point numbers, copied from section
    # 4.2.6 of the Python 2.3 documentation.  The "(...)" group
    # constructs in the original have been replaced by "(?:...)"
    # constructs, as a way of grouping sub-expressions without
    # creating explicit groups in the regexp itself. The explicit
    # groups cause split and match to be annoying.
    floatpattern = re.compile(
        "[-+]?(?:\d+(?:\.\d*)?|\d*\.\d+)(?:[eE][-+]?\d+)?")

    # Pattern for detecting PDF date strings, which should not be
    # compared.  This looks for a non-digit or beginning of a line,
    # followed by exactly 14 digits, followed by 'Z'.
    datepattern = re.compile("(?:\D|^)\d{14}Z")
    # Pattern for detecting the time as printed by datetime.today().
    timepattern = re.compile("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d\.\d*")

    try:
        f2 = file(file2)
    except:
        if generate:
            os.rename(file1,file2)
            print >> sys.stderr, "\nMoving file %s to %s.\n" % (file1, file2)
            return True
        else:
            raise

    f1 = file(file1)

    global errorcount, filename1, filename2, silent
    filename1 = file1           # store in globals
    filename2 = file2
    errorcount = 0
    silent = quiet

    try:
        for f1_lineno, f1_line in enumerate(f1):
            try:
                f2_line = f2.next()
            except StopIteration:
                eof_error(f1_lineno, filename2)
                break
            if f1_line[0] == f2_line[0] == comment:
                continue

            # If we're comparing PDF files, and both lines contain
            # date strings, just go on to the next lines.  This
            # ignores anything else on a line containing dates.  It's
            # not generally true that there's nothing else interesting
            # on date lines, but it is true of the pdf's generated by
            # oof.
            if ((pdfmode and 
                datepattern.search(f1_line) and datepattern.search(f2_line)) or
                (ignoretime and 
                timepattern.search(f1_line) and timepattern.search(f2_line))):
                continue
                
            f1_text_items = floatpattern.split(f1_line)
            f2_text_items = floatpattern.split(f2_line)
            f1_float_items = floatpattern.findall(f1_line)
            f2_float_items = floatpattern.findall(f2_line)

            for (item1, item2) in zip(f1_text_items, f2_text_items):
                if item1.strip() != item2.strip():
                    print_mismatch(f1_lineno, item1, item2)
            
            for(item1, item2) in zip(f1_float_items, f2_float_items):
                try:
                    int1 = int(item1)
                    int2 = int(item2)
                except ValueError:
                    try:
                        float1 = float(item1)
                        float2 = float(item2)
                    except ValueError:
                        conversion_error(f1_lineno, item1, item2)
                    else:
                        diff = abs(float1 - float2)
                        reltol = min(abs(float1), abs(float2))*tolerance
                        # This uses the same tolerance for both absolute
                        # and relative error, which isn't usually a good
                        # idea, but is ok if the numbers being compared
                        # are more or less of order 1.
                        ok = diff < reltol or diff < tolerance
                        if not ok:
                            print_mismatch(f1_lineno,
                                           "%-16.9g"%float1, "%-16.9g"%float2)
                else: # Integer conversion worked, do comparison.
                    if int1!=int2:
                        print_mismatch(f1_lineno, "%16d"%int1, "%16d"%int2)

        # Done with the lines in file 1. Check that there's nothing
        # left in file 2.
        try:
            f2_line = f2.next()
        except StopIteration:
            pass
        else:
            eof_error(f1_lineno, filename1)
        
        if errorcount > 0:
            if not silent:
                print >> sys.stderr, ("%d error%s in file comparison!" %
                                      (errorcount, "s"*(errorcount!=1)))
            return False
        return True
    finally:
        f1.close()
        f2.close()
    
if __name__ == "__main__":
    import sys
    import getopt

    tolerance = 0
    pdf = False
    commentchar = '#'

    option_list = ['tolerance=', 'pdf', 'comment', 'max=']
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'c:t:pm:', option_list)
    except getopt.error, message:
        print message
        sys.exit()

    for opt in optlist:
        if opt[0] in ('--tolerance', '-t'):
            tolerance = float(opt[1])
        if opt[0] in ('--pdf', '-p'):
            pdf = True
        if opt[0] in ('--comment', '-c'):
            commentchar = opt[1]
        if opt[0] in ('--max', '-m'):
            maxerrors = int(opt[1])

    ok = fp_file_compare(args[0], args[1], tolerance=tolerance,
                         comment=commentchar, pdfmode=pdf)
    if not ok:
        print 'Files differ.'
        sys.exit(1)
    sys.exit(0)
