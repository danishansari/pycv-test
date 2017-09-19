import sys, cv2
import numpy as np

# Class to find circles in an image
class CircleDetector:

    # image to process
    img = None

    # function to denoise image
    def denoiseImage(self):

        # convert image to gray
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    
        # find edges
        img_canny = cv2.Canny(img_gray, 100, 40);
    
        # remove noise, using dilation-erosion
        kernel = np.ones((7, 7), np.uint8)
        img_dilation = cv2.dilate(img_canny, kernel, iterations=1)
        img_erosion = cv2.erode(img_dilation, kernel, iterations=1)

        self.img = img_erosion

    # function to find circles
    def findCircles(self):

        # blur image to find circles using haugh
        img_blur = cv2.blur(self.img, (3, 3))
  
        # qpply haugh to find circles
        circles = cv2.HoughCircles(img_blur, cv2.cv.CV_HOUGH_GRADIENT, 1.5, 20)

        # detected circles
        detected = []

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                detected.append((i[0], i[1], i[2]))

        return detected

    
    # function to detect circles
    def detectCircles(self, src_img):

        self.img = src_img
        # initialize 
        #init(self, src_img)

        # denoise image 
        self.denoiseImage()

        # find all circles greater than 10px
        circles = self.findCircles()

        return circles


# main function    
def main():

    # check input
    if len(sys.argv) < 2:
        print "python", sys.argv[0], "image-path"
        return -1

    # load source image
    img = cv2.imread(sys.argv[1], 1)
   
    # check load success
    if img is None:
        print "could not load image:", sys.argv[1]
        return -1

    # show source image
    cv2.imshow("source-image", img)

    # detect circles in source image
    detector = CircleDetector()
    detectedCircles = detector.detectCircles(img);

    # draw all detected circles
    if len(detectedCircles) > 0:
        for i in detectedCircles:
            cv2.circle(img, (i[0], i[1]), i[2], (256, 0, 0), 2)

        print "Circles found = ", len(detectedCircles)
        cv2.imshow("processed-image", img);
    else:
        print "No circle detected!!" 
   
    print "Press any key to exit!"
    cv2.waitKey(0)


if __name__=="__main__":
    main()
