import os
import cv2
import numpy as np
import pandas as pd

channel = 'gray'
inputfolder = '/Users/skbulls/Downloads/Input'
outputfolder = '/Users/skbulls/Downloads/Output'

pixelsize = 1.2
minum2 = 20
maxum2 = 500
minarea = minum2 / (pixelsize ** 2)
maxarea = maxum2 / (pixelsize ** 2)

thresholdscale = 1.1
minintensity = 40
kernelsize = 3

cropbottom = 90
cropright = 240

bgmin = 21
bgmax = 101

summarylist = []
objectslist = []

for file in os.listdir(inputfolder):
    if not file.lower().endswith(('.jpg', '.png', '.tif', '.jpeg')):
        continue

    path = os.path.join(inputfolder, file)
    img = cv2.imread(path)
    if img is None:
        continue

    h, w = img.shape[:2]
    y2 = max(1, h - cropbottom)
    x2 = max(1, w - cropright)
    imgroi = img[:y2, :x2].copy()

    if len(imgroi.shape) == 3:
        if channel == 'red':
            gray = imgroi[:, :, 2]
        elif channel == 'green':
            gray = imgroi[:, :, 1]
        elif channel == 'blue':
            gray = imgroi[:, :, 0]
        else:
            gray = cv2.cvtColor(imgroi, cv2.COLOR_BGR2GRAY)
    else:
        gray = imgroi.copy()

    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    hroi, wroi = gray.shape
    k = max(bgmin, min(bgmax, int(min(hroi, wroi)/20)))
    if k % 2 == 0:
        k = k + 1

    background = cv2.GaussianBlur(gray, (k, k), 0)
    diff = cv2.subtract(gray, background)
    diff = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    otsu, _ = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    tval = int(otsu * thresholdscale)
    if tval < 0:
        tval = 0
    if tval > 255:
        tval = 255

    _, mask = cv2.threshold(diff, tval, 255, cv2.THRESH_BINARY)

    kernel = np.ones((kernelsize, kernelsize), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    numlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)

    totalarea = 0
    totalintensity = 0
    totalpixels = 0
    numinclusions = 0

    for i in range(1, numlabels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < minarea or area > maxarea:
            continue

        maskcomp = (labels == i)
        intensities = gray[maskcomp]
        meanint = np.mean(intensities)
        if meanint < minintensity:
            continue

        cx, cy = centroids[i]
        totalarea = totalarea + area
        totalintensity = totalintensity + np.sum(intensities)
        totalpixels = totalpixels + area
        numinclusions = numinclusions + 1

        objectslist.append({
            "image": file,
            "area_px": int(area),
            "mean_intensity": float(meanint),
            "centroid_x_px": float(cx),
            "centroid_y_px": float(cy)
        })

    imgarea = hroi * wroi
    if imgarea > 0:
        percentarea = (totalarea / imgarea) * 100
    else:
        percentarea = 0
    if totalpixels > 0:
        meanintensity = totalintensity / totalpixels
    else:
        meanintensity = 0

    summarylist.append({
        "image": file,
        "num_inclusions": numinclusions,
        "total_area_px": int(totalarea),
        "total_area_um2": totalarea * (pixelsize ** 2),
        "percent_area": percentarea,
        "mean_intensity": meanintensity
    })

pd.DataFrame(summarylist).to_csv(os.path.join(outputfolder, "summary.csv"), index=False)
pd.DataFrame(objectslist).to_csv(os.path.join(outputfolder, "per_inclusion_features.csv"), index=False)

print(pd.DataFrame(summarylist))
