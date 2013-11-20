import csv

def read_file(filename):
    try:
       f = open(filename,'r')
       content = f.read()
       f.close()
       return content
    except Exception as err:
        print err

def save_languages(languages):
    fcsv = open('top_languages.csv', 'wb')
    writer = csv.writer(fcsv, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Language', 'Push Count'])
    for c in languages:
        writer.writerow([c[0], c[1]])
    fcsv.close()

def calculate_top_languages(count):

    languages = {}

    index = 0
    content = read_file('language_correlation.csv')
    lines = content.split('\n')

    for i in range(1, len(lines)):
        line_items = lines[i].split("\",\"")
        if(len(line_items) == 3):
            lang = line_items[1].replace("\"","")
            push_count = line_items[2].replace("\"","")
            push_count = int(push_count)

            if lang is not None:
                if lang not in languages:
                    languages[lang] = 0
                languages[lang]+= push_count

            print(index)
            index += 1

    languages = sorted(languages.items(), key=lambda x: x[1],reverse=True)
    return languages[0:count]

def get_top_languages():
    languages = []

    content = read_file('top_languages.csv')
    lines = content.split('\n')

    for i in range(1, len(lines)):
        line_items = lines[i].split(",")
        if len(line_items) == 2:
            lang = line_items[0]
            push_count = line_items[1]
            push_count = int(push_count)

            if lang is not None:
                if lang not in languages:
                    languages.append(lang)

    return languages

def reduce_language_correlation(languages):

    user_records = {}

    index = 0
    content = read_file('language_correlation.csv')
    lines = content.split('\n')

    for i in range(1, len(lines)):
        line_items = lines[i].split("\",\"")
        if(len(line_items) == 3):
            actor = line_items[0].replace("\"","")
            lang = line_items[1].replace("\"","")
            push_count = line_items[2].replace("\"","")
            push_count = int(push_count)

            if lang is not None:
                if lang in languages:
                    if actor not in user_records:
                        user_records[actor] = {}
                    if lang not in user_records[actor]:
                        user_records[actor][lang] = push_count
                    else:
                        user_records[actor][lang] += push_count
            print(index)
            index += 1

    print(user_records)

if __name__ == "__main__":
    #languages = calculate_top_languages(20)
    #save_languages(languages)
    languages = get_top_languages()
    reduce_language_correlation(languages)