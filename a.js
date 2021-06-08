const cookies = [{
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