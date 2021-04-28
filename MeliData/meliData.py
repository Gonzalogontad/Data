from gSheets import get_links_gsheet,saveCSV2gsheet, saveDicts2gsheet
from meliCollect import meliCollect, melisave2csv,meli_csv_header
import os
import datetime

#JSON file to access google drive files
json_file= os.path.dirname(os.path.abspath(__file__))+"/melitest.json"

#Path to the folder where the data will be save
csvPath =os.path.dirname(os.path.abspath(__file__))+'/DataBackup/'

#Tuple of attributes to get from each advertise
props= ('id', 'price','sold_quantity','available_quantity','status','time_stamp')

def main ():
    #Get the links and collect the data from Mercado libre
    links= get_links_gsheet(json_file,"Links",0)
    pubs2save = meliCollect(links, props)

    #Create one data backup file per month
    date=datetime.datetime.now()
    csvFile= csvPath+f'Data {date.month}.{date.year}.csv' 
    if not os.path.isfile(csvFile): 
        meli_csv_header(csvFile, props)
    melisave2csv(csvFile,pubs2save,props)

    #Upload the data to Google sheets
    saveDicts2gsheet(pubs2save,props,json_file,'Datos',0)

if __name__ == "__main__":
    main()