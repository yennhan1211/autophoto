import os

defautPath = os.getcwd()

os.chdir(defautPath)

processFolderPath = os.path.join(defautPath, 'imgFolder')

if not os.path.exists(processFolderPath):
    print ('Create folder')
    os.makedirs(processFolderPath)

for root, dirs, files in os.walk('imgFolder'):
    for filename in files:
        print (filename)
    print (root)

# print (processFolderPath)