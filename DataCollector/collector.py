from downloader import Download
from archive import Archive
import datetime
from datetime import timedelta
import gzip

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
                dl = Download(url, self.downloadFolder)
                dl.start()

    def extract(self, file, folder):
        a = Archive(file)
        a.extract(file, folder)


if __name__ == "__main__":
    collector = Collector("d:\\temp\\")
    #collector.download("http://data.githubarchive.org/2012-04-11-15.json.gz")
    collector.download(datetime.date(2011,02,12), datetime.date(2013,1,10))
    #a = Archive("",ext="gz")
    #a.extract("D:\\temp\\2012-01-01-0.json.gz", "D:\\temp")