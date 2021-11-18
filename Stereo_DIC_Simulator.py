import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

def camera_calibration(f,camPx,camRes,So,theta):

    with open('blank_calibration.caldat','r') as file:
        blank = file.readlines()

    blank = [line.strip('\n').split(';') for line in blank]
    
    # focal length
    focalLength = f'{round(f/camPx):.1f}'
    blank[0][-1] = focalLength
    blank[1][-1] = focalLength
    blank[10][-1] = focalLength
    blank[11][-1] = focalLength

    # image plane center
    camC = camRes/2
    blank[8][-1] = str(camC[0])
    blank[9][-1] = str(camC[1])
    blank[18][-1] = str(camC[0])
    blank[19][-1] = str(camC[1])

    # camera distance in Y-direction
    Ty = round(So*math.sin(math.radians(theta)))
    blank[21][-1] = f'{Ty:.1f}'

    # stereo-angle
    blank[23][-1] = f'{theta:.1f}'
    
    with open('calibration.caldat','w') as file:
        for line in blank:
            file.write(f'{";".join(line)}\n')
    
    return

def speckle_image(camRes):

    ref_img = cv2.imread('speckle_patterns\\ref_speckle_1.bmp',0)

    new_img = ref_img[0:camRes[1],0:camRes[0]]

    cv2.imwrite('speckle.bmp',new_img)

    plt.figure()
    plt.imshow(new_img,cmap='gray')
    plt.show()

def main():

    # +++ INPUT +++

    # Object
    fov = [76,76+30]    # field-of-view in milimeters
    
    # Lenses
    f = 50.0            # focal length in milimeters
    mwd = 450.0         # minimum working distance in milimeters
    mag = 0.0

    # Camera
    res_px = np.array([1392,1040])  # camera spatial resolution in pixel
    px = 6.45                       # camera pixel size in micrometer

    res_mm = res_px * px * 10**-3
    
    # Object Distace
    So = max(fov)*f/max(res_mm)

    # generate reference speckle image 
    speckle_image(res_px)

    # generate camera calibration files
    theta = 15
    camera_calibration(f,px,res_px,So,theta)

    print(f'Estimated Object Distance = {So:.3f} mm')

    # open MatchID Stereo
    os.system('matchidstereo')

    return

if __name__ == '__main__':
    main()