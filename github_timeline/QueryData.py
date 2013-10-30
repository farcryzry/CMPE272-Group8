# Run a synchronous query, save the results to a table, overwriting the
# existing data, and print the first page of results.
# Default timeout is to wait until query finishes.
def runSyncQuery (service, projectId, datasetId, timeout=0):
  try:
    print 'timeout:%d' % timeout
    jobCollection = service.jobs()
    queryData = {'query':'SELECT * FROM publicdata:samples.github_timeline where repository_url is not null limit 100;',
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
      print 'has a rows attribute'
      printTableData(queryReply, 0)
      currentRow = len(queryReply['rows'])

      # Loop through each page of data
      while('rows' in queryReply and currentRow < queryReply['totalRows']):
        queryReply = jobCollection.getQueryResults(
                          projectId=jobReference['projectId'],
                          jobId=jobReference['jobId'],
                          startIndex=currentRow).execute()
        if('rows' in queryReply):
          printTableData(queryReply, currentRow)
          currentRow += len(queryReply['rows'])

  except AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
    "the application to re-authorize")

  except HttpError as err:
    print 'Error in runSyncQuery:', pprint.pprint(err.content)

  except Exception as err:
    print 'Undefined error' % err
