import gspread
import json
import csv
import os



json_file= os.path.dirname(os.path.abspath(__file__))+"/melitest.json"
csvPath =os.path.dirname(os.path.abspath(__file__))+'/data.csv'
props= ('id', 'price','sold_quantity','available_quantity','status','time_stamp')

def open_sheet(file, worksheet, json_file):
    gc = gspread.service_account(filename=json_file)
    sheet=gc.open(file)
    worksheet=sheet.get_worksheet(worksheet)
    return worksheet

def get_links_gsheet (json_file, gsheet_file, worksheet):
    ws = open_sheet (gsheet_file,worksheet,json_file)
    links=ws.get_all_records()
    return [(link['Link'],link['Name']) for link in links]


def saveDicts2gsheet (list_of_rows, fieldnames, json_file, gsheet_file, worksheet):
    ws = open_sheet (gsheet_file,worksheet,json_file)
    rows=[]
    for list_row in list_of_rows:
        row=[]
        for key in fieldnames:
            row.append(list_row[key])
        rows.append (row)

    ws.append_rows(rows)



def saveCSV2gsheet (csv_file, fieldnames, json_file, gsheet_file, worksheet):
    with open(csv_file, newline='') as csvfile:
        csvdata = csv.DictReader(csvfile)
        ws = open_sheet (gsheet_file,worksheet,json_file)
        rows=[]
        for csv_row in csvdata:
            row=[]
            for key in fieldnames:
                row.append(csv_row[key])
            rows.append (row)

        ws.append_rows(rows, value_input_option='USER_ENTERED')




def main():
    urls= get_links_gsheet(json_file,"Links",0)
    print (urls)
    saveCSV2gsheet (csvPath,props,json_file,"Datos",0)
    """
    w=open_sheet("CollectedData", 1, json_file)
    items=w.get_all_values()
    print (items)
    w.append_row(items[0])
    items=w.get_all_values()
    print (items)
    """
    #list_of_dicts = w.get_all_records()
    #print (list_of_dicts)
#    w.update_cell(1, 2, 'Bingo!')
 #   list_of_dicts = w.get_all_records()
  #  print (list_of_dicts)

if __name__ == "__main__":
    main()
