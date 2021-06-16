import os
import matplotlib.pyplot as plt
os.add_dll_directory('C:/Users/Oh Seung Hwan/PycharmProjects/Anogan/venv/Lib/site-packages/openslide-win64-20171122/bin')
from openslide import OpenSlide
import numpy as np
from PIL import Image
import shutil
import cv2
from pytictoc import TicToc

t_list = ['META', 'NO TUMOR']
t = TicToc()

for i in t_list:
    major_list = os.listdir('D:/Anogan/img/'+i)
    for findex,flist in enumerate(major_list): # 2020
        tlist = os.listdir('D:/Anogan/img/'+ i +'/'+str(flist))

        for sindex, sflist in enumerate(tlist): # patient ID
            fflist = os.listdir('D:/Anogan/img/'+ i +'/' + str(flist) + '/' + str(sflist))

            for eindex, eflist in enumerate(fflist): # patient File

                if not (os.path.isdir('D:/Anogan/img/'+i+'_2/'+flist+'/' + str(sflist))):
                    os.makedirs('D:/Anogan/img/'+i+'_2/'+flist+'/' + str(sflist))
                if "FS" in eflist:
                    t.tic()
                    img = OpenSlide('D:/Anogan/img/'+ i +'/' + str(flist) + '/' + str(sflist) +'/' + str(eflist))
                    size0, size1, size2, size3 = img.level_dimensions
                    image = np.asarray(img.get_thumbnail(size3))
                    image2 = np.asarray(img.get_thumbnail(size0))
                    ret, binary = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 150, 255, cv2.THRESH_OTSU)
                    contours, hierarchy = cv2.findContours(~binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    x, y, w, h = cv2.boundingRect(contours[0])
                    cv2.rectangle(cv2.drawContours(image.copy(), contours, 0, (255, 0, 255), 3), (x, y), (x + w, y + h), (255, 0, 0), 5)
                    count = 0
                    for c in contours:
                        x, y, w, h = cv2.boundingRect(c)
                        if (cv2.contourArea(c)) > 50000:
                            count += 1
                            pil_image = Image.fromarray(image2[(size0[1] // size3[1]) * y:(size0[1] // size3[1]) * y + (size0[1] // size3[1]) * h,(size0[0] // size3[0]) * x: (size0[0] // size3[0]) * x + (size0[0] // size3[0]) * w])
                            pil_image.save('D:/Anogan/img/' + i + '_2/' + flist + '/' + str(sflist) + '/' + str(eflist) + '_'+str(count)+'.jpg')
                    t.toc()
                img = 0
                image = 0
                image2 = 0
                pil_image = 0

'''
import os
import matplotlib.pyplot as plt
os.add_dll_directory('C:/Users/Oh Seung Hwan/PycharmProjects/Anogan/venv/Lib/site-packages/openslide-win64-20171122/bin')
from openslide import OpenSlide
import numpy as np
from PIL import Image
import shutil

major_list = os.listdir('D:/Anogan/img/NO TUMOR')

t_list = ['META', 'NO TUMOR']

for i in t_list:
    for findex,flist in enumerate(major_list): # 2020
        tlist = os.listdir('D:/Anogan/img/'+ i +'/'+str(flist))

        for sindex, sflist in enumerate(tlist): # patient ID
            fflist = os.listdir('D:/Anogan/img/'+ i +'/' + str(flist) + '/' + str(sflist))

            for eindex, eflist in enumerate(fflist): # patient File
                if not (os.path.isdir('D:/Anogan/img/'+i+'_2/'+flist+'/' + str(sflist))):
                    os.makedirs('D:/Anogan/img/'+i+'_2/'+flist+'/' + str(sflist))
                if "FS" in eflist:
                    shutil.copy('D:/Anogan/img/'+ i +'/' + str(flist) + '/' + str(sflist) +'/' + str(eflist) , 'D:/Anogan/img/'+i+'_2/'+flist+'/' + str(sflist))

'''