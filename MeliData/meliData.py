from gSheets import get_links_gsheet,saveCSV2gsheet, saveDicts2gsheet
from meliCollect import meliCollect, melisave2csv,meli_csv_header
import os
import datetime

json_file= os.path.dirname(os.path.abspath(__file__))+"/melitest.json"
#csvPath =os.path.dirname(os.path.abspath(__file__))+'/data.csv'
csvPath =os.path.dirname(os.path.abspath(__file__))+'/'
props= ('id', 'price','sold_quantity','available_quantity','status','time_stamp')

def main ():
    links= get_links_gsheet(json_file,"Links",0)
    pubs2save = meliCollect(links, props)
    date=datetime.datetime.now()
    csvFile= csvPath+f'Data {date.month}.{date.year}.csv' 
    #
    if not os.path.isfile(csvFile):
        meli_csv_header(csvFile, props)
    melisave2csv(csvFile,pubs2save,props)
    saveDicts2gsheet(pubs2save,props,json_file,'Datos',0)

if __name__ == "__main__":
    main()