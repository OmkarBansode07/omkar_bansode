# import needed libraries 
# cv2- for capturng the image using webcam
# numpy to store DeprecationWarning
# pyzbar to decode the barcode
import cv2
import numpy as np
from pyzbar.pyzbar import decode
 
# decode the barcode and return it's value
def read_barcode():
    def decoder(image):
        
        # generating the gray image
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        #storing the decoded value in barcode variable using decode module of pyzbar
        barcode = decode(gray_img)
    
        # Initialize barcodeData outside the loop
        barcodeData = None
    
        # extracting the barcode data
        for obj in barcode:
            rect = obj.rect
            points = obj.polygon
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, (0, 255, 0), 3)
    
            barcodeData = obj.data.decode("utf-8")
            barcodeType = obj.type
            string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
            cv2.putText(image, string, (rect[0], rect[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    

        return barcodeData

    # capturing the image using cv2
    cap = cv2.VideoCapture(0)
    
    # variable to store the barcode value
    result=""

    # reads image from webcam and call decoder method
    while True:
        ret, frame = cap.read()
        result = decoder(frame)
        cv2.imshow('Image', frame)
    
        # Break the loop after the first successful scan
        if result is not None:
            break
    
        code = cv2.waitKey(10)
        if code == ord('q'):
            break
    
    cap.release()
    return result

print(read_barcode())