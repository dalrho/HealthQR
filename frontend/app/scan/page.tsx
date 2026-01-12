"use client";
import { useState } from 'react';
import axios from 'axios';

// 1. Define what a Patient looks like so TypeScript is happy
interface Patient {
  full_name: string;
  age: number;
  allergies: string;
  medical_history: string;
}

export default function ScanPage() {
  const [token, setToken] = useState("");
  // 2. Tell the state it will hold a Patient or null
  const [patientData, setPatientData] = useState<Patient | null>(null);

  const handleScanLookup = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/scan/${token}`);
      setPatientData(res.data);
    } catch (err) {
      alert("Patient not found!");
      setPatientData(null);
    }
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Medic Lookup Station</h1>
      <div className="flex gap-2 mb-8">
        <input 
          type="text" 
          placeholder="Paste QR Token here" 
          className="border p-2 flex-grow rounded"
          onChange={(e) => setToken(e.target.value)}
        />
        <button onClick={handleScanLookup} className="bg-green-600 text-white px-4 py-2 rounded">
          Lookup
        </button>
      </div>

      {patientData && (
        <div className="p-6 border rounded-lg bg-white shadow-md border-green-200">
          <h2 className="text-2xl font-bold text-green-800 border-b pb-2 mb-4">
            {patientData.full_name}
          </h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-500 uppercase font-bold">Age</p>
              <p className="text-lg">{patientData.age}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500 uppercase font-bold">Allergies</p>
              <p className="text-lg text-red-600">{patientData.allergies}</p>
            </div>
          </div>
          <div className="mt-4">
            <p className="text-sm text-gray-500 uppercase font-bold">Medical History</p>
            <p className="text-lg">{patientData.medical_history}</p>
          </div>
        </div>
      )}
    </div>
  );
}