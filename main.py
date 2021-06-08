import requests
from bs4 import BeautifulSoup
import subprocess
import os


def get_books():
    book = []
    r = requests.get("https://www.stylist.fr/magazine/archives/")
    soup = BeautifulSoup(r.text)
    book += [x.attrs['href'].split('/')[-1] for x in soup.find_all("a", attrs={'class': 'IssueItem'})]
    for i in range(1, 15):
        url = f'https://www.stylist.fr/magazine/archives/{i}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        book += [x.attrs['href'].split('/')[-1] for x in soup.find_all("a", attrs={'class': 'IssueItem'})]

    return book


def make_js(x):
    js = """const cookies = [{
    'name': "_gat_gtag_UA_137017242_1",
    'value': '1',
    "domain": "mozzoviewer.publishingcenter.net"
}, {
    'name': "_gid",
    'value': "GA1.2.559183115.1623174323",
    "domain": "mozzoviewer.publishingcenter.net"
}, {
    'name': "_gat_gtag_UA_85493217_2",
    'value': '1',
    "domain": "mozzoviewer.publishingcenter.net"
}, {
    'name': "_ga",
    'value': "GA1.2.50440865.1623174323",
    "domain": "mozzoviewer.publishingcenter.net"
}, {
    'name': "reader_language",
    'value': 'fr',
    "domain": "mozzoviewer.publishingcenter.net"
}, {
    'name': "FCREADERHTML",
    'value': "f60bfacb2916ecfcc60bfacb291730", "domain": "mozzoviewer.publishingcenter.net"
}];

const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setCookie(...cookies);
    // Enable request interception
    await page.setRequestInterception(true);
    page.on('request', async (request) => {

        if (request.headers()['x-auth-mozzo']) {
            console.log(request.url());
            console.log(request.headers()['x-auth-mozzo']);
            process.exit(1);

        }

        return request.continue(); // Allow request to continue
        // return request.abort(); // use this instead to abort the request!
    })


    await page.goto('https://www.stylist.fr/archives/read/xxxyyyzzz');
    // Make a screenshot

    await new Promise(r => setTimeout(r, 5000));
    await browser.close();
})()
""".replace('xxxyyyzzz', x)
    return js


def make_curl(name, url, key):
    name = name
    url = url
    key = key
    curl = f"""curl '{url}' \
          -H 'Connection: keep-alive' \
          -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"' \
          -H 'x-auth-mozzo: {key}' \
          -H 'sec-ch-ua-mobile: ?0' \
          -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
          -H 'Accept: */*' \
          -H 'Sec-Fetch-Site: same-origin' \
          -H 'Sec-Fetch-Mode: cors' \
          -H 'Sec-Fetch-Dest: empty' \
          -H 'Accept-Language: en,zh-CN;q=0.9,zh;q=0.8' \
          -H 'Cookie: _gat_gtag_UA_137017242_1=1; _gid=GA1.2.559183115.1623174323; _gat_gtag_UA_85493217_2=1; _ga=GA1.2.50440865.1623174323; reader_language=fr; FCREADERHTML=f60bfacb2916ecfcc60bfacb291730' \
          --compressed --output book/{name}.pdf"""
    return curl


if __name__ == '__main__':
    book = get_books()
    for i in book:
        js = make_js(i)
        with open('a.js', 'w') as w:
            w.write(js)
        s = subprocess.Popen(['node', 'a.js'], stdout=subprocess.PIPE)
        r = [x.decode('utf8') for x in s.communicate() if x][0]
        url, key = r.strip().split('\n')

        curl = make_curl(i, url, key)

        os.system(curl)
