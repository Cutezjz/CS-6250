import time
import os
import sys
import argparse
import json
import shutil
from bonnie.submission import Submission

def main():
  parser = argparse.ArgumentParser(description='Submits code to the Udacity site.')
  parser.add_argument('--provider', choices = ['gt', 'udacity'], default = 'gt')
  parser.add_argument('--environment', choices = ['local', 'development', 'staging', 'production'], default = 'production')

  args = parser.parse_args()

  app_data_dir = os.path.abspath(".bonnie")

  submission = Submission('cs6250', 'Project-6', 
                          filenames = ["dns_firewall.py"], 
                          exclude = False, 
                          environment = args.environment, 
                          provider = args.provider,
                          app_data_dir = app_data_dir)

  while not submission.poll():
    time.sleep(3.0)

  if submission.result():
    print json.dumps(submission.result(), indent=4)
  elif submission.error_report():
    print submission.error_report()
  else:
    print "Unknown error."

if __name__ == '__main__':
  main()
