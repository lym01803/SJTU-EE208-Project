import asyncio
from pyppeteer import launch
from pyppeteer import launcher
import sys, re, os, time
from tqdm import tqdm
from bs4 import BeautifulSoup as BSp
launcher.AUTOMATION_ARGS.remove("--enable-automation")
links = []
price = []
def getTargetLinks(page):
    global links, price
    content = ''
    url = "https://list.jd.com/list.html?cat=670,671,672&page={}&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main".format(page)

    async def main():
        browser = await launch(headless=True)
        page = await browser.newPage()
        await page.goto(url, {'timeout': 60*1000})
        await page.evaluate("""
        	           ()=>{
        	               Object.defineProperties(navigator, {
        	                   webdriver: {
        	                       get: ()=>false
        	                   }
        	               })
        	           }
        	       """)
        content = await page.content()
        #print(content)
        bsp = BSp(content, 'html.parser')
        #with open('debug.txt', 'w', encoding='utf8') as fout:
        #    fout.write('{}'.format(content))
        for item in bsp.find_all('li', attrs={'class': 'gl-item'}):
            links.append(item.div.find_all('div', attrs={'class': 'p-img'})[0].a.get('href'))
            J_price = item.find_all('strong', attrs={'class':'J_price'})[0]
            if J_price != None:
                price.append(J_price.get_text())
            else:
                price.append('none')
        #for item in bsp.find_all('div', attrs={'class': 'p-price'}):
            # print(item)
            #price.append(item.get_text().strip().replace('\n', ''))
        print(len(price))
        await browser.close()
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except:
        pass
for st in tqdm(range(0, 40)):
    price = []
    links = []
    for i in tqdm(range(st*20, (st+1)*20)):
        getTargetLinks(i)
        print('sleep...')
        time.sleep(5)
        print('...')
    print(price)
    with open('targetlinkstest.txt', 'a', encoding='utf8') as fout:
        num = len(links)
        for i in range(num):
            fout.write('{} {}\n'.format(links[i], price[i]))
    print(len(links))