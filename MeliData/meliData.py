#from Data.MeliData.meliCollect import meli_scrap
from meliCollect import meliURL2ID
from gSheets import get_links_gsheet,saveCSV2gsheet, saveDicts2gsheet,update_table_gsheet
from meliCollect import meliCollect, melisave2csv,meli_csv_header, meli_scrap
import os
import datetime

#JSON file to access google drive files
json_file= os.path.dirname(os.path.abspath(__file__))+"/melitest.json"

#Path to the folder where the data will be save
csvPath =os.path.dirname(os.path.abspath(__file__))+'/DataBackup/'

#Tuple of attributes to get from each advertise
props= ('id', 'price','sold_quantity','available_quantity','status','time_stamp','Name')
props_id_name= ('id', 'Name')

def main ():
    #Get the links and collect the data from Mercado libre
    links= get_links_gsheet(json_file,"Links",0)
    urls = [link['Link'] for link in links]
    #pubs2save = meliCollect(urls, props) #The use of Melis API was replaced for the scrapig option below
    pubs2save = meli_scrap(urls, props)

    #Create one data backup file per month
    date=datetime.datetime.now()
    csvFile= csvPath+f'Data {date.month}.{date.year}.csv' 
    if not os.path.isfile(csvFile): 
        meli_csv_header(csvFile, props)
    melisave2csv(csvFile,pubs2save,props)

    #Upload the data to Google sheets
    saveDicts2gsheet(pubs2save,props,json_file,'Datos',0)

    #Updating the name and ID table
    for link in links:
        link['id']=meliURL2ID(link['Link'])
    
    update_table_gsheet (links, props_id_name,json_file, 'Datos', 1)
    
if __name__ == "__main__":
    main()