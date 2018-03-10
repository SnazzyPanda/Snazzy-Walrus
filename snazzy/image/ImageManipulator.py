'''

@author: Snazzy Panda
'''
from PIL import Image
import random
import math

class ImageManipulator(object):
    '''
    classdocs
    '''
    # TODO: Close images as necessary!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    DEFAULT_SAMPLE = Image.LANCZOS
    DEFAULT_HEIGHT = 1080
    DEFAULT_WIDTH = 1920
    DEFAULT_START_Y = 0
    DEFAULT_START_X = 0
    DEFAULT_CROP_DIRECTION = 0 # horizontal
    DEFAULT_CROP_POSITION = 0 # random

    DEFAULT_NUM_IMAGES_IN_PREVIEW = 3
    DEFAULT_PREVIEW_WIDTH = 200
    DEFAULT_PREVIEW_HEIGHT = 200
    DEFAULT_PREVIEW_PCT_OFFSET = .1

    DEFAULT_MIN_X = 0
    DEFAULT_MIN_Y = 0
    PLACEHOLDER = -1

    CROP_RANDOM = 0 # random in relevant direction
    CROP_CENTER = 1 # center
    CROP_RT = 2 # right or top
    CROP_LB = 3 # left or bottom

    CROP_HORIZONTAL = 0
    CROP_VERTICAL = 1
    # UNUSED!!
    CROP_ANY = 3 #TODO: consider implementing this?


    def __init__(self):
        '''
        Constructor
        '''
    # end constructor

    def getScaledWidth(self, originalWidth, originalHeight, newHeight = DEFAULT_HEIGHT):
        return int((originalWidth * newHeight) / originalHeight)
    # end getScaledWidth

    def getScaledHeight(self, originalWidth, originalHeight, newWidth = DEFAULT_WIDTH):
        return int((newWidth * originalHeight) / originalWidth)
    # end getScaledHeight

    def resizeImageToSize(self, image, width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT, sampleToApply = DEFAULT_SAMPLE):
        return image.resize((width, height), sampleToApply)
    # end resizeImageToSize

    def loadImage(self, imgPath):
        return Image.open(imgPath, "r")
    # end loadImage
    
    def saveImage(self, img = None, imgPath = None):
        if img is not None:
            if imgPath is not None:
                img.save(imgPath)
    # end saveImage

    def imageIsPortrait(self, img = None):
        if(img is not None):
            if(img.height > img.width):
                return True
        return False
    # end imageIsPortrait

    def relativeResizeByWidth(self, image, newWidth = DEFAULT_WIDTH, sampleToApply = DEFAULT_SAMPLE):
        newHeight = self.getScaledHeight(image.width, image.height, newWidth)
        return image.resize((newWidth, newHeight), sampleToApply)
    # end relativeResizeByWidht

    def relativeResizeByHeight(self, image, newHeight = DEFAULT_HEIGHT, sampleToApply = DEFAULT_SAMPLE):
        newWidth = self.getScaledWidth(image.width, image.height, newHeight)
        return image.resize((newWidth, newHeight), sampleToApply)
    # end relativeResizeByHeight

    def cropToSize(self, image, startX = DEFAULT_START_X, startY = DEFAULT_START_Y,
                   newWidth = DEFAULT_WIDTH, newHeight = DEFAULT_HEIGHT):
        if((startX + newWidth) > image.width):
            newWidth = int(image.width - startX)
        if((startY + newHeight) > image.height):
            newHeight = int(image.height - startY)
        # 4-tuple defining the left, upper, right, and lower pixel coordinate.
        return image.crop((startX, startY, (startX + newWidth), (startY + newHeight)))
    # end cropToSize

#    def cropToBoundedRandomSize(self, image, minX = DEFAULT_MIN_X, minY = DEFAULT_MIN_Y, maxX, maxY):
        # 0 max = any size (within image)
        # TODO: other placeholder stuff
        # TODO: implement this method
