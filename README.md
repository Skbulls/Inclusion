To run this program, make sure you have OpenCV, Numpy and Pandas
  If you don't, just install it with this command: pip3 install opencv-python numpy pandas

Replace inputfolder with your input folder PATH and likewise for outputfolder... 

*As I only have two images (inclusion & noninclusion), the threshold/size values won't be exact, you can tune it as you like.


To detect inclusions, this program converts all images to grayscale so that the intensity of inclusions can be compared.., to do this, we normalize the brightness of each image and blur the image using Gaussian Blur.

Gaussian Blur helps because we reduce small & random noise but keep the overall brightness pattern and large structures. 

By using an Otsu threshold, we're able to find the best threshold for the images to separate bright & dark pixels, and this is important as images vary in brightness.

From here, we used a connected components algorithm so we can group pixels together as an object to measure it as an inclusion. 

The total inclusion area and percent area is printed out and so is the prediction for inclusion / no inclusion. 

In the output folder, the program will save the overlay images and a summary csv file.
