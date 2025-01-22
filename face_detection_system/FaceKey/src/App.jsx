/* eslint-disable no-unused-vars */
/* eslint-disable react-hooks/exhaustive-deps */
import { useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";
import "./FaceScanner.css";

export default function FaceScanner() {
  const webRef = useRef(null);
  const [currentFrame, setCurrentFrame] = useState(null);
  const [faceName, setFaceName] = useState(null);

  const [isCameraActive, setIsCameraActive] = useState(true);//Webcam i kolayca açıp kapatmak için

  
  // Kameradan kare yakalama
  const captureFrame = async () => {
    if (webRef.current) {
      const imageSrc = webRef.current.getScreenshot();
      console.log("Captured frame:", imageSrc);
      setCurrentFrame(imageSrc);
    }
  };

  // Kamera başlatıldığında veri almak
  const getName = async () => {
    const response = await fetch(
      "https://localhost:7016/api/Faces/get-latest-face",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (response.ok) {
      const data = await response.json();
      setFaceName(data.faceName);
      console.log(data.faceName);
    } else {
      console.log("Hata oluştu", response.status);
    }
  };

  // Kameradan veri almak ve arka planda göndermek için interval
  useEffect(() => {
    const interval = setInterval(() => {
      captureFrame(); // Her 1 saniyede bir kare yakala
      sendFrameToBackend(); // Kareyi backend'e gönder
    }, 1000); // 1 saniye

    return () => clearInterval(interval); // Unmount olduğunda interval temizlenir
  }, [currentFrame]); // currentFrame her değiştiğinde tetiklenir

  // Yüz tanıma isteği gönderme
  useEffect(() => {
    getName(); // İlk başta bir kez çağır
    const interval = setInterval(() => {
      getName(); // 3 saniyede bir çağır
    }, 3000);
  
    return () => clearInterval(interval); // Interval'i temizle
  }, []);
  



  // Kameradan alınan kareyi backend'e gönderme
  const sendFrameToBackend = async () => {
    if (currentFrame) {
      try {
        const response = await fetch(
          "https://localhost:7016/api/Faces/Save-Camera-Frame",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              frame: currentFrame,
            }),
          }
        );
        const data = await response.json();
        console.log("Backend response:", data);
      } catch (error) {
        console.error("Error uploading image:", error);
      }
    } else {
      console.log("No image to send");
    }
  };



  return (
    <div className="scanner-container">
      <h2>Signup for the event by scanning your face</h2>
      <div className="face-frame">
        {/* Webcam */}
        {isCameraActive && (
          <Webcam
            className="camera-video"
            ref={webRef}
            screenshotFormat="image/jpeg"
            audio={false}
            onUserMediaError={(error) =>
              console.error("Error with webcam:", error)
            }
            onUserMediaSuccess={() => captureFrame()} // Media akışı başarıyla sağlandığında captureFrame tetiklenir.
          />
        )}

        {/* Yüz algılama efekti */}
        <div className="face-overlay"></div>
      </div>
      <p className="info-text">
        Place your face in the frame to start scanning process
      </p>
      <p className="scanning-text">Scanning...</p>
      <p className="detected-face-name">
        {faceName === "Unknown" || faceName==="No face found" || faceName===null || faceName==="Server is not running"
          ? faceName
          : `WELCOME ${faceName}`}
      </p>

      <br />
     
    </div>
  );
}
