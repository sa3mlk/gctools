from bs4 import BeautifulSoup
from urllib2 import urlopen
import simplejson as json

def gcfind(name):
	name = name.replace(" ", "%20")
	search_url = "http://www.geocaching.com/seek/nearest.aspx?key={name}&submit4=Go"
	#search_url = "http://www.geocaching.com/seek/nearest.aspx?{name}"
	#name = "origin_lat=62.37991376122116&origin_long=17.334729739596927&dist=100"
	page = urlopen(search_url.format(name=name))
	soup = BeautifulSoup(page)
	page.close()

	table = soup.find("table", {"class": "SearchResultsTable Table"})
	if not table:
		return

	for tr in table.findChildren("tr", {"class": "Data"}):
		favs = int(tr.contents[5].findChild("span").text.strip())
		url = tr.contents[10].a["href"]
		name = tr.contents[10].a.text.strip()
		size, size_img = tr.contents[14].img["alt"][6:], tr.contents[14].img["src"]
		dt = map(float, tr.contents[14].span.text.split("/"))
		placed = tr.contents[16].span.text.strip()
		last_found = tr.contents[18].text.strip()
		nickname, code, location = tuple(map(lambda s: s.strip(), tr.contents[10].find("span", {"class": "small"}).text.split("|")))
		# Remove "By" from nickname
		nickname = nickname[3:]
		yield { "name": name, "favs": favs, "url": url,
			"size": size, "size_img": "http://www.geocaching.com" + size_img,
			"dt": dt, "placed": placed, "last_found": last_found,
			"nickname": nickname, "code": code, "location": location }

def main():
	from sys import argv, stderr
	if len(argv) != 2:
		print >> stderr, "Usage: gcfind.py query"
		return 1
	print json.dumps([c for c in gcfind(argv[1])])
	return 0

if __name__ == "__main__":
	exit(main())
