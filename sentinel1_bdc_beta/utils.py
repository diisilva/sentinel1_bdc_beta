import os
import shutil
from datetime import datetime
from pathlib import Path

from .process import imageProcess

def imageSearch(folder, extension):
    images_list = []
    for images in os.listdir(folder):
        if images.endswith(extension):
            images_list.append(folder + '/' + images)
    print("Image list: " + str(images_list))
    return images_list

def createS1Imglist(inputfolder='', extension='zip'):
    s1list = []
    images_list = imageSearch(inputfolder, extension)  # The goal here is to fetch a list of path and give it to our variable object
    for path in images_list:
        s1list.append(imageProcess(path))
    return s1list, images_list

def get_auxfile_date(string):
    strsplit = string.split('.')[0].split('_')
    dates= {'start':datetime.strptime(strsplit[6].replace('V','').replace('T',''),'%Y%m%d%H%M%S'),
            "end":datetime.strptime(strsplit[7].replace('T',''),'%Y%m%d%H%M%S')}
    return dates

def search_and_inject_auxfiles(img_info,aux_path):
    img_sensor = img_info.split('_')[0]
    img_date = img_info.split('_')[4].replace('T','')
    img_datetime = datetime.strptime(img_date, '%Y%m%d%H%M%S')
    print(f'looking for {img_datetime}')
    search_path = os.path.join(aux_path,img_sensor,str(img_datetime.year),str('{:02d}'.format(img_datetime.month)))
    listed_aux_files = os.listdir(search_path)
    for file_name in listed_aux_files:
        auxdate = get_auxfile_date(file_name)
        if auxdate['start'] < img_datetime < auxdate['end']:
            print(f'found  Start: {auxdate["start"]} - End: {auxdate["end"]} \n')
            break
    snap_folder = os.path.join('/home/jovyan/.snap/auxdata/Orbits/Sentinel-1/POEORB',img_sensor,str(img_datetime.year),str('{:02d}'.format(img_datetime.month)))
    final_file_path = os.path.join(search_path,file_name)
    inject_auxfiles(final_file_path,file_name, snap_folder)


def inject_auxfiles(source,file_name, destination):
    print(destination)
    Path(destination).mkdir(parents=True, exist_ok=True)
    destination_final = os.path.join(destination,file_name)
    shutil.copyfile(source, destination_final)

# not used for now
def createstack(polarisation, stack):
    if os.path.isfile(input_dir + "/+" + polarisation + 'stack*'):
        print("file already exists")
    else:
        print("creating stack")
        # initialisation des parametres
        parameters = HashMap()  # initialise le dico pour les parametres
        parameters.put('extent', 'Master')
        parameters.put('initialOffsetMethod', 'Product Geolocation')
        parameters.put('ResamplingType', 'None')
        parameters.put('FindOptimalMaster', 'True')
        # recherche des images pour le stack
        create_stack = GPF.createProduct("CreateStack", parameters, stack)
        output = input_dir + '/stackVV'
        ProductIO.writeProduct(create_stack, output, 'BEAM-DIMAP')