#        return None
    # end cropToRandomBoundedSize

    def cropByLocation(self, image, width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT,
                       direction = DEFAULT_CROP_DIRECTION, location = DEFAULT_CROP_POSITION):
        startX = 0
        startY = 0

        if(direction is self.CROP_HORIZONTAL):
            # horizontal
            startX = self.getStartXByLocation(image, width, location)
        elif(direction is self.CROP_VERTICAL):
            # vertical
            startY = self.getStartYByLocation(image, height, location)
        else:
            print("[WARN] Unsupported crop direction supplied: " + direction + ". Trying again with default...")
            return self.cropByLocation(image, width, height, self.DEFAULT_CROP_DIRECTION, location)

        if((startY + height) > image.height):
            height = image.height - startY
        if((startX + width) > image.width):
            width = image.width - startX
        #The box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
        return image.crop((startX, startY, width, height))
    # end cropByLocation

    def getStartXByLocation(self, image, width = DEFAULT_WIDTH, location = DEFAULT_CROP_POSITION):
        # horizontal
        # calculate the maximum x possible from given values
        maxX = image.width - width
        if(maxX < 0):
            print("[WARN] Supplied width exceeded available width. Given: " + width + ", avail: " + image.width)
            maxX = image.width # x was negative, so revert to image width (aka last x pixel)
        startX = 0
        if(location is self.CROP_RANDOM):
            startX = random.randint(0, maxX)
        elif(location is self.CROP_CENTER):
            startX = (image.width - width) / 2
        elif(location is self.CROP_RT):
            startX = image.width - width
        elif(location is self.CROP_LB):
            startX = 0
        else:
            # no match
            startX = random.randint(0, maxX)
            print("[WARN] Horizontally: invalid position given: " + location + ". using default position.")
            return self.getStartXByLocation(image, width, self.DEFAULT_CROP_POSITION)
        return startX
    # end getStartXByLocation

    def getStartYByLocation(self, image, height = DEFAULT_HEIGHT, location = DEFAULT_CROP_POSITION):
        maxY = image.height - height
        if(maxY < 0):
            print("[WARN] Supplied height exceeded available height. Given: " + height + ", avail: " + image.height)
            maxY = image.height

        startY = 0
        if(location is self.CROP_RANDOM):
            startY = random.randint(0, maxY)
        elif(location is self.CROP_CENTER):
            startY = (image.height - height) / 2
        elif(location is self.CROP_RT):
            startY = image.height - height
        elif(location is self.CROP_LB):
            startY = 0
        else:
            # no match
            startY = random.randint(0, maxY)
            print("[WARN] Horizontally: invalid position given: " + location + ". using default position.")
            return self.getStartXByLocation(image, height, self.DEFAULT_CROP_POSITION)
        return startY
    # end getStartYByLocation


    def generatePreviewImage(self, inImgList, imgLimit = DEFAULT_NUM_IMAGES_IN_PREVIEW,
            previewWidth = DEFAULT_PREVIEW_WIDTH, previewHeight = DEFAULT_PREVIEW_HEIGHT,
            pctImageOffset = DEFAULT_PREVIEW_PCT_OFFSET, sampleToApply = DEFAULT_SAMPLE):

        # assume given list of images!!!!

        # return none if empty list of images to use
        if(0 == len(inImgList)):
            print("[ERROR] Apparently empty list given to genPreview: " + len(inImgList))
            return None

        # TODO: consider adding border to images?

        # OffsetPerImage (Percentage viewable if image is on top of it)
        # 10% (0.1) seems fine for now
        pctOff = pctImageOffset
        #float pctOff = pctImageOffset;

        # if desired images to use exceeds images given, set to number we can use
        if(imgLimit > len(inImgList)):
            imgLimit = len(inImgList)

        # total percentage is: ((NumImages - 1) * PercentOffsetPerImage)
        totalPctOffset = (imgLimit - 1) * pctOff
        # calculate height and width for individual pictures
        # ((1 - TotalPercentageUsed) * FullPossibleWidth) -- (or height)
        innerImgWidth = math.floor((1 - totalPctOffset) * previewWidth)
        innerImgHeight = math.floor((1 - totalPctOffset) * previewHeight)

        # grab all images we are going to use for preview
        imgList = inImgList[:imgLimit]

        # reverse images we will use
        imgList = list(reversed(imgList))

        # create output image
        output = Image.new("RGBA", (previewWidth, previewHeight)) # CMYK
        output.putalpha(Image.new("L", (previewWidth, previewHeight)))

        count = 0
        # for each image
        for i in imgList:
            # get scaled down image to put in preview
            tmpImage = i.resize((innerImgWidth, innerImgHeight), self.DEFAULT_SAMPLE)

            # calculate starting x val
            # (FullPossibleWidth - IndividualImageWidth) - (thisIteration * (PercentOffsetPerImage * FullPossibleWidth)
            startX = math.floor(((previewWidth - innerImgWidth) - (count * (pctOff * previewWidth))))
            # calculate starting y val
            # (thisIteration * (PercentOffsetPerImage * FullPossibleHeight))
            startY = math.floor((count * (pctOff * previewHeight)))

            # Pastes another image into this image. The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper, right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted image must match the size of the region.
            # Image.paste(im, box=None, mask=None)
            #draw output onto preview image
            # sampleToApply
            output.paste(tmpImage, (startX, startY))

            count += 1
        # end for
        return output
    # end generatePreviewImage

    def isImageLandscape(self, img = None):
        if(img is None):
            return True
        width = img.width
        height = img.height
        return (width > height)
    # end isImageLandscape
