To run this program, make sure you have OpenCV, Numpy, and Pandas
  If you don't, just install it with this command: pip3 install opencv-python numpy pandas

Replace inputfolder with your input folder PATH and likewise for outputfolder... 

*The kernel size was just chosen via experimentation...

To detect inclusions, this program converts all images to grayscale so that the intensity of inclusions can be compared. To do this, we normalize the brightness of each image and blur the image using Gaussian Blur.

Gaussian Blur helps because we reduce small & random noise but keep the overall brightness pattern and large structures. I used a 51 x 51 kernel as we need an odd number to have a center pixel, and 51 x 51 was a good enough size where we smooth out bright clusters but preserve the overall brightness of the whole image. The Gaussian blur removes bright spots/inclusions in the image, so it effectively represents the background since the structure is smoothed out.  I also subtracted the original image from the Gaussian Blur image to produce a difference image, which emphasized the localized bright spots. 

By using an Otsu threshold, we're able to find the best threshold for the images to separate bright & dark pixels, and this is important as images vary in brightness.

Morphological Cleanup was also something that I used to clean up the image by reducing noise and making sure that 

From here, we used a connected components algorithm so we can group pixels together as an object to measure it as an inclusion. 

To quantify the total inclusion area, I add the areas of all detected conclusions, and the total percent area is just the (total inclusion area / total image area) * 100. 

The total inclusion area and percent area are printed out, and so is the prediction for inclusion / non-inclusion.

In the output folder, the program will save the overlay images and a summary CSV file.
