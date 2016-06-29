import urllib2
import re  # this actually stands for regular expression
from bs4 import BeautifulSoup

# -----------------------------------------------------------
def returnGroupIcon2(url2):
        try:
                url = "http://www." + url2 + ".deviantart.com"
                sock = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
                print "\n" + url2 + " needs to be deleted"
                return ""
        else:
                soup = BeautifulSoup(sock.read(), 'html.parser')
                # returns an array of three strings, i.e.:
                #['21  Members', '21  Watchers', '66  Pageviews']
                stats = filter(None,str((soup.find("div", {"id": "super-secret-stats"})).get_text()).split("\n"))
                icon_url = soup.find("meta",{"property":"og:image"})['content']
                if icon_url == 'http://a.deviantart.net/avatars/default.gif':
                        return 'http://a.deviantart.net/avatars/default_group.gif'
                else:
                        return icon_url

print returnGroupIcon2('foggao')

