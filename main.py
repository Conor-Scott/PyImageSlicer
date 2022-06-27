import sys
from PIL import Image

def sliceImage(filename):
    #non-transparent pixels
    images = []
    
    #remaining pixels to search
    search = []
    
    #neighbors to search through
    imageSearch = []
    
    #individual image being built before being added to images
    currentImage = []
    
    #minimum size to be a sprite
    minimumSize = 16
    
    with Image.open(filename) as im:
        
        #populate rows & columns to search
        for i in range(0, im.size[0]):
            for j in range(0, im.size[1]):
                search.append((i, j))
        
        #search all rows & columns for non-transparent pixels
        for pixel in search[:]:
            if pixel in search:
                search.remove(pixel)
            else:
                continue
            
            #if pixel isn't transparent
            if im.getpixel(pixel)[3] == 255:
                
                #image we are building
                currentImage.append(pixel)
                
                #current pixels to search in image
                imageSearch.append(pixel)
                
                #loop while there are still neighbors 
                while len(imageSearch) > 0:
                    
                    west = imageSearch[0][0],imageSearch[0][1]-1
                    north = imageSearch[0][0]+1,imageSearch[0][1] 
                    east = imageSearch[0][0],imageSearch[0][1]+1
                    south = imageSearch[0][0]-1,imageSearch[0][1]
                    northWest = imageSearch[0][0]+1,imageSearch[0][1]-1
                    northEast = imageSearch[0][0]+1,imageSearch[0][1]+1
                    southWest = imageSearch[0][0]-1,imageSearch[0][1]-1
                    southEast = imageSearch[0][0]-1,imageSearch[0][1]+1
                    
                    neighbors = (west, northWest, north, northEast, east, southEast, south, southWest)
                    
                    for neighbor in neighbors:
                        if neighbor in search:
                            if im.getpixel(neighbor)[3] != 0: 
                                imageSearch.append(neighbor)
                                search.remove(neighbor)
                                currentImage.append(neighbor)
                            else:
                                search.remove(neighbor)
                    
                    #dequeue
                    del imageSearch[0]
                
                #image search complete
                if len(currentImage) > minimumSize:
                    images.append(currentImage)
                    print (f'Image {len(images)} created.')
                currentImage = []
                imageSearch = []
    
        #crop and save images
        for i, image in enumerate(images):
            cols = []
            rows = []
            currImage = None
            for pixel in image:
                cols.append(pixel[0])
                rows.append(pixel[1])
            cols.sort()
            rows.sort()
            cropRect = (cols[0], rows[0], cols[-1]+1, rows[-1]+1)
            currImage = im.crop(cropRect)
            currImage.save(f'{filename[:-4]}_{i}.png')
            

    print (f'{len(images)} images created!')
                    
def main():
    if sys.argv[1]:
        sliceImage(sys.argv[1])
    else:
        print("Please include the filename you wish to slice.")                    
                    
if __name__ == '__main__':
    main()