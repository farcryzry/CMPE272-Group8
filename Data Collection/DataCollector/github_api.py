import requests
import json
from indeed import IndeedClient
import urllib as req

categories = [{"id":"1","catName":"ALM","parentID":"0"},{"id":"2","catName":"Apache Projects","parentID":"0"},
              {"id":"3","catName":"Architectures","parentID":"0"},{"id":"4","catName":"Build Tools","parentID":"0"},
              {"id":"5","catName":"Compilers","parentID":"0"},{"id":"6","catName":"Database Tools","parentID":"27"},
              {"id":"7","catName":"Java API","parentID":"0"},{"id":"8","catName":"Languages","parentID":"0"},
              {"id":"9","catName":"Mobile OS","parentID":"0"},{"id":"10","catName":"MS Frameworks","parentID":"0"},
              {"id":"11","catName":"Operating Systems","parentID":"0"},{"id":"12","catName":"RDBMS","parentID":"0"},
              {"id":"13","catName":"Unit Testing","parentID":"0"},{"id":"14","catName":"Web Frameworks","parentID":"0"},
              {"id":"15","catName":"CM","parentID":"0"},{"id":"16","catName":"Continuous Integration Tools","parentID":"0"},
              {"id":"17","catName":"NoSQL","parentID":"27"},{"id":"18","catName":"ORM","parentID":"0"},
              {"id":"19","catName":"Software Development Methodologies","parentID":"0"},{"id":"28","catName":"Javascript Libraries","parentID":"0"}]

def post():
    response = requests.post('https://api.github.com/user/repos',
    data=json.dumps({'name': 'foo'}), auth=('user', 'pass'))

    assert response.status_code == 201

def get(url):
    response = requests.get(url)

    assert response.status_code == 200

    return response.content

def repos():
    list = get('https://api.github.com/repositories')

    for repo in list:
        print(repo)

def search(q, l):
    q = req.pathname2url(q)
    l = req.pathname2url(l)
    result = get('https://api.github.com/search/repositories?q={0}+language:{1}&sort=stars&order=desc'.format(q, l))

    return json.loads(result)

#https://github.com/indeedlabs/indeed-python
def test_indeed(q, l):
    client = IndeedClient(publisher = 1019296539940316)
    params = {
        'q' : req.pathname2url(q),
        'l' : req.pathname2url(l),
        'userip' : "1.2.3.4",
        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)"
    }

    search_response = client.search(**params)
    return search_response

if __name__ == "__main__":
    result = search("", "java")
    print(result.get("total_count"))
    result_indeed = test_indeed("python", "san jose")
    print(result.get("totalResults"))
