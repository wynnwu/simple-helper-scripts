import os

# For organizing Android screenshots with the following format: Screenshot_20210430-234106_Vivino.jpg
# Two underlines in name.
# All of the screenshot files should be in a subfolder called 'screenshots'

if not os.path.exists('screenshots'):
    print('Must have a subfolder named "screenshots". Quitting now.')
    exit()

files = os.scandir('screenshots/')

counter = 0
counterAll = 0

for entry in files:
    if entry.is_file() and entry.name.split('.')[1] == 'jpg':
        print(f"Processing: {entry.name}")
        # print(entry.name.split('.')[0].split('_')[2])
        counterAll += 1
        if len(entry.name.split('.')[0].split('_')) == 3:
            folderName = entry.name.split('.')[0].split('_')[2]
            if not os.path.exists('screenshots/' + folderName):
                os.makedirs('screenshots/' + folderName)

            os.rename('screenshots/' + entry.name, 'screenshots/' + folderName + '/' + entry.name)
            counter += 1

print('\n' + '===='*5)
print (f'Done! \n{counter} files sorted into folders. \n{counterAll} files total.')
print('===='*5)