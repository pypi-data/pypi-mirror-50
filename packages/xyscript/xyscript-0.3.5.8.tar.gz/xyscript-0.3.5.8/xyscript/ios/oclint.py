#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from xyscript.common.xylog import printandresult,successlog,faillog
import webbrowser
from git import Repo
import re
from xyscript.common.mail import Email

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
        try:
            
            self.check_oclint()
            self.check_xcpretty()
            path = os.getcwd()
            path = "/Users/v-sunweiwei/Desktop/saic/ios-shell-driver"

            os.chdir(path)
            printandresult("xcodebuild clean")
            printandresult("xcodebuild | tee xcodebuild.log")
            printandresult("xcodebuild | xcpretty -r json-compilation-database")
            printandresult("cp build/reports/compilation_db.json build/reports/compile_commands.json")
            reports_path = path + "/build/reports"
            os.chdir(reports_path)
            printandresult("oclint-json-compilation-database -e Pods -- -rc=LONG_LINE=200 -rc=LONG_VARIABLE_NAME=30 -rc=NCSS_METHOD=100 -max-priority-1=100000 -max-priority-2=100000 -max-priority-3=100000 >> report.json")
            html_path = "file://" + reports_path + "/report.json"
            # webbrowser.open_new_tab(html_path)

            mail_addresses = self._get_lastest_push_user_mail(path)
            Email(mail_addresses).send_diagnose("/Users/v-sunweiwei/Downloads/timg.jpeg","测试文本")

            # printandresult("open " + reports_path + "/report.json")
        except BaseException as error:
            faillog("run diagnose failed:" + format(error))

    

    def _get_lastest_push_user_mail(self,workspace):
        repo = Repo(workspace)
        result =  repo.git.show('--stat')

        authors = []
        res = re.findall(r'Author\:((?:.|\n)*?>)',result)
        for author in res:
            res = re.findall(r'((?<=\<)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,8}(?=\>))',author)
            for mail_address in res:
                authors.append(mail_address)
        print(authors)

def main():
    OCLint().run_oclint()

if __name__ == "__main__":
    main()
