import cv2
import sys
import math
import numpy as np
from matplotlib import pyplot as plt


def eval_psnr(image1, image2, R):
    error = np.sum((image1.astype(float) - image2.astype(float)) ** 2)
    mse = error / (float(image1.shape[0] * image1.shape[1]))
    psnr = 10 * math.log10(255 * 255 / mse)
    print("MSE: " + str(mse))
    print("PSNR: " + str(psnr))


def main():
    filename = "satsuma.png"
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        print("Cannot find image : " + filename)
        sys.exit()

    image_tm = np.asarray(image)
    # FFT (time domain -> frequency domain)
    image_fq = np.fft.fft2(image_tm)
    # IFFT (frequency domain -> time domain)
    image_tm_inverse = np.fft.ifft2(image_fq).real

    # Component replacement (Low-frequency components -> center)
    image_fq_shifted = np.fft.fftshift(image_fq)
    # Calculating magnitude spectrum
    magnitude_spectrum = 20 * np.log(np.abs(image_fq_shifted))

    eval_psnr(image_tm, image_tm_inverse, 255)

    plt.subplot(131),plt.imshow(image_tm, cmap = 'gray')
    plt.title('Image (input)'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude spectrum'), plt.xticks([]), plt.yticks([])
    plt.subplot(133),plt.imshow(image_tm_inverse, cmap = 'gray')
    plt.title('Image (inverse)'), plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == "__main__":
    main()
