#!/usr/bin/env python

"""
.doc to PDF conversion
David North <david-doc2pdf@dnorth.net>, August 2010

Requirements: Python >= 2.5, unoconv, OpenOffice, Xvfb for headless systems
"""
from __future__ import with_statement # required for Python 2.5

import os
import sys
import time
import shutil
import signal
import traceback
import subprocess

class DisplayHelper:
    """Helper class which can ensure the presence of a display.
       Can be used as a context manager, e.g.
         with DisplayHelper() as disp:
             print "Display running on", disp

    """
    def _start_display(self):
        """Starts a display and returns where it is, e.g. :1"""
        if 'DISPLAY' in os.environ:
            return os.environ['DISPLAY'] # we're done if X is running

        self._disp = ':7' # TODO: try and find a free display to use instead of hard-coding 7
        FNULL = open(os.devnull, 'w')
        self._proc = subprocess.Popen(['Xvfb', self._disp], stdout=FNULL, stderr=FNULL)

        # give Xvfb ten to sort itself out
        time.sleep(10)
        if self._proc.returncode:
            raise Exception("Xvfb terminated prematurely")

        return self._disp

    def _stop_display(self):
        """Stops the running display, if any"""
        if self._proc and not self._proc.returncode:
            pid = self._proc.pid
            os.kill(pid, signal.SIGKILL)

    def __enter__(self):
        disp = self._start_display()
        os.environ['DISPLAY'] = disp
        return disp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_display()
        return False


def doc2pdf(inFile, outFile):
    """Convert file at path inFile to a PDF and save it at outFile"""
    if not os.path.isfile(inFile):
        raise Exception("%s does not exist" % inFile)

    with DisplayHelper() as disp:
        unoconv = subprocess.Popen(['unoconv', inFile])
        unoconv.communicate()
        if unoconv.returncode != 0:
            raise Exception("unoconv failed with exit code " + unoconv.returncode)

        # clean up crap left around by unoconv
        crap = os.path.join(os.getcwd(), '__db.')
        if os.path.isfile(crap):
            os.unlink(crap)

        pdf = inFile[:-3] + 'pdf'
        if not os.path.isfile(pdf):
            raise Exception("PDF not found at %s; unoconv failed" % pdf)
        
        try:
            shutil.move(pdf, outFile)
        except:
            print >> sys.stderr, "Could not write to " + outFile
            raise

def main():
    me, args = sys.argv[0], sys.argv[1:]
    if len(args) != 2 or not os.path.isfile(args[0]):
        print >> sys.stderr, "Usage: %s /path/to/input.doc /path/to/output.pdf" % me
        sys.exit(1)

    inFile, outFile = args

    try:
        doc2pdf(inFile, outFile)
    except:
        print >> sys.stderr, "Error during conversion: "
        raise

    sys.exit(0)

if __name__=='__main__':
    main()
