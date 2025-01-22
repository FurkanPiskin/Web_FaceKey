import cv2
from simple_facerec import SimpleFacerec
import numpy as np
import requests
import io
import os
import base64
from simple_facerec import SimpleFacerec
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from io import BytesIO
from PIL import Image



###################################

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("source code/images/")

output_dir = "databaseface"
os.makedirs(output_dir, exist_ok=True)
###############################################################################
#Base64 veriyi numpy dizisine çeviren yardımcı fonskiyon
def base64_to_image(base64_str):
    # Base64 string'den binary veri
    image_data = base64.b64decode(base64_str)
    # Binary veriyi bir numpy dizisine dönüştür
    image = Image.open(BytesIO(image_data))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

base64_images={}
with open("login_img.jpg","rb") as image_file:
    base64_image=base64.b64encode(image_file.read()).decode()
#print(base64_image)    

url = "https://localhost:7016/api/Faces"

# SSL doğrulamasını devre dışı bırak
response = requests.get(url, verify=False)

if response.status_code == 200:
    print("Veri başarıyla alındı!")
    data = response.json()  # JSON formatında yanıtı çözümle

    # Yanıt bir liste ise
    if isinstance(data, list):
        for item in data:
            print(f"ID: {item.get('id')}")
            person_id=item.get('id')
            image_base64=item.get('image')

            if person_id and image_base64:
                base64_images[person_id]=image_base64

            if base64_image==item.get('image'):
                print("Resim bulundu")
            else:
                print("Failed") 
    
 # Base64'ü OpenCV formatına çevir
      
        
                         # Her bir öğedeki 'id' alanı

    # Yanıt bir sözlük ise
    elif isinstance(data, dict):
        print(f"ID: {data.get('id')}")
for person_id, base64_str in base64_images.items():
    image = base64_to_image(base64_str)
    sfr.encode_image(image, person_id)
    file_name = os.path.join(output_dir, f"{person_id}.jpg")  # Klasörle birlikte dosya adı
    #cv2.imwrite(file_name, image)
    print(f"{file_name} kaydedildi.")  # Örneğin: "John_Doe.jpg"
              # Sözlükteki 'id' alanı
else:
    print(f"İstek başarısız oldu! Durum kodu: {response.status_code}")
    print(f"Sunucu yanıtı: {response.text}")
###################################################################################

# Load Camera
sfr.detect_and_display_faces()
