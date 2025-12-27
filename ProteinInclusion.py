
#Refer to ReadME file for proper documentation on how this works..

import os
import cv2
import numpy as np
import pandas as pd

inputfolder = 'C:/Users/kiran/Downloads/Input'
outputfolder = 'C:/Users/kiran/Downloads/Output'


umpx = 0.5  


minum2 = 30.0      
maxum2 = 500.0

minarea = minum2 / (umpx ** 2)
maxarea = maxum2 / (umpx ** 2)
      

mkrnlsize = 3

summary = []

 

for filename in os.listdir(inputfolder):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')): #Images only work if it's under the jpg / jpeg / png format.., if it is another format, you have to add the extension under the parameters
        continue

    img_path = os.path.join(inputfolder, filename)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR) 

    if img is None:
        continue

    
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    else:
        gray = img.copy()


    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    gray = gray.astype(np.uint8)

    

    
    background = cv2.GaussianBlur(gray, (51, 51), 0) #

   
    diff = cv2.subtract(gray, background)

 
    diff = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)
    diff = diff.astype(np.uint8)


    _, mask = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    
    kernel = np.ones((mkrnlsize, mkrnlsize), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)

    image_area_px = gray.shape[0] * gray.shape[1]
    total_area_px = 0
    total_intensity = 0
    total_pixels = 0
    num_inclusions = 0

 
    for label in range(1, num_labels):  
        area = stats[label, cv2.CC_STAT_AREA]

       
        if area < minarea or area > maxarea:
            continue

        compmask = (labels == label)
        intensities = gray[compmask]
        mean_int = float(np.mean(intensities))
        
        total_area_px += area
        total_intensity += np.sum(intensities)
        total_pixels += area
        num_inclusions += 1


    if image_area_px > 0:
        percent_area = (total_area_px / image_area_px) * 100
    
    
    else:
        percent_area = 0
        

    if total_pixels > 0:
        mean_intensity = (total_intensity / total_pixels) 
        
    else:
        mean_intensity = 0

    if percent_area > 1.0:
        prediction = "Inclusion" 
    
    else:
        prediction = "No Inclusion"

    summary.append({
        "image": filename,
        "num_inclusions": num_inclusions,
        "total_area_px": int(total_area_px),
        "total_area_um2": total_area_px * (umpx ** 2),
        "percent_area": percent_area,
        "mean_intensity": mean_intensity,
        "prediction": prediction
    })



    
    overlay = img.copy()
    
   
    for x in range(1, num_labels):
        area = stats[x, cv2.CC_STAT_AREA]
        
        if area < minarea or area > maxarea:
            continue
        
        compmask = (labels == x)
        intensities = gray[compmask]
        mean_int = float(np.mean(intensities))
        
        
    
        cx, cy = centroids[x]
        radius = int(np.sqrt(area / np.pi)) 
        
        
        cv2.circle(overlay, (int(cx), int(cy)), radius, (0, 0, 255), 2)

    outputpath = os.path.join(outputfolder, os.path.splitext(filename)[0] + "(overlay).png")
    cv2.imwrite(outputpath, overlay)


summarydf = pd.DataFrame(summary)
summarydf.to_csv(os.path.join(outputfolder, "summary.csv"), index=False)


print(summarydf)

