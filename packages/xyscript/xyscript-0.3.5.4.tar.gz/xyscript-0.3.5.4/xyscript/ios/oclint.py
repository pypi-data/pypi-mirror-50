#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from xyscript.common.xylog import printandresult,successlog

class OCLint:
    def check_oclint(self):
        result = os.popen("which oclint")
        path = result.read()
        if len(path) <= 0:
            printandresult("brew tap oclint/formulae")
            printandresult("brew install oclint")
        else:
            successlog("the path of oclint is:" + path) 

    def check_xcpretty(self):
        result = os.popen("which xcpretty")
        path = result.read()
        if len(path) <= 0:
            printandresult("gem install xcpretty")
        else:
           successlog("the path of xcpretty is:" + path) 

    def run_oclint(self):
        self.check_oclint()
        self.check_xcpretty()

        os.chdir("/Users/v-sunweiwei/Desktop/saic/ios-shell-driver")
        printandresult("xcodebuild clean")
        printandresult("xcodebuild | xcpretty -r json-compilation-database")
        printandresult("cp build/reports/compilation_db.json build/reports/compile_commands.json")
        os.chdir("/Users/v-sunweiwei/Desktop/saic/ios-shell-driver/build/reports")
        printandresult("oclint-json-compilation-database -e Pods   -- -rc=LONG_LINE=200 -rc=NCSS_METHOD=100 -max-priority-1=9999 -max-priority-2=9999 -max-priority-3=9999  -o=report.html")



def main():
    OCLint().run_oclint()

if __name__ == "__main__":
    main()