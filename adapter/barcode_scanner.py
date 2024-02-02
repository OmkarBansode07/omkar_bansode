# import cv2
# import numpy as np
# from pyzbar.pyzbar import decode
 
# def decoder(image):
#     gray_img = cv2.cvtColor(image,0)
#     barcode = decode(gray_img)

#     barcodeData = None
 
#     for obj in barcode:
#         points = obj.polygon
#         (x,y,w,h) = obj.rect
#         pts = np.array(points, np.int32)
#         pts = pts.reshape((-1, 1, 2))
#         cv2.polylines(image, [pts], True, (0, 255, 0), 3)
 
#         barcodeData = obj.data.decode("utf-8")
#         barcodeType = obj.type
#         string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
       
#         cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
#         print("Barcode: " + barcodeData)

#     return barcodeData
 
# cap = cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     decoder(frame)
#     print(type(decoder(frame)))
#     cv2.imshow('Image', frame)
#     code = cv2.waitKey(10)
#     if code == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
# exit()

import cv2
import numpy as np
from pyzbar.pyzbar import decode
def scan():
    def decoder(image):
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        barcode = decode(gray_img)
    
        # Initialize barcodeData outside the loop
        barcodeData = None
    
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
    
        # Print barcode data even if no barcode is detected 
        return barcodeData
    
    cap = cv2.VideoCapture(0)
    result=""
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
    cv2.destroyAllWindows()

def extract_barcode():
    barcode_value=scan()
    return [barcode_value,barcode_value[:1:],barcode_value[1:6:],barcode_value[6:7:],barcode_value[7:12:],barcode_value[12::]]
    
if __name__=='__main__':
    extract_barcode()