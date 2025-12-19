import cv2 

inputfolder = '/Users/skbulls/Downloads/Input'
outputfolder = '/Users/skbulls/Downloads/Output'

umpx = 0.5

minum2 = 2
maxum2 = 500

minarea = 2 / (0.5**2)
maxarea = 2 / (0.5**2)

results = []

for x in inputfolder:
    img = cv2.imread(x+'.jpg')
    
    if len(img.shape) == 3:
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    else:
        grayimg = img

    grayimg = cv2.normalize(gray,None,0,255,cv2.NORM_MINMAX)

    graysmooth = cv2.GaussianBlur(gray,(5,5),0)

    _, thresh = cv2.threshold(graysmooth,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    binmask = thresh > 0




 