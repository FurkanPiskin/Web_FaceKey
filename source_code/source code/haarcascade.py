import cv2
import numpy as np

def process_face_image(img):
    # Yüz tespiti için Haar Cascade sınıflandırıcı dosyasını yükleme
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Görüntüyü gri tonlamaya çevirme
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit etme
    faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Eğer yüz tespit edildiyse, ilk yüzü çizebiliriz
    if len(faces_detected) > 0:
        (x, y, w, h) = faces_detected[0]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Padding değerini ayarlama
    p = 20  # padding
    img_cropped = img[y - p + 1:y + h + p, x - p + 1:x + w + p]

    # Kırpılan resmi normalleştirme
    norm_img = np.zeros((img_cropped.shape[0], img_cropped.shape[1]))
    norm_img = cv2.normalize(img_cropped, norm_img, 0, 255, cv2.NORM_MINMAX)

    # Yeniden boyutlandırma (orijinal boyutlara döndürme)
    im_reshape = cv2.resize(norm_img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR)

    return im_reshape

# Örnek kullanım:
img = cv2.imread('foto1.png')  # Burada bir görüntü dosyasının yolu verilmeli

# İşlem yapılmış görüntüyü elde etme
processed_img = process_face_image(img)

# İşlenmiş görüntüyü ekranda gösterme
cv2.imshow('Processed Face Image', processed_img)

# 'q' tuşuna basılana kadar pencereyi açık tutma
cv2.waitKey(0)
cv2.destroyAllWindows()
