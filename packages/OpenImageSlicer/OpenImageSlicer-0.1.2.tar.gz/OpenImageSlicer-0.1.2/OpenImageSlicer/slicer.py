import os
from PIL import Image
from math import ceil

class Split:
    def __init__(self, array):
        self.split_array = array
        self.split_rows = len(array)
        self.split_cols = len(array[0])
    
    def get_count_rows(self):
        return self.split_rows
        
    def get_count_cols(self):
        return self.split_cols
    
    def get_array(self):
        return self.split_array
        
    def save(self, outpath, name="split"):
        if not os.path.exists(outpath):
            os.mkdir(outpath)
    
        for row in range(len(self.split_array)):
            for col in range(len(self.split_array[row])):
                tile = self.split_array[row][col]
                filename = name + '_' + str(row).zfill(len(str(self.get_count_rows()))) + "_" + str(col).zfill(len(str(self.get_count_cols()))) + ".jpg"
                filepath = os.path.join(outpath, filename)
                tile.save(filepath, "JPEG")

def split_image(inpath, cols, rows):
    image = Image.open(inpath)
    imgwidth, imgheight = image.size
    
    array = []
    
    height = ceil(float(imgheight) / rows)
    width = ceil(float(imgwidth) / cols)
    for i in range(0, imgheight, height):
        row = []
        for j in range(0, imgwidth, width):
            box = (j, i, j + width, i + height)
            try:
                a = image.crop(box)
                row.append(a)
            except Exception as e:
                print(e)
        array.append(row)
    
    return Split(array)