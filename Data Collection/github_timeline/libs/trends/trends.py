import json
from dateutil import parser
import time
import math

def transfer_csv_to_json():

    content = read_file('trends.csv')
    lines = content.split('\n')

    trends = {}
    week_trends = {}
    languages = get_top_languages()

    min_d = date_from_string_to_js_long("1/1/2013")
    max_d = date_from_string_to_js_long("11/19/2013")

    for i in range(1, len(lines)):
        line_items = lines[i].split(",")
        if(len(line_items) == 3):
            d = line_items[0]
            wk = date_to_week_number(d)
            d = date_from_string_to_js_long(d)

            if d >= min_d and d <= max_d:
                lang = line_items[1]
                lang_count = line_items[2]

                lang_count = int(lang_count)

                if lang in languages:
                    if lang not in trends.keys():
                        trends[lang] = []
                        week_trends[lang] = {}

                    trends[lang].append([d, lang_count])

                    if wk not in week_trends[lang]:
                        week_trends[lang][wk] = []

                    week_trends[lang][wk].append(lang_count)


    trends_result = []
    for trend in trends:
        trends[trend].sort()
        trends_result.append({"key": trend, "values": trends[trend]})

    uf = open('daily_trends_2013.json', 'w')
    uf.write(json.dumps(trends_result))
    uf.close()

    #weekly_trends_result = []
    #
    #for trend in week_trends:
    #    week_trend = week_trends[trend]
    #    trend_list = []
    #    for week in week_trend:
    #        trend_list.append([week, sum(week_trend[week])])
    #
    #    weekly_trends_result.append({"key": trend, "values": trend_list})
    #
    #uf = open('weekly_trends_2012.json', 'w')
    #uf.write(json.dumps(weekly_trends_result))
    #uf.close()

    #trends_result_cumulative = []
    #for trend in trends:
    #    trends[trend].sort()
    #    total = 0
    #
    #    for t in trends[trend]:
    #        t[1] = t[1] + total
    #        total = t[1]
    #
    #    trends_result_cumulative.append({"key": trend, "values": trends[trend]})
    #
    #uf = open('trends_cumulative.json', 'w')
    #uf.write(json.dumps(trends_result_cumulative))
    #uf.close()

def date_from_string_to_js_long(sDate):
    dt = parser.parse(sDate)
    return math.floor(time.mktime(dt.utctimetuple()) * 1000)

def date_to_week_number(sDate):
    dt = parser.parse(sDate)
    wk = dt.isocalendar()[1]

    return wk

def get_top_languages():
    content = read_file('top_languages.csv')
    lines = content.split('\n')

    languages = []

    for i in range(1, 11):
        line_items = lines[i].split(",")
        if(len(line_items) == 2):
            lang = line_items[0]

            if lang not in languages:
                languages.append(lang)

    return languages

def read_file(filename):
    try:
       f = open(filename,'r')
       content = f.read()
       f.close()
       return content
    except Exception as err:
        print err

if __name__ == "__main__":
    transfer_csv_to_json()

