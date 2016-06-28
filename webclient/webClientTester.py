#!/usr/bin/python

import subprocess
from urlparse import urlparse
import os
import httplib
import sys
from colorama import Fore, Style

CRLF = "\r\n"
OUTPUT_DIR = "project5_temp"

from twisted.protocols.ftp import FileNotFoundError

def main():
    init()
    index=1
    urls = open(os.path.abspath("urls.txt"), "r")
    for url in urls:
        try:
            url = url.rstrip('\n')
            print "Test#%d: Url is %s " % (index, url)
            outputFile = get_output_file(url, index)
            webclient = "%s"% (os.path.abspath("web_client.py"))
            childprocess = subprocess.Popen(['python', webclient, url, outputFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = childprocess.communicate()
            # print any error to the console
            print stdErr

            with open(os.path.abspath(os.path.curdir) + "/%s/stdout.txt" % OUTPUT_DIR, "a") as text_file:
                text_file.writelines("Test#%d: Url is %s %s" % (index, url, CRLF))
                text_file.write(stdOut)
                text_file.write(CRLF+CRLF)

            # Run unit tests
            run_unit_tests(outputFile, stdOut)
            index = index + 1

        except subprocess.CalledProcessError as error:
            errorMessage = ">>> Error while executing:\n"\
                           + "python %s %s %s" % (webclient, url, outputFile) \
                           + "\n>>> Returned with error:\n"\
                           + str(error.output)
            print("Error: " + errorMessage)

        except FileNotFoundError as error:
            errorMessage = error.strerror
            print("Error: ", errorMessage)

    urls.close()
    print Fore.MAGENTA + "The output from web_client.py is at %s" % os.path.abspath(OUTPUT_DIR) + "/stdout.txt"
    print(Style.RESET_ALL)

def init():
    os.system("rm -rf %s" % OUTPUT_DIR)
    os.system("mkdir -p %s" % OUTPUT_DIR)


def run_unit_tests(outputFile, stdOut):
    sanity_check_get_request(stdOut)

    responseCode = get_response_code(stdOut)
    contentLen = get_content_length(stdOut)
    retrievedLen = get_retrieved_len(outputFile)

    if responseCode == httplib.OK:
        if contentLen == retrievedLen: # check if content matches
            if contentLen == 0:
                print Fore.GREEN + "Response is OK but content not retrieved because Content-Length field was not found"
            else:
                print Fore.GREEN + "Response is OK and retrieved content matches Content-Length(%d)" % contentLen
        else:
            print Fore.RED + "Response is OK but retrieved content(%d) doesn't match Content-Length(%d)" \
                             % (retrievedLen, contentLen)
    else: # response is not OK
        if  retrievedLen > 0: # check if content retrieved
            print Fore.RED + "Response is Not-OK(code=%d) but content retrieved! (See piazza @964)" % responseCode
        else:
            print Fore.GREEN + "Response is Not-OK(code=%d) and content not retrieved." % responseCode

    if retrievedLen > 0:
        print "Output: %s" % outputFile

    print(Style.RESET_ALL)


def sanity_check_get_request(stdOut):
    line = stdOut.split(CRLF + CRLF, 1)[0].upper()
    if (line.find('HTTP/1.0') >= 0):
        print Fore.RED + "Project-5 expects HTTP/1.1 since \"Connection\" field must specify non-persistent connections. " \
              "But web_client.py is using HTTP/1.0"
    if (line.find('HOST:') == -1):
        print Fore.RED + "Project-5 expects \"Host:\" field in the HTTP Get request. " \
              "But web_client.py is not using \"Host:\" field"
    if (line.find('CONNECTION:') == -1):
        print Fore.RED + "Project-5 expects \"Connection:\" field in the HTTP Get request. " \
              "But web_client.py is not using \"Connection:\" field"

def get_retrieved_len(outputFile):
    retrievedLen = 0
    if os.path.exists(outputFile):
        statinfo = os.stat(outputFile)
        retrievedLen = statinfo.st_size

    return retrievedLen

def get_response_code(stdOut):
    try:
        line = stdOut.split(CRLF+CRLF, 1)[1].upper()
        offset = line.find('HTTP/1.1')
        #print  line[offset:].split(CRLF, 1)[0]
        responseCode = int(line[offset:].split(CRLF, 1)[0].split(" ")[1])
    except:
        responseCode = sys.maxint

    return responseCode

def get_output_file(url, index):
    outputFile = "url%d.html"%index
    outputDir = os.path.abspath(os.curdir) + '/' + OUTPUT_DIR + '/'
    urlParsed = urlparse(url)
    if urlParsed.path != '' and len(urlParsed.path.split('/')[-1]) > 0:
        outputFile = urlParsed.path.split('/')[-1]

    return outputDir + outputFile

def get_content_length(stdOut):
    contentLen = 0
    pos1 = stdOut.upper().find("CONTENT-LENGTH:")
    if pos1 >= 0:
        line = stdOut[pos1:].split(CRLF)[0].split(":")[1]
        contentLen = int(''.join(x for x in line if x.isdigit()))
    return contentLen

if __name__ == "__main__":
    main()

