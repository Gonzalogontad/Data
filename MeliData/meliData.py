from gSheets import get_links_gsheet,saveCSV2gsheet
from meliCollect import meliCollect, melisave2csv,meli_csv_header
import os

json_file= os.path.dirname(os.path.abspath(__file__))+"/melitest.json"
csvPath =os.path.dirname(os.path.abspath(__file__))+'/data.csv'
props= ('id', 'price','sold_quantity','available_quantity','status','time_stamp')

def main ():
    links= get_links_gsheet(json_file,"Links",0)
    pubs2save = meliCollect(links, props)
    meli_csv_header(csvPath, props)
    melisave2csv(csvPath,pubs2save,props)
    saveCSV2gsheet(csvPath,props,json_file,'Datos',0)

if __name__ == "__main__":
    main()