"use client";
import { useState, useEffect } from "react";
import axios from 'axios';

export default function ScanPage() {
  const [patientData, setPatientData] = useState<any>(null);
  const [isScanning, setIsScanning] = useState(true);

  useEffect(() => {
    let scanner: any;
    let isCleared = false;

    const safeClear = async () => {
      if (isCleared) return;
      isCleared = true;
      try {
        await scanner?.clear();
      } catch (e) {
        // console.warn("Cleanup quieted");
      }
    };

    if (isScanning && typeof window !== "undefined") {
      (async () => {
        const { Html5QrcodeScanner } = await import("html5-qrcode");

        scanner = new Html5QrcodeScanner(
          "reader",
          { 
            fps: 10, 
            qrbox: 250,
            rememberLastUsedCamera: true 
          },
          false
        );

        scanner.render(
          async (decodedText: string) => {
            console.log("✅ SCANNED TOKEN:", decodedText);
            
            try {
              // 1. Fetch data from FastAPI
              const res = await axios.get(`http://localhost:8000/scan/${decodedText}`);
              
              // 2. Stop camera and save data
              await safeClear();
              setPatientData(res.data);
              setIsScanning(false);
            } catch (err) {
              alert("Patient not found in database.");
            }
          },
          () => {} // frame errors ignored
        );
      })();
    }

    return () => { safeClear(); };
  }, [isScanning]);

  return (
    <main className="min-h-screen bg-gray-100 p-8 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-8 text-blue-900">Medic Scan Station</h1>

      {isScanning ? (
        <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl overflow-hidden border-4 border-white">
          <div id="reader" />
          <p className="text-center p-4 text-gray-400 italic">Position QR code within frame</p>
        </div>
      ) : (
        <div className="w-full max-w-2xl animate-in zoom-in duration-300">
          {/* Display your patient cards here */}
          <div className="bg-white p-8 rounded-3xl shadow-xl border-t-8 border-blue-600">
            <h2 className="text-3xl font-bold">{patientData?.full_name}</h2>
            <p className="text-red-600 font-bold">Blood Type: {patientData?.blood_type}</p>
            {/* ... other data fields ... */}
            
            <button 
              onClick={() => { setPatientData(null); setIsScanning(true); }}
              className="mt-8 w-full bg-blue-600 text-white py-4 rounded-xl font-bold hover:bg-blue-700 transition"
            >
              Scan Next Patient
            </button>
          </div>
        </div>
      )}
    </main>
  );
}