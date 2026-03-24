import requests
import bs4
import pandas as pd

#Pull in list of all guide pages to check for embedded widgets
pageList = input("Enter filename for Spreadsheet containing LibGuides URLs ('.xlsx' extension will be added by script): ")
source = pd.read_excel(f"{pageList}.xlsx", keep_default_na=False)
guidepageURLs = source['page url'].astype(str)
guidepageNames = source['page title'].astype(str)


#Create dict to put data in
dict2 = {}
dict2['on page- title'] = []
dict2['on page- url'] = []
dict2['widget ID'] = []
dict2['embed url'] = []

#Loop through input file info to check for embedded widgets, extracting the information to put in the dict
for w, guidepageURL in enumerate (guidepageURLs, 0):
    guidepageURL = guidepageURLs[w]
    guidepageName = guidepageNames[w]

    res = requests.get(guidepageURL)

    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    #Look for the widgets, grab the ID, look for the embedded iframe, grab the src url
    try: 
        widgets = soup.find_all('div', class_="s-lg-widget")

        for i, widget in enumerate (widgets, 0):
            widget = widgets[i]
            widgetid = widget['id']
            print(widgetid)
            dict2['widget ID'].append(widgetid)

            iframe = widgets[0].find('iframe')

            try: 
                vidsrc = iframe['src']
                print(vidsrc)
                dict2['embed url'].append(vidsrc)
            except TypeError:
                dict2['embed url'].append("NO SRC FOUND")

            dict2['on page- title'].append(guidepageName)
            dict2['on page- url'].append(guidepageURL)

        
    except AttributeError:
        pass

df2 = pd.DataFrame(dict2)

df2.head()

widgetResults = input("Enter desired output filename ('.xlsx' will be added to the end)")
df2.to_excel(f'{widgetResults}.xlsx', index=False)