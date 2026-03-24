import requests
import bs4
import pandas as pd

#Sets up dictionary to put data into
dict = {}
dict['guide title'] = []
dict['guide url'] = []
dict['page title'] = []
dict['page url'] = []

#Prompts for filename input and then pulls in the entered file
#Input file should have a header of "guideURL" containing the URLs of the LibGuides you want information from
guideList = input("Enter filename for Spreadsheet containing LibGuides URLs ('.xlsx' extension will be added by script): ")
source = pd.read_excel(f"{guideList}.xlsx", keep_default_na=False)
guideURLs = source['guideURL'].astype(str)

#Loops through input file
#Goes through the guide's navigation and extracts the nav links
#Adds the guide URL, guide title, nav links, and their names to the dict
for y, guideURL in enumerate(guideURLs, 0):
    guideURL = guideURLs[y]
    res = requests.get(guideURL)

    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    try:
        raw_guideTitle = soup.find('h1', id="s-lg-guide-name")
        guideTitle = raw_guideTitle.getText()
    except AttributeError:
        guideTitle=""
    print(guideTitle)

    try:
        guideTabs = soup.find('div', id="s-lg-guide-tabs")

        navLinks = guideTabs.find_all('a')

        for k, navLink in enumerate(navLinks, 0):
            navLink = navLinks[k]

            guidePage = navLink.get('href')
            raw_pageName = navLink.getText()

            pageName = raw_pageName.strip()

            dict['guide title'].append(guideTitle)
            dict['guide url'].append(guideURL)
            dict['page title'].append(pageName)
            dict['page url'].append(guidePage)

    #Error handling~
    except AttributeError:
        dict['guide title'].append(guideTitle)
        dict['guide url'].append("")
        dict['page title'].append("")
        dict['page url'].append("")

#Creates a dataframe from the dict to export to an Excel file
df = pd.DataFrame(dict)

df.head()

pageList = input("Enter desired output filename ('.xlsx' will be added to the end)")
df.to_excel(f'{pageList}.xlsx', index=False)