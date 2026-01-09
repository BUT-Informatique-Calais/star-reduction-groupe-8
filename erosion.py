from astropy.io import fits
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from photutils.detection import DAOStarFinder
from astropy.stats import sigma_clipped_stats
import requests
import json
import time

#Cle api
key = "plkcttkosimsbqgm"

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
    
# API reponse
response = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps({"apikey": key})})
result = response.json()
if result.get('status') == 'success':
    session = result['session']
else:
    raise Exception(f"Échec de connexion: {result}")

# Upload picture to API
data_upload = {'request-json': json.dumps({"session": session})}

with open(fits_file, 'rb') as f:
    reponse = requests.post('http://nova.astrometry.net/api/upload',files={'file': f},data=data_upload)
result = reponse.json()
if result.get('status') == 'success':
    subid = result['subid']
else:
    raise Exception("\nÉchec upload")

# Creation of the jobs
job_id = None
attempts = 20

# Try until the reponse
for i in range(attempts):
    time.sleep(3)
    response = requests.get(f'http://nova.astrometry.net/api/submissions/{subid}')
    try:
        submission_data = response.json()
    except json.JSONDecodeError:
        continue
    
    if 'jobs' in submission_data and len(submission_data['jobs']) > 0:
        jobs = submission_data['jobs']
        if jobs[0] is not None:
            job_id = jobs[0]
            break    

while True:
    response = requests.get(f'http://nova.astrometry.net/api/jobs/{job_id}')
    status = response.json()['status']
    if status == 'success':
        print("Image identifiée !")
        break
    elif status == 'failure':
        print("Échec de l'identification")
        break
    time.sleep(5)
    
#Upload the catalog of stars into a file
axy_url = f'http://nova.astrometry.net/axy_file/{job_id}'
response = requests.get(axy_url)

with open('./stars.fits', 'wb') as f:
    f.write(response.content)

# Read positions
with fits.open('./stars.fits') as cat_hdul:
    pixel_data = cat_hdul[1].data
    
    # Create the mask of stars
    stars = []
    for star in pixel_data:
        x, y = int(star['X']), int(star['Y'])
        if 0 <= x < data_gray.shape[1] and 0 <= y < data_gray.shape[0]:
            stars.append((x, y))
        
    # Ifinal
    Ifinal = Ierode.copy()
    for x, y in stars:
        if data.ndim == 3:
            star_color = image[y, x]
        else:
            star_color = image[y, x]
        
        mask_star = np.zeros(data_gray.shape, dtype=np.uint8)
        cv.circle(mask_star, (x, y), 10, 255, -1)
        
        Ifinal = cv.inpaint(Ifinal, mask_star, 3, cv.INPAINT_TELEA)
        
        if data.ndim == 3:
            Ifinal[y, x] = star_color
        else:
            Ifinal[y, x] = star_color
    
    # Save result
    if data.ndim == 3:
        cv.imwrite('./results/final.png', cv.cvtColor(Ifinal, cv.COLOR_RGB2BGR))
    else:
        cv.imwrite('./results/final.png', Ifinal)
    
hdul.close()