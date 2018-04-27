from bs4 import BeautifulSoup
import requests
import urllib3
mainUrl = "https://www.flipkart.com/orient-9w-1109-wall-lights-lamp-shade/p/itmemfj3zeg6qara?pid=LAEEMFJ3HAMUCBTS&lid=LSTLAEEMFJ3HAMUCBTSQXTREB&marketplace=FLIPKART&srno=s_1_2&otracker=search&iid=aa9e9741-d51b-4070-bf22-8225f2b1ef3a.LAEEMFJ3HAMUCBTS.SEARCH&qH=4b14d22829fa2694"
def getSoup(url):
	http = urllib3.PoolManager()
	response = http.request('GET', url)
	return BeautifulSoup(response.data, "html.parser")
def checkurl(url):
	if url.find("pf_rd_p") >= 0 or url.find("/p/") >= 0 or url.find(
	    "/gp/") >= 0 or url.find("/dp/") >= 0:
		return True
	else:
		return False
def getPname(soup):
	pname = soup.title.string
	return pname
def getPrice(soup):
	try:
		price = str(soup.find("span", id="priceblock_dealprice"))
		if price == 'None':
			price = str(soup.find("span", id="priceblock_saleprice"))
		if price == 'None':
			price = str(soup.find("span", id="priceblock_ourprice"))
		# if price == 'None':
		# 	matches = soup.findAll(match_class("buyingPrice"))
		#   if len(matches) == 0:
		# 	  price = str(soup.find("span", id="product-price"))
		#   else:
		# 	  price = str(matches[0])
		if price == 'None':
			price = str(soup.find("_1vC4OE_37U4_g"))
		if price == 'None':
			price = str(soup.find("span", id="priceblock_ourprice"))
		price = "\u20b9 " + price.split("</span>")[-2].replace(
		    " ", '').replace("\n", "")
	except:
		try:
			price = str(
			    soup.find(
			        "span", class_="a-size-base a-color-price a-color-price"))
			price = "\u20b9 " + price.split("</span>")[-2].replace(
			    " ", "").replace("\n", "")
		except:
			price = "Product Currently Unavailable!"
	return price
if checkurl(mainUrl) == True:
	soup = getSoup(mainUrl)
	pname = getPname(soup)
	price = getPrice(soup)
	data = {'pname': pname, 'price': price}
	print(pname)
	print(price)
else:
	print("Not a product URL!")
