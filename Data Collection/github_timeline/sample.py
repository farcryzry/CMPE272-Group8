# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line skeleton application for BigQuery API.
Usage:
  $ python sample.py

You can also get help on all the command-line flags the program understands
by running:

  $ python sample.py --help

"""

import argparse
import httplib2
import os
import sys
import csv

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/917277710242/apiui>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/bigquery',
      'https://www.googleapis.com/auth/cloud-platform',
      'https://www.googleapis.com/auth/devstorage.full_control',
      'https://www.googleapis.com/auth/devstorage.read_only',
      'https://www.googleapis.com/auth/devstorage.read_write',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))


def main(argv):
  # Parse the command-line flags.
  flags = parser.parse_args(argv[1:])

  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file.
  storage = file.Storage('github-timeline.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the BigQuery API.
  service = discovery.build('bigquery', 'v2', http=http)

  try:
    #print "Success! Now add code here."
    runSyncQuery (service, "cmpe272-group8", "publicdata:samples", 1000)

  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")
	  
# Run a synchronous query, save the results to a table, overwriting the
# existing data, and print the first page of results.
# Default timeout is to wait until query finishes.
def runSyncQuery (service, projectId, datasetId, timeout=0):
  try:
    print 'timeout:%d' % timeout
    jobCollection = service.jobs()
    queryData = {'query':'SELECT * FROM publicdata:samples.github_timeline where repository_url is not null limit 1000;',
                 'timeoutMs':timeout}

    queryReply = jobCollection.query(projectId=projectId,
                                     body=queryData).execute()

    jobReference=queryReply['jobReference']

    # Timeout exceeded: keep polling until the job is complete.
    while(not queryReply['jobComplete']):
      print 'Job not yet complete...'
      queryReply = jobCollection.getQueryResults(
                          projectId=jobReference['projectId'],
                          jobId=jobReference['jobId'],
                          timeoutMs=timeout).execute()

    # If the result has rows, print the rows in the reply.
    if('rows' in queryReply):
      print 'result lines: ', len(queryReply['rows'])
      printTableData(queryReply)

      # Loop through each page of data
      #while('rows' in queryReply and currentRow < queryReply['totalRows']):
      #  queryReply = jobCollection.getQueryResults(
      #                    projectId=jobReference['projectId'],
      #                    jobId=jobReference['jobId'],
      #                    startIndex=currentRow).execute()
      #  if('rows' in queryReply):
      #    printTableData(queryReply, currentRow)
      #    currentRow += len(queryReply['rows'])

  #except AccessTokenRefreshError:
   # print ("The credentials have been revoked or expired, please re-run"
    #"the application to re-authorize")

  #except HttpError as err:
    #print 'Error in runSyncQuery:', pprint.pprint(err.content)

  except Exception as err:
    print err

def printTableData(queryReply):
  try:
      content = unicode(queryReply.get('schema')['fields']) + "\n"
      print(queryReply.get('schema')['fields'])

      lines = len(queryReply['rows'])
      for i in range(0,lines):
         content += unicode(queryReply.get('rows')[i]) + "\n"
         print(queryReply.get('rows')[i])

      writeToTxt("a.txt", content)
  except Exception as err:
    print err

def writeToCsv(fileName):
    try:
        with open(fileName, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
            spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    except Exception as err:
        print err

def writeToTxt(fileName, content):
    try:
        text_file = open(fileName, "w")
        text_file.write(content)
        text_file.close()

    except Exception as err:
        print err

# For more information on the BigQuery API you can visit:
#
#   https://developers.google.com/bigquery/docs/overview
#
# For more information on the BigQuery API Python library surface you
# can visit:
#
#   https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/
#
# For information on the Python Client Library visit:
#
#   https://developers.google.com/api-client-library/python/start/get_started
if __name__ == '__main__':
  main(sys.argv)
