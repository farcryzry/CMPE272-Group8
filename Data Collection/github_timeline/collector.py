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
import glob
import datetime
import json

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

from os.path import basename

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])

def writeToTxt(fileName, content):
    try:
        text_file = open(fileName, "w")
        text_file.write(content.encode('UTF-8'))
        text_file.close()

    except Exception as err:
        print err

def readFile(filename):
        try:
           f = open(filename,'r')
           content = f.read()
           f.close()
           return content
        except Exception as err:
            print err

def changeClient():
    values = get_clinet_info_from_jsonFile('client_secrets.json')
    modifyDatFile('github-timeline.dat', values)

def get_clinet_info_from_jsonFile(file):
    jsonContent = readFile(file)
    clientJson = json.loads(jsonContent)

    values = {"client_id": clientJson["installed"]["client_id"],
            "client_secret": clientJson["installed"]["client_secret"]}
    return values

def modifyDatFile(file, values):
    jsonContent = readFile(file)
    clientJson = json.loads(jsonContent)

    clientJson['client_id'] = values['client_id']
    clientJson['client_secret'] = values['client_secret']
    writeToTxt(file, json.dumps(clientJson))

#changeClient()

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

SQL_PATH = 'sql\\'
OUTPUT_PATH = 'result\\'

def initService(argv):
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
    return service

def main(argv):

    service = initService(argv)

    try:
        print "Success! Now add code here."
        query = Query(service, "green-segment-405", "publicdata:samples", 60)

        sqlFiles = glob.glob(SQL_PATH + '*.sql')

        strNow = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        #for file in sqlFiles:
            #query.runSyncQuery(file, OUTPUT_PATH + basename(file) + strNow + '.csv')
        #languages = get_top_languages()
        #query.runSyncQuery(SQL_PATH +'language_correlation.sql', OUTPUT_PATH + 'language_correlation.csv', languages)
    except client.AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, please re-run the application to re-authorize")

def read_file(filename):
    try:
       f = open(filename,'r')
       content = f.read()
       f.close()
       return content
    except Exception as err:
        print err

def get_top_languages():

    languages = []
    content = read_file(OUTPUT_PATH + 'top_languages.csv')
    lines = content.split('\n')

    for i in range(1, len(lines)):
        line_items = lines[i].split(",")
        if(len(line_items) == 2):
            lang = line_items[0]

            if lang not in languages:
                languages.append(lang)

    return languages

class Query():
    def __init__(self, service, projectId, datasetId, timeout=0):
        self.service = service
        self.projectId = projectId
        self.datasetId = datasetId
        self.timeout = timeout

    # Run a synchronous query, save the results to a table, overwriting the
    # existing data, and print the first page of results.
    # Default timeout is to wait until query finishes.
    def runSyncQuery (self, sql, outputFile, v_list):

        if v_list is None:
            v_list = ['']

        sql = readFile(sql)

        index = 0
        for v in v_list:
            try:
                print 'timeout:%d' % self.timeout
                jobCollection = self.service.jobs()

                queryData = {'query':sql.replace("{0}", v),'timeoutMs':self.timeout }

                queryReply = jobCollection.query(projectId=self.projectId,
                                                 body=queryData).execute()

                jobReference = queryReply['jobReference']

                # Timeout exceeded: keep polling until the job is complete.
                while(not queryReply['jobComplete']):
                    print 'Job not yet complete...'
                    queryReply = jobCollection.getQueryResults(
                                  projectId=jobReference['projectId'],
                                  jobId=jobReference['jobId'],
                                  timeoutMs=self.timeout).execute()

                # If the result has rows, print the rows in the reply.
                if('rows' in queryReply):
                    self.SaveData(queryReply, outputFile.replace('.csv', str(index) + '.csv'))

            except Exception as err:
                print err

            index += 1

    def SaveData(self, queryReply, outputFile):
        #try:
            #print(queryReply)

            columns = queryReply.get('schema')['fields']
            columnsArray = []
            for i in range(0, len(columns)):
                columnsArray.append(unicode("\"" + columns[i].get('name') + "\"" ))

            content = unicode(",".join(columnsArray) + '\n')

            rows = queryReply['rows']

            print(len(rows))

            for i in range(0, len(rows)):
                rowArray = []
                row = rows[i].get('f')
                for j in range(0, len(row)):
                    if not(row[j] is None):
                        rowArray.append(unicode("\"" + row[j].get('v') + "\"" ))
                content += unicode(",".join(rowArray) + '\n')
                print(i)

            writeToTxt(outputFile, content)

        #except Exception as err:
        #    print err




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