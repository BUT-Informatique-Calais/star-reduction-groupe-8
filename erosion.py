from astropy.io import fits
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats

# Open and read the FITS file
fits_file = './examples/test_M31_linear.fits'
hdul = fits.open(fits_file)

# Display information about the file
hdul.info()

# Access the data from the primary HDU
data = hdul[0].data

# Access header information
header = hdul[0].header

# Handle both monochrome and color images
if data.ndim == 3:
    # Color image - need to transpose to (height, width, channels)
    if data.shape[0] == 3:  # If channels are first: (3, height, width)
        data = np.transpose(data, (1, 2, 0))
    
    # Normalize each channel separately to [0, 255] for OpenCV
    image = np.zeros_like(data, dtype='uint8')
    for i in range(data.shape[2]):
        channel = data[:, :, i]
        image[:, :, i] = ((channel - channel.min()) / (channel.max() - channel.min()) * 255).astype('uint8')
    
    # For star detection, use grayscale version
    data_gray = np.mean(data, axis=2)
else:
    # Monochrome image
    image = ((data - data.min()) / (data.max() - data.min()) * 255).astype('uint8')
    data_gray = data

# Define a kernel for erosion
kernel = np.ones((3,3), np.uint8)

# Create an eroded version
Ierode = cv.erode(image, kernel, iterations=1)

# Save eroded image in RGB format
if data.ndim == 3:
    cv.imwrite('./results/eroded.png', cv.cvtColor(Ierode, cv.COLOR_RGB2BGR))
else:
    cv.imwrite('./results/eroded.png', Ierode)

# Star detection with DAOStarFinder
mean, median, std = sigma_clipped_stats(data_gray, sigma=3.0)
daofind = DAOStarFinder(fwhm=3.0, threshold=5.*std)
sources = daofind(data_gray - median)

#Create a star mask to identify star regions to reduce
M = np.zeros(data_gray.shape, dtype=np.float32)

if sources is not None:    
    # Mark star zones
    for star in sources:
        x, y = int(star['xcentroid']), int(star['ycentroid'])
        cv.circle(M, (x, y), 10, 1.0, -1)
else:
    print("No stars detected")

# Soften mask edges with Gaussian blur
M = cv.GaussianBlur(M, (15, 15), 0)

# Replace stars with single pixels
Ifinal = Ierode.copy()

if sources is not None:
    for star in sources:
        x, y = int(star['xcentroid']), int(star['ycentroid'])
        
        # Get the star pixel color from the original image
        if data.ndim == 3:
            star_color = image[y, x]
        else:
            star_color = image[y, x]
        
        # Create a mask for the star zone
        mask_star = np.zeros(data_gray.shape, dtype=np.uint8)
        cv.circle(mask_star, (x, y), 10, 255, -1)
        
        # Ifinal
        Ifinal = cv.inpaint(Ifinal, mask_star, 3, cv.INPAINT_TELEA)
        
        # Put back a single pixel at the center with original color
        if data.ndim == 3:
            Ifinal[y, x] = star_color
        else:
            Ifinal[y, x] = star_color

# Save final image in correct color format
if data.ndim == 3:
    cv.imwrite('./results/final.png', cv.cvtColor(Ifinal, cv.COLOR_RGB2BGR))
else:
    cv.imwrite('./results/final.png', Ifinal)

# Close the file
hdul.close()