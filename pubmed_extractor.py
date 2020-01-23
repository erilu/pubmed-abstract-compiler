# Test edit
# Erick Lu
# pubmed_extractor.py

# SAMPLE SEARCH FUNCTION:

"""
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=P2RY8&usehistory=y&retmin=0&retmax=500
"""

# SAMPLE FETCH FUNCTION:

'''
http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&WebEnv=NCID_1_196289963_130.14.18.34_9001_1524513200_1515294449_0MetA0_S_MegaStore&query_key=1&retmode=json&rettype=abstract
'''

# Import the necessary packages.
import csv
import re
import urllib
import os
from time import sleep


# Gather all the terms that you want to search Pubmed for.
terms = ["P2RY8"]

numfailed = 0
for item in terms:

    	#Create the csv file that will hold the categorized abstracts.

       # myfile = open ( str(item) + " abstracts.csv", 'wb')
       # master_file = csv.writer(myfile, delimiter = ',')
        datefile = open ('P2RY8abstracts.txt', 'w')
       # errorfile = open("error2.txt", 'w')
        #Write the names for each column in the CSV file.
       # master_file.writerow(["Journal", "Title", "Authors", "Organization", "Abstract", "PMID" ])

        #The set of static variables needed for the ESearch function:
        baseURL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        eutil_search = 'esearch.fcgi?'
        db_setting = 'db=pubmed'
        usehistory_setting = '&usehistory=y'
        rettype = '&rettype=json'
        eutil_fetch = 'efetch.fcgi?'


        term_setting = '&term='+ str(item)
        retmax = 500
        retstart = 0
        run = True
        while run:

                #Print the URL to check in terminal incase of error.
                print (baseURL+eutil_search+db_setting+term_setting+usehistory_setting)


                #Open the webpage that will run the ESearch Function.

                f = urllib.urlopen (baseURL+eutil_search+db_setting+term_setting+usehistory_setting+rettype)
                data = f.read().decode('utf-8')

                #Print the search to the terminal (debugging purposes)
                print (data)

                #Extract the Web Env and querykey  (Tracking Search), and count (for iteration),
                webenv = "&WebEnv=" + re.findall ("<WebEnv>(\S+)<\/WebEnv>", data)[0]
                count = int(re.findall("<Count>(\d+?)</Count>",data)[0])
                querykey = "&query_key=" + re.findall("<QueryKey>(\d+?)</QueryKey>",data)[0]

                #webenv = 'NCID_1_811107105_130.14.22.33_5555_1351061178_277739021'

                #retrieve the data. Retmax = the number of abstracts returned. Retstart =
                # the index at which retmax begins.


                #Reset some parameters for the EFetch utility. many of parameters will be recycled from above.

                rettype = "&rettype=abstract"
                str_retmax = "&retmax=" + str(retmax)
                retmode = "&retmode=text"


                str_retstart = "&retstart=" + str(retstart)
                fetch_url = baseURL+eutil_fetch+db_setting+querykey+webenv+str_retstart+str_retmax+retmode+rettype

                #Print the url for debugging purposes.
                print (fetch_url)

                print ("sleeping for 5 seconds")
                sleep(3)


                #To ensure the program runs to completion, use a try/except clause.
                #The program will try to extract from the KB, and write to the csv file.
                #If there is an error in the extraction, a non-halting error will be thrown
                #containing the index at which the extraction error occured.
                try:
                        #Open the webpage with the fetch utility.
                        fetch = urllib.urlopen (fetch_url)
                        failed = False
                        #Decode the data returned by the fetch command.
                        datam = fetch.read().decode('utf-8')
                        #print(datam)
                        #Strip off Unnecessary text.
                        #chunk = datam[62:-20]

                        #Split the data into individual abstracts.
                        chunks = datam.split("[PubMed")
                        if len(chunks) < 100:
                                print(str(retstart))
                                failed = True


                        #print ((len(chunks)-4))
                        #For each abstract, split the individual abstract and write it to the CSV file,
                        #Categorized by Journal, Title, Author, Organization, Abstract, and PMID.
                        for i in range(0, (len(chunks)-4)):
                        #To obtain categories, split every double newline.
                                splitchunk = chunks[i].split("\n\n")[1:2]
                                #splitchunk = [f for f in splitchunk if f != ""]


                                #Some of the abstracts returned either are incomplete or have no information.
                                #A full abstract will have All six categories.
                                #The abstracts that have less than 5 categories will be ignored because of
                                #Insufficient information.
                                #The abstracts with only 5 categories have been found to be missing information
                                #on the organization from which they came from. I will add them to the CSV file
                                datefile.write(" ".join(splitchunk))
                                datefile.write("\n")


                               # master_file.writerow(splitchunk)
                                #print(splitchunk)
                        if failed == True:
                                datefile.write("\n Failed at " + str(retstart) + "\n\n")
                        else:
                                datefile.write("\n Success at " + str(retstart) + "\n\n")

                #The except clause explained above.

                except:
                        print ("Error at retstart:", retstart)
                        datefile.write("\n Failed at " + str(retstart) + "\n")
                        numfailed = numfailed +1
                #If the return index is higher than the total number of indexes, then break the loop and exit.
                #break
                if retstart > count:
                        break
                #If it is not, then update retstart and perform the actions again.
                retstart = retstart+retmax
                print ("sleeping for 3 seconds")
                sleep(3)


        #NOTE: EFETCH automatically cuts off if retmax is over the total number of articles remaining. It will not error.
        datefile.close()
        #errorfile.close()


print (numfailed)
