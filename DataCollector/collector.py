from downloader import Download
from archive import Archive
import datetime
from datetime import timedelta
import gzip
import csv
import json
import collections
import os

class Collector:
    def __init__(self, folder):
        self.downloadFolder = folder

    def download(self, start_date, end_date):
        if(start_date > end_date):
            raise "Start Date should less than End Date"

        days = (end_date - start_date).days + 1
        url_pattern = "http://data.githubarchive.org/{0}-{1}.json.gz"

        for x in range(0, days):
            for y in range(0, 24):
                date = start_date + timedelta(days=x)
                url = str.format(url_pattern, date.strftime('%Y-%m-%d'), y)
                print(url)
                try:
                    dl = Download(url, self.downloadFolder)
                    dl.start()
                except Exception as e:
                    print("Error: " + e.message)

    def extract(self, start_date, end_date):
        if(start_date > end_date):
            raise "Start Date should less than End Date"

        days = (end_date - start_date).days + 1
        file_pattern = "D:\\temp\\{0}-{1}.json.gz"

        for x in range(0, days):
            for y in range(0, 24):
                date = start_date + timedelta(days=x)
                file_path = str.format(file_pattern, date.strftime('%Y-%m-%d'), y)
                print(file_path)
                csv_file = str.format("{0}.csv", file_path)
                if os.path.isfile(csv_file):
                    print(str.format("{0} existed", csv_file))
                else:
                    if os.path.isfile(file_path):
                        self.extractFile(file_path)
                    else:
                        print(str.format("{0} not existed", file_path))

    def extractFile(self, file):
        try:
            f = gzip.open(file, 'rb')
            file_content = f.read()
            f.close()
        except Exception as e:
            print("Error: " + e.message)
            return

        event_type_list = ['CreateEvent', 'DeleteEvent', 'DownloadEvent', 'FollowEvent', 'IssuesEvent', 'MemberEvent',
                           'PullRequestEvent', 'PushEvent', 'ReleaseEvent', 'TeamAddEvent', 'WatchEvent']
        repository_columns = ["id", "url", "has_downloads", "created_at", "has_issues","description","forks","fork",
                              "has_wiki","homepage","size","private","name","owner","open_issues","watchers",
                              "pushed_at","language", "master_branch", "organization", "stargazers"]
        lines = []
        urls = []

        list = file_content.split("\n")

        if(len(list) <= 1):
            file_content = file_content.replace('}{"', '}\n{"')
            list = file_content.split("\n")

        for i in range(0, len(list)):

            #try:
                if(list[i]):

                    if(list[i].count('"repo":') > 1 or list[i].count('"repository":') > 1):

                        sub_content = list[i].replace('}{"', '}\n{"')
                        sub_list = sub_content.split("\n")
                        for i in range(0, len(sub_list)):
                            #try:
                                if(sub_list[i]):
                                    sub_json_str = unicode(sub_list[i], "ISO-8859-1")
                                    sub_j = json.loads(sub_json_str, object_pairs_hook=collections.OrderedDict)
                                    self.parseJson(sub_j, event_type_list, urls, repository_columns, lines)
                             #except Exception as e:
                                #print("Error: " + e.message)
                    else:
                        json_str = unicode(list[i], "ISO-8859-1")
                        j = json.loads(json_str, object_pairs_hook=collections.OrderedDict)
                        self.parseJson(j, event_type_list, urls, repository_columns, lines)

            #except Exception as e:
                #print("Error: " + e.message)
                #print(json_str)

        csv_file = open(file + ".csv", 'wb')
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        wr.writerow(repository_columns)
        for item in lines:
            #print(item)
            wr.writerow(item)

        del(file_content)
        del(lines)
        del(urls)
        del(list)

    def parseJson(self, j, event_type_list, urls, repository_columns, lines):
        type = j.get('type')
        if(type in event_type_list):
            repository =  (j.get('repo'), j.get('repository'))[j.get('repository') != None]

            if(repository != None):

                #print(j.get('repository'))
                url = repository.get('url')

                if not url in urls:
                    urls.append(url)
                    line = []
                    for column in repository_columns:
                        s = ""

                        val = repository.get(column)
                        if(val != None):
                            if(isinstance(val, (int))):
                                s = str(val)
                            else:
                                if(isinstance(val, (unicode))):
                                    s = val.encode('utf-8')
                                else:
                                    s = val

                        line.append(s)
                    lines.append(line)

        #lines.append(self.flatten(j))
        #print(self.flatten(j))

    def getJsonColumns(self, l, prefixes=[]):
        columns = []
        if isinstance(l, (list, tuple)):
            for item in l:
                columns.extend(self.getJsonColumns(item))
        elif isinstance(l, (dict)):
            for dictkey in l.keys():
                if(dictkey != 'payload'):
                    prefixes.append(dictkey)
                    #print('.'.join(prefixes))
                    columns.append('.'.join(prefixes))

                    columns.extend(self.getJsonColumns(l[dictkey], prefixes))
                    prefixes.pop()
        return columns

    def flatten(self, l):
        out = []
        if isinstance(l, (list, tuple)):
            for item in l:
                out.extend(self.flatten(item))
        elif isinstance(l, (dict)):
            for dictkey in l.keys():
                if(dictkey != 'payload'):
                    out.extend(self.flatten(l[dictkey]))
        elif isinstance(l, (str, int, unicode)):
            s = ""
            if(isinstance(l, (int))):
                s = str(l)
            else:
                if(isinstance(l, (unicode))):
                    s = l.encode('utf-8')
                else:
                    s = l
            out.append(s)
        return out

if __name__ == "__main__":
    collector = Collector("d:\\temp\\")

    #Step 1: download
    #collector.download(datetime.date(2012,2,1), datetime.date(2013,2,1))

    #Step 2: extraction
    collector.extract(datetime.date(2011,1,1), datetime.date(2013,10,1))
    #collector.extractFile("d:\\temp\\2012-01-04-21.json.gz")

