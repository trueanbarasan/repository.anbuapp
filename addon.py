# Addon: My Python Kodi Add-on
# Author: Anbu
#----------------------------------------------------------------

import sys
import urllib
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin

import xbmcaddon

import urllib2
from bs4 import BeautifulSoup


# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')
_addonID = _addon.getAddonInfo('id')
_icon = _addon.getAddonInfo('icon')
_fanart = _addon.getAddonInfo('fanart')
_path = _addon.getAddonInfo('path')


category = {'01mov': 'Movies',
         '02ltv': 'Live Tv'	
}


#Get Movies from Tamil Gun
url = "http://tamilgun.work/categories/hd-movies/"

req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
page = urllib2.urlopen( req )

page_soup = BeautifulSoup(page, 'html.parser')

movies = []

items = page_soup.find_all('div', class_='row')

for item in items:
    for container in item.findAll('div', class_='col-lg-3 col-md-3 col-sm-12 item'):
        movies.append({'name': container.section.h3.a['title'],
                                  'video': container.section.h3.a['href']})


def list_category():
    """
    Create the Pages menu in the Kodi interface.
    """
    listing = []
    for page,title in sorted(category.iteritems()):
	    list_item = xbmcgui.ListItem(label=title)
	    list_item.setArt({'icon': _icon,
	                      'fanart': _fanart})
	    url = '{0}?action=1&page={1}'.format(_url, page[2:])
	    is_folder = True
	    listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def list_movies(page):
    if page == 'mov':
        """
        Create the Movies menu in the Kodi interface.
        """
        listing = []
        for item in movies:
    	    list_item = xbmcgui.ListItem(label=item['name'])
    	    list_item.setArt({'icon': _icon,
    	                      'fanart': _fanart})
            list_item.setInfo('video', {'title': item['name']})
            list_item.addStreamInfo('video', { 'codec': 'h264'})
            list_item.setProperty('IsPlayable', 'true')
    	    url = '{0}?action=2&page={1}'.format(_url, item['video'])
#            list_item.addContextMenuItems([('Save Video', 'RunPlugin(plugin://'+_addonID+'/?action=3&page='+item['video']+'ZZZZ'+item['name']+')',)])
    	    is_folder = False
    	    listing.append((url, list_item, is_folder))

        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)

def play_video(iurl, dl=False):
    title = 'unknown'
    play_item = xbmcgui.ListItem(path=iurl)
    vid_url = play_item.getfilename()
    play_item.setPath(vid_url)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def router(paramstring):
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin

    if params:
        if params['action'] == '1':
            list_movies(params['page'])
        elif params['action'] == '2':
            list_movies(params['page'])
    else:
        list_category()

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
    

