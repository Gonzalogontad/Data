import requests as rq
import json
from datetime import datetime
import re
import csv
import time
from functools import lru_cache


#Attributes to capture from Mercado Libre API
props= ('id', 'price','sold_quantity','available_quantity','status','time_stamp')



# Request items data from Mercado Libre API by item 'id' or 'url' list.
# 'props' is the tuple of attributes that will be filtered
def meliCollect(ids_urls,props):

    pubs2save=[]
        
    ids_urls= [meliURL2ID(id_url) for id_url in ids_urls if meliURL2ID(id_url) ] #Extract the IDs from the URLs valid
    
    for i in range (0, len (ids_urls), 20 ):
        url= 'https://api.mercadolibre.com/items?ids=' #form the url for the request (max 20 ids per request)
        for id_url in ids_urls [i:i+20]:
            url=url+id_url+','   
                
        try:
            pubs=rq.get(url).json() #get a list of dicts from mercadolibre API
        except rq.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
            return None
        except rq.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            return None
        except rq.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            return None
        except rq.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
            return None

        if(type(pubs) != type(list())): #if the answer isn't a list of dicts means that there is an error
            continue

        pub2save={}
        for pub in pubs:
            for k in props:
                pub2save[k]=pub['body'].get(k,'NO_DATA')    #Get the elements by key in props
            pub2save['time_stamp']=datetime.now().isoformat(timespec='seconds')  #timestamp isn't in the API response so it's added here

            pubs2save.append(dict(pub2save)) #Construct a list with the data collected

    return pubs2save

#Transform an URL to an ID, if an ID is used as argument it returns the ID whithout the "-" or 
# "none" if the URL has no ID
@lru_cache(maxsize=1) #Catchin the last result speedup the use in comprehesion list double use.
def meliURL2ID(url):
    id=re.search(r'MLA[-]?[1234567890]+', url)
    if id:
        id=id.group().replace('-','')

    return id


#Save the collected data to a CSV file
def melisave2csv (file,dataCollected, fieldnames):
    with open(file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerows(dataCollected)


#Create or replace a CSV file with the header defined in fieldnames argument
def meli_csv_header (file, fieldnames):
    #Erase the file an save the headers
    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()



#Here start the module test.

csvPath = 'data.csv'

urls=[
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-006539602-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-836539602-sensor-movimiento-huayra-pared-infrarrojo-ip65-180-led-_JM#position=1&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-868633841-sensor-de-movimiento-de-pared-apto-led-exterior-oferta-_JM#position=2&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-870908057-sensor-de-movimiento-360-infrarrojo-presencia-_JM#position=3&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-836559198-sensor-movimiento-huayra-infrarrojo-interior-360-apto-led-_JM#position=4&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-836497568-sensor-de-movimiento-pared-infrarrojo-ip65-180-cuotas-_JM#position=5&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-870941055-control-remoto-para-sensor-de-movimiento-presencia-_JM#position=6&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-870910961-sensor-de-movimiento-360-presencia-infrarrojo-_JM#position=7&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-836554574-sensor-de-movimiento-aplicar-infrarrojo-360-ip65-pack-x3-_JM#position=8&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-750859545-sensor-de-movimiento-huayra-shf-002-360-para-techo-apto-led-_JM#position=9&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-851836402-plafon-led-16w-aplicar-techo-redondo-con-sensor-mov-_JM?searchVariation=54723832241#searchVariation=54723832241&position=10&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-874223136-sensor-movimiento-360-infrarrojo-presencia-control-cuotas-_JM#position=11&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-884160516-sensor-de-movimiento-360-presencia-aplicar-control-cuotas-_JM#position=12&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-875914305-sensor-de-movimiento-360-infrarrojo-presencia-_JM#position=13&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-836554577-sensor-movimiento-aplicar-infrarrojo-360-ip65-pack-x3-cuotas-_JM#position=14&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-874222759-sensor-movimiento-360-infrarrojo-presencia-control-cuotas-_JM#position=15&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-835896204-sensor-de-movimiento-embutir-alta-frecuencia-apto-led-_JM#position=16&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-874222725-sensor-de-movimiento-360-infrarrojo-presencia-control-_JM#position=17&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-870939488-control-remoto-para-sensor-de-movimiento-presencia-cuotas-_JM#position=18&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-855442597-sensor-de-movimiento-embutir-huayra-apto-led-_JM#position=19&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-879925072-sensor-de-movimiento-de-alta-frecuencia-huayra-rh-l01-_JM#position=20&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-879921274-sensor-de-movimiento-de-alta-frecuencia-huayra-rh-l02-_JM#position=21&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
'https://articulo.mercadolibre.com.ar/MLA-874223602-sensor-movimiento-360-presencia-aplicar-control-pack-x10-_JM#position=22&type=item&tracking_id=06fab054-5c21-46d9-bf29-1495b15ff8bb',
]


if __name__ == "__main__":

    #Get the data    
    dataCollected= meliCollect(urls,props)
    if dataCollected:
        for data in dataCollected:
            print (data)

        #Save de data in the CSV file
        melisave2csv (csvPath,dataCollected, props)


