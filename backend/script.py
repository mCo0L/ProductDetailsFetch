# coding: utf-8

import urllib3
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template


urllib3.disable_warnings()
app = Flask(__name__)


@app.route('/getProductInfo', methods=['GET', 'POST'])
def getInfo():

    content = request.get_json()
    url = content['url']
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}

    check = checkurl(url)

    if check == "Amazon":
        soup = getSoup(url)

        pname = getAmazonPname(soup)
        price = getAmazonPrice(soup)

        data = {'pname': pname, 'price': price}
        return jsonify(data)

    elif check == "Flipkart":
        soup = getSoup(url)

        pname = getFlipPname(soup)
        price = getFlipPrice(soup)

        data = {'pname': pname, 'price': price}
        return jsonify(data)

    else:
        return jsonify({'pname': "Invalid product link", 'price': "Can't fetch Price"})


def checkurl(url):
    if (url.find("/gp/") >= 0 or url.find("/dp/") >= 0) and url.find("amazon.in") >= 0:
        return "Amazon"
    elif (url.find("pf_rd_p") >= 0 or url.find("/p/")) and url.find("flipkart.com") >= 0:
        return "Flipkart"
    else:
        return False


def getSoup(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return BeautifulSoup(response.data, "html.parser")


def getAmazonPname(soup):
    pname = soup.title.string
    pname = pname.replace("Buy ", "").replace(" Online at Low Prices in India - Amazon.in", "")
    return pname


def getFlipPname(soup):
    pname = soup.title.string
    pname = pname.replace(" Online at Best Price with Great Offers Only On Flipkart.com", "")
    return pname


def getAmazonPrice(soup):
    try:
        price = str(soup.find("span", id="priceblock_dealprice"))
        if price == 'None':
            price = str(soup.find("span", id="priceblock_saleprice"))
        if price == 'None':
            price = str(soup.find("span", id="priceblock_ourprice"))
        if price == 'None':
            price = soup.findAll("span", id="buyingPrice")
            if price.count() > 1:
                price = str(price[0])
            else:
                price = str(soup.find("span", id="product-price"))

        price = price.split("</span>")[-2].replace(" ", '').replace("\n", "")
    except:
        try:
            price = str(soup.find("span", class_="a-size-base a-color-price a-color-price"))
            price = price.split("</span>")[-2].replace(" ", "").replace("\n", "")
        except:
            price = "Product Currently Unavailable!"
    return price


def getFlipPrice(soup):
    try:
        price = soup.findAll("div", {"class": "_1vC4OE"})
        price = str(price[0])
        price = price.split("-->")[-1].replace("</div>", "")
    except:
        price = "Product Currently Unavailable!"
    return price


if __name__ == '__main__':
    app.run(port=8000, debug=True)
