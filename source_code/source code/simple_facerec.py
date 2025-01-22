import face_recognition
import cv2
import os
import glob
import numpy as np
import requests
import base64
import time
import warnings
from urllib3.exceptions import InsecureRequestWarning

previous=[]  
class SimpleFacerec:##Yüz tanıma işlemleri bu sınıfta yönetilir.
     
    def __init__(self):
        self.known_face_encodings = []#Tanınmış yüzlerin özellik vektörleri saklanır.
        self.known_face_names = []# Tanınmış yüzlere atanmış isimleri saklar.
        self.frame_resizing = 0.25
        self.face_recognition = face_recognition 

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))#Klasördeki tüm dosyaları alır
        #"source code/images/person1.jpg", "source code/images/person2.png",

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)

            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]# Görüntüdeki yüzün encodingini alır.
                                                                      #Amacı verilen dizideki yüzleri tanınabilir hale getirmek

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)  # Store filename as the name

        print("Encoding images loaded")
        
    def encode_image(self, image, name): #Tek bir görüntüyü encode eder ve bu görüntüye bir isim atar.
        """
        Encode a single image and store its encoding with its name.
        :param image: The image to encode
        :param name: The name to associate with the image
        """
        # Convert image to RGB for encoding
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Get the face encoding from the image
        face_locations = face_recognition.face_locations(rgb_img)#Yüzün özelliklerini çıkarır
                                                                 #Amacı gerçek zamanlı eklemeler yapmak için bireysel yüzleri tanımlamak

        if not face_locations:
            print(f"No faces found in the image for {name}. Skipping encoding.")
            return
        
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

        if not face_encodings:
            print(f"No face encodings found for {name}. Skipping encoding.")
            return
           
        img_encoding = face_encodings[0]

        # Store the encoding and name
        self.known_face_encodings.append(img_encoding)
        self.known_face_names.append(name)

        print(f"Encoded image for {name}")

        # Save the image as a file
        file_name = f"{name}.jpg"  # Save as JPG file
        # cv2.imwrite(file_name, image)  # Uncomment if you want to save the image
        print(f"{file_name} saved.")
            

    def detect_known_faces(self, frame):#Video karesindeki yüzleri tanımlar ve bilinen yüzlerle eşleştirir.
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        # Eğer yüzler bulunduysa, encoding işlemini yap
        if face_locations:  # Eğer yüzler bulunmuşsa
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)#Algılanan yüzü bilinen yüzlerle karşılaştırır.
                name = "Unknown"
                

                # Eğer eşleşen yüz varsa
                if True in matches:
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    if len(face_distances) > 0:  # face_distances dizisinin boş olmaması gerekir
                        best_match_index = np.argmin(face_distances)#En düşük mesafeyi bulup en iyi eşleşmeyi belirler.
                        name = self.known_face_names[best_match_index]
                        #Amacı tanımlanan yüzlerin konumlarını ve isimlerini döndürmek
                
                face_names.append(name)
      
            
            

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
    
    def process_face_image(self,img):
      
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Görüntüyü gri tonlamaya çevirme
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit etme
        faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Yüz tespit edilmediğinde img_cropped değişkenini None olarak başlatma
        img_cropped = None

    # Eğer yüz tespit edildiyse, ilk yüzü çizebiliriz
        if len(faces_detected) > 0:
           (x, y, w, h) = faces_detected[0]
           cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Padding değerini ayarlama
           p = 20  # padding

        # Kırpılan görüntüyü alma
           img_cropped = img[y - p + 1:y + h + p, x - p + 1:x + w + p]

    # Yüz tespiti yapılmışsa img_cropped kontrolü yaparak işlemi gerçekleştirme
        if img_cropped is not None and img_cropped.size > 0:
        # Kırpılan resmi normalleştirme
          norm_img = np.zeros((img_cropped.shape[0], img_cropped.shape[1]))
          norm_img = cv2.normalize(img_cropped, norm_img, 0, 255, cv2.NORM_MINMAX)

        # Yeniden boyutlandırma (orijinal boyutlara döndürme)
          im_reshape = cv2.resize(norm_img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR)

          return im_reshape

    # Yüz tespiti yapılmadıysa orijinal resmi döndürme
        return img
    
    
    def detect_and_display_faces(self):
      warnings.simplefilter('ignore', InsecureRequestWarning)
    # SimpleFacerec nesnesi oluştur
      sfr = SimpleFacerec()
      sfr.load_encoding_images("source code/images/")  # Yüz veritabanını yükle

      previous_name = None  # Başlangıçta önceki isim yok.

      while True:  # Sürekli döngü başlat
        # Veritabanından frame al
        url = "https://localhost:7016/api/Faces/Camera-Frame"
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            print("Veri başarıyla alındı")
            data = response.json()

            # Base64 verisini çöz
            base64_image = data[0].get("frame")
            image_data = base64.b64decode(base64_image)
            image_array = np.frombuffer(image_data, np.uint8)
            frame2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            face_locations = self.face_recognition.face_locations(frame2)
            if face_locations:
                 frame2=sfr.process_face_image(frame2)

            # Eğer frame doğru alınmışsa, yüz tanımayı başlat
            if frame2 is None:
                print("Frame alınamadı!")
                continue

            # Yüz tanıma işlemi
            face_locations, face_names = sfr.detect_known_faces(frame2)

            # Yüz bulunmadığında
            if face_locations is None or len(face_locations) == 0:
                if previous_name != "No face found":  # "No face found" önceki adla eşleşmiyorsa
                    save_url = "https://localhost:7016/api/Faces/save-face-recognation"
                    data = {"faceName": "No face found"}
                    response = requests.post(save_url, json=data, verify=False)
                    if response.status_code == 200:
                        print("Veri aktarıldı: No face found")
                    else:
                        print("Hata oluştu:", response.status_code)
                    previous_name = "No face found"  # Önceki adı "No face found" olarak güncelle
                continue  # Yüz bulunmazsa bir sonraki frame'e geç

            # Yüz bulunduysa, "No face found" durumu sıfırlanır ve istek gönderilebilir
            # Yüz bulunduğunda bayrak sıfırlanır
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if not isinstance(name, str):
                    name = "Unknown"

                # Yüzü etiketle
                cv2.rectangle(frame2, (left, top), (right, bottom), (0, 255, 255), 2)
                cv2.putText(frame2, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0), 1)

                # Eğer yeni bir yüz tanındıysa, veritabanına kaydet
                if name != previous_name:
                    save_url = "https://localhost:7016/api/Faces/save-face-recognation"
                    data = {"faceName": name}
                    response = requests.post(save_url, json=data, verify=False)
                    if response.status_code == 200:
                        print("Veri aktarıldı:", name)
                    else:
                        print("Hata oluştu:", response.status_code)
                    previous_name = name  # Önceki isim güncellenir

            # Frame'i göster
            cv2.imshow('Video', frame2)

            # 'q' tuşuna basıldığında döngüyü durdur
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Veritabanından veri alınamadı:", response.status_code)

        # Performansı iyileştirmek için biraz bekleme süresi ekle
        time.sleep(2)  # 2 sn bekle

    # Pencereleri kapat
    cv2.destroyAllWindows()
    
    
       
  
    


# Örnek kullanım

