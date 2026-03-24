import requests
import os
import bs4
import re
import pandas as pd

#Create subdirectory to download PDFs to (will create in current directory)
os.makedirs('libfiles', exist_ok=True)

#Pull in list of all guide pages to check for .docx and .pdf files
pageList = input("Enter filename for Spreadsheet containing LibGuides URLs ('.xlsx' extension will be added by script): ")
source = pd.read_excel(f"{pageList}.xlsx", keep_default_na=False)
guidepageURLs = source['page url'].astype(str)
guidepageNames = source['page title'].astype(str)

#Create dict to put information in
dict2 = {}
dict2['on page- title'] = []
dict2['on page- url'] = []
dict2['item ID'] = []
dict2['item label'] = []
dict2['file type'] = []
dict2['save status'] = []

#Loops through input data of guide page URLs
#Looks for files to attempt downloading them, grabbing the asset ID and link text in the process
for w, guidepageURL in enumerate (guidepageURLs, 0):
    guidepageURL = guidepageURLs[w]
    guidepageName = guidepageNames[w]
    
    res = requests.get(guidepageURL)

    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    #Look for PDFs first
    try:
        pdfs = soup.find_all('i', class_="fa-file-pdf-o")

        for i, pdf in enumerate (pdfs, 0):
            pdf = pdfs[i]

            tag_link = pdf.find_parent()

            raw_name = tag_link.getText()
            name = raw_name.strip()

            link = tag_link.get('href')

            raw_sysID = re.findall(r'\d+', link)
            sysID = raw_sysID[0]

            res = requests.get(link)
            res.raise_for_status()


            try:
                # Save the image to ./libfiles.
                # First attempt to name the file with the asset ID and link text
                imageFile = open(os.path.join('libfiles', os.path.basename(f"{sysID}- {name}.pdf")), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                dict2['on page- title'].append(guidepageName)
                dict2['on page- url'].append(guidepageURL)
                dict2['item ID'].append(sysID)
                dict2['item label'].append(name)
                dict2['file type'].append('PDF')
                dict2['save status'].append('Saved')

            # If link text give an error as a filename, just use the asset ID
            except ValueError:
                imageFile = open(os.path.join('libfiles', os.path.basename(f"{sysID}.pdf")), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                dict2['on page- title'].append(guidepageName)
                dict2['on page- url'].append(guidepageURL)
                dict2['item ID'].append(sysID)
                dict2['item label'].append(name)
                dict2['file type'].append('PDF')
                dict2['save status'].append('Saved with Error')
            
            # Another error handling for exceptions
            except OSError:
                imageFile = open(os.path.join('libfiles', os.path.basename(f"{sysID}.pdf")), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                dict2['on page- title'].append(guidepageName)
                dict2['on page- url'].append(guidepageURL)
                dict2['item ID'].append(sysID)
                dict2['item label'].append(name)
                dict2['file type'].append('PDF')
                dict2['save status'].append('Saved with Error')
    except AttributeError:
        pass

    # Now, try for any .docx files...
    try:
        docxs = soup.find_all('i', class_="fa-file-word-o")
        print(docxs)

        for x, pdf in enumerate (docxs, 0):
            docx = docxs[x]

            tag_link = docx.find_parent()

            raw_name = tag_link.getText()
            name = raw_name.strip()
            print(name)

            link = tag_link.get('href')
            #name = tag_link.a.getText()
            print(link)

            raw_sysID = re.findall(r'\d+', link)
            sysID = raw_sysID[0]
            print(sysID)


            res = requests.get(link)
            res.raise_for_status()

            try:
                # Save the image to ./libfiles.
                imageFile = open(os.path.join('libfiles', os.path.basename(f"{sysID}- {name}.docx")), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                dict2['on page- title'].append(guidepageName)
                dict2['on page- url'].append(guidepageURL)
                dict2['item ID'].append(sysID)
                dict2['item label'].append(name)
                dict2['file type'].append('DOCX')
                dict2['save status'].append('Saved')
            except ValueError:
                imageFile = open(os.path.join('libfiles', os.path.basename(f"{sysID}.docx")), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                dict2['on page- title'].append(guidepageName)
                dict2['on page- url'].append(guidepageURL)
                dict2['item ID'].append(sysID)
                dict2['item label'].append(name)
                dict2['file type'].append('DOCX')
                dict2['save status'].append('Saved with Error')

            except OSError:
                imageFile = open(os.path.join('libfiles', os.path.basename(f"{sysID}.docx")), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                dict2['on page- title'].append(guidepageName)
                dict2['on page- url'].append(guidepageURL)
                dict2['item ID'].append(sysID)
                dict2['item label'].append(name)
                dict2['file type'].append('DOCX')
                dict2['save status'].append('Saved with Error')
    except AttributeError:
        pass

# Convert dict to dataframe to save to Excel
df2 = pd.DataFrame(dict2)

df2.head()

fileResults = input("Enter desired output filename ('.xlsx' will be added to the end)")
df2.to_excel(f'{fileResults}.xlsx', index=False)