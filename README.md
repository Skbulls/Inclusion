To run this program, make sure you have OpenCV, Numpy, and Pandas
  If you don't, just install it with this command: pip3 install opencv-python numpy pandas

Replace inputfolder with your input folder PATH and likewise for outputfolder... 

To detect inclusions, this program converts all images to grayscale so that the intensity of inclusions can be compared. To do this, we normalize the brightness of each image and blur the image using Gaussian Blur.

Gaussian Blur helps because we reduce small & random noise but keep the overall brightness pattern and large structures. I'm using a dynamically updating kernel that updates from 21 to 101 - still odd numbers as we need a singular center pixel.  The Gaussian blur removes bright spots/inclusions in the image, so it effectively represents the background since the structure is smoothed out.  I also subtracted the original image from the Gaussian Blur image to produce a difference image, which emphasized the localized bright spots. 

The inclusions are being filtered by a physical size filter which is dictated by the "minum2" and the "maxum2" variables. Also, the "minintensity" variable is being used as a filter for inclusions. 

I'm also cropping out the bottom parts of the image that contain the scale bar and the timestamp, so it doesn't get in the way of the algorithm.

By using an Otsu threshold, we're able to find the best threshold for the images to separate bright & dark pixels, and this is important as images vary in brightness. We are now multiplying the threshold scale against the Otsu threshold because we classify fewer pixels as inclusions and we remove the possibility of smaller regions passing segmentation. 

Morphological Cleanup was used to clean up the image by reducing noise and making sure that inclusions were well defined and easily identifiable from the other "noise".

From here, we used a connected components algorithm so we can group pixels together as an object to measure it as an inclusion. Inclusions are highlighted with white circles on the image. 

To quantify the total inclusion area, I add the areas of all detected inclusions, and the total percent area is just the (total inclusion area / total image area) * 100. 

In the output folder, the program will save the overlay images and a summary CSV file along with a features csv file which contains the details for every inclusion in every image. 
