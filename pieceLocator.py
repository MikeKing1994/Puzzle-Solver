#here we will write a script to compare the split up images with the image of the individual piece
import os

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES
from image_match.goldberg import ImageSignature

es = Elasticsearch()
ses = SignatureES(es)
directory=os.getcwd()
gis = ImageSignature()

from slicer import slice

#slice('puzzle.jpg', cols=5, rows=3)

"""
def splitFileNames():
    items = os.listdir(".")
    print(items)
    newlist = []
    for names in items:
        if names.endswith(".png"):
            newlist.append(names)
        
    for filename in newlist:
        ses.add_image(filename)
        """
"""
from PIL import Image
from resizeimage import resizeimage

fd_img = open('input.jpeg', 'rb')
img = Image.open(fd_img)
img = resizeimage.resize_contain(img, [200, 100])
img = img.convert("RGB")
img.save('inputResized.png', img.format)
fd_img.close()"""
        
inputSignature = gis.generate_signature('input.png')


def splitFileNames():
    items = os.listdir(".")
    print(items)
    newlist = []
    for names in items:
        if names.endswith(".png"):
            newlist.append(names)
    newlist.remove('input.png')
            
    print(newlist)
            
    bestDistance = 1
    bestFileName = 'dummy.png'
    secondBestDistance = 1
    secondBestFileName = 'dummy.png'
    for filename in newlist:
        currentFileDistance = gis.normalized_distance(inputSignature,gis.generate_signature(filename) )
        if currentFileDistance < bestDistance:
            bestDistance = currentFileDistance
            bestFileName = filename
        elif currentFileDistance < secondBestDistance:
            secondBestDistance = currentFileDistance
            secondBestFileName = filename
            
    return bestDistance, bestFileName, secondBestDistance, secondBestFileName
    
            
bestDistance, bestFileName, secondBestDistance, secondBestFileName = splitFileNames()
            
print("best result has distance {} and name {}, second best  result has distance {} and name {}".format(bestDistance, bestFileName, secondBestDistance, secondBestFileName))

        
        

#c = gis.generate_signature(    'puzzle_01_01.png')
#d =    gis.generate_signature(    'puzzle_01_01.png')
#print(gis.normalized_distance (c,d))
        
#ses.search_image('puzzle_01_01.png')
#ses.search_single_record('puzzle_01_01.png')
#print(ses.search_image('puzzle_01_01.png'))