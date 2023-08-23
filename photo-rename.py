# This script will take all of the files with ".jpg" in the file name in the directory and
# subdirectories and rename them using the photo taken date time derived from the Exif
# CHECK PATHS AND TEST FIRST.


import os
import PIL.Image
from PIL.ExifTags import TAGS
from datetime import datetime
from datetime import timedelta


# directory_items = os.listdir('.')
# for item in directory_items:
#     if os.path.isdir(os.path.join(os.path.abspath('.'),item)):
#         print(item)


def get_exif_datetime_as_object(r, file):
    # Takes the path to the file and the file name itself.
    # Returns a datetime object based on the EXIF data.

    img = PIL.Image.open(os.path.join(r, file))
    exif = img._getexif()
    # print(exif) # Show the EXIF object. Sometimes the object, or 36867 is missing. Need to handle this.
    return datetime.strptime(exif[36867], '%Y:%m:%d %H:%M:%S')

# Adjustment loop. Input: rename? Yes
# Change time. Show output. Happy?
# Yes: Adjust all for real


def setup_adjust_datetime(datetime_object):
    happy = 'n'
    while happy == 'n':
        print("Original: ", datetime_object)
        adjustment_string = input("What's the adjustment? [days,mins]")
        datetime_object_temp = datetime_object + timedelta(days=int(adjustment_string.split(',')[0]), minutes=int(adjustment_string.split(',')[1]))
        print("Update: ", datetime_object_temp)
        happy = input("Happy with this? [y, n]")
        if happy == 'y':
            days_delta = int(adjustment_string.split(',')[0])
            minutes_delta = int(adjustment_string.split(',')[1])
    return days_delta, minutes_delta

def adjustment_test(target_folder_path):
    file_target = input("Target file name?")
    for r, d, f in os.walk(target_folder_path):
        for file in f:
            print("Trying: " + file)
            if file_target in file:
                try:
                    datetime_object = get_exif_datetime_as_object(r, file)
                    days_delta, minutes_delta = setup_adjust_datetime(datetime_object)
                    print("Adjusting by {} days {} mins".format(days_delta, minutes_delta))
                except KeyError:
                    pass
    return None


def rename_photos(target_folder_path):
    rename_all = False
    for r, d, f in os.walk(target_folder_path):
        for file in f:
            print("Processing: " + file)
            if ' -- ' in file:
            	pass
            # elif 'IMG_' in file:
            # 	tempFileName = file.lower().split('.jpg')[0]
            # 	splitFileName = tempFileName.lower().split('_')
            # 	if len(splitFileName) == 4:
            # 		os.rename(os.path.join(r, file), os.path.join(r, splitFileName[1][2:] + '-' + splitFileName[2]) + ' -- ' + splitFileName[3] + ' - img.jpg')            		
            # 	elif len(splitFileName) == 3:
            # 		os.rename(os.path.join(r, file), os.path.join(r, splitFileName[1][2:] + '-' + splitFileName[2]) + ' -- img.jpg')
            # 	else:
            # 		print("#"*10 + ' SOMETHING BAD')				

            elif 'dsc_' in file or 'DCS_' in file:
                try:
                    datetime_object = get_exif_datetime_as_object(r, file)
                    print('Processing: ', os.path.join(r, file), '  |  ', datetime_object)
                    os.rename(os.path.join(r, file), os.path.join(r, datetime_object.strftime("%y%m%d-%H%M%S") + ' -- ' + file.lower().split('.jpg')[0] + '.jpg'))
                except KeyError:
                    print("Error processing: ", file)
                    pass
            elif ('DSC' in file or 'dsc' in file) and ('.JPG' in file or '.jpg' in file):
                # setup the local instance of the variables
                try:
                    # Let's first attempt to get the datatime from the file
                    datetime_object = get_exif_datetime_as_object(r, file)
                    if rename_all == False:
                        days_delta, minutes_delta = setup_adjust_datetime(datetime_object)
                        rename_all = True

                    print("Adjusting by {} days {} mins".format(days_delta, minutes_delta))

                    # Use these to adjust if the camera EXIF datetime is not setup correctly.
                    datetime_object = datetime_object + timedelta(days=days_delta, minutes=minutes_delta)

                    # print('Old: ', os.path.join(r, file), '  |  ', datetime_object)
                    # print('New: ', os.path.join(r, datetime_object.strftime("%y%m%d-%H%M%S") + ' - ' + file.split(' - ')[1]))
                    # This next line is for a renaming
                    os.rename(os.path.join(r, file), os.path.join(r, datetime_object.strftime("%y%m%d-%H%M%S") + ' -- ' + file.lower().split('.jpg')[0] + '.jpg'))
                    # os.rename(os.path.join(r, file), os.path.join(r, datetime_object.strftime("%y%m%d-%H%M%S") + ' - ' + file.split(' - ')[1]))
                except KeyError:
                    print("Error processing: ", file)
                    pass
            elif '.jpg' in file or '.JPG' in file:
                try:
                    datetime_object = get_exif_datetime_as_object(r, file)
                    print('Processing: ', os.path.join(r, file), '  |  ', datetime_object)
                    os.rename(os.path.join(r, file), os.path.join(r, datetime_object.strftime("%y%m%d-%H%M%S") + ' -- ' + file.lower().split('.jpg')[0] + '.jpg'))
                except KeyError:
                    print("Error processing: ", file)
                    pass
            elif '.png' in file:
                try:
                    # datetime_object = get_exif_datetime_as_object(r, file)
                    print(os.path.join(r, file), '  |  PNG')
                except KeyError:
                    print("Error processing: ", file)
                    pass
            else:
                pass

def fix_name(target_folder_path):
    # Rolls back the name if something went wrong
    for r, d, f in os.walk(target_folder_path):
        for file in f:
            print("Processing: " + file)
            if ' -- ' in file:
                os.rename(os.path.join(r, file), os.path.join(r, file.split(' -- ')[1]))

# adjustment_test('INSERT PATH')
rename_photos('/Users/xwu1/Dropbox/Photos/Google Photos/2007')
# fix_name('INSERT PATH')

# TODO: Fix handling when the file does not have the correct EXIF object.
