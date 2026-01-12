"use client";
import { useState } from 'react';
import axios from 'axios';

interface Patient {
  full_name: string;
  age: number;
  blood_type: string;
  emergency_contact_name: string;
  emergency_contact_phone: string;
  allergies: string;
  medical_history: string;
}

export default function ScanPage() {
  const [token, setToken] = useState("");
  const [patientData, setPatientData] = useState<Patient | null>(null);

  const handleScanLookup = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/scan/${token}`);
      setPatientData(res.data);
    } catch (err) {
      alert("Invalid Token or Patient not found!");
      setPatientData(null);
    }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto min-h-screen bg-gray-50 text-gray-900">
      <h1 className="text-3xl font-bold mb-6 text-blue-800">Medic Lookup Station</h1>
      
      {/* Search Section */}
      <div className="flex gap-2 mb-10 bg-white p-4 rounded-xl shadow-sm border border-gray-200">
        <input 
          type="text" 
          placeholder="Paste Patient QR Token" 
          className="border border-gray-300 p-3 flex-grow rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
          onChange={(e) => setToken(e.target.value)}
        />
        <button 
          onClick={handleScanLookup} 
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-bold transition"
        >
          Lookup
        </button>
      </div>

      {patientData && (
        <div className="space-y-6 animate-in fade-in duration-500">
          
          {/* Header Card: Identity & Vitals */}
          <div className="bg-white p-6 rounded-2xl shadow-md border-l-8 border-blue-600">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-3xl font-bold text-gray-800">{patientData.full_name}</h2>
                <p className="text-gray-500 uppercase tracking-widest text-sm font-semibold">Patient Identity</p>
              </div>
              <div className="text-right">
                <span className="bg-red-100 text-red-700 text-2xl font-black px-4 py-2 rounded-lg border border-red-200">
                  {patientData.blood_type}
                </span>
                <p className="text-xs text-red-500 mt-1 font-bold uppercase">Blood Type</p>
              </div>
            </div>
            
            <div className="mt-4 text-xl">
              <span className="font-bold">Age:</span> {patientData.age}
            </div>
          </div>

          {/* Emergency Contact Card */}
          <div className="bg-white p-6 rounded-2xl shadow-md border border-gray-200">
            <h3 className="text-lg font-bold text-gray-700 mb-3 flex items-center gap-2">
              🚨 Emergency Contact
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-500 uppercase font-bold">Primary Contact</p>
                <p className="text-lg font-medium">{patientData.emergency_contact_name}</p>
              </div>
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-500 uppercase font-bold">Phone Number</p>
                <p className="text-lg font-medium text-blue-600 underline">{patientData.emergency_contact_phone}</p>
              </div>
            </div>
          </div>

          {/* Medical Records Card */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-red-50 p-6 rounded-2xl border border-red-100">
              <h3 className="text-lg font-bold text-red-800 mb-2">⚠️ Allergies</h3>
              <p className="text-red-900 text-lg leading-relaxed">
                {patientData.allergies || "No known allergies reported."}
              </p>
            </div>
            <div className="bg-blue-50 p-6 rounded-2xl border border-blue-100">
              <h3 className="text-lg font-bold text-blue-800 mb-2">📋 Medical History</h3>
              <p className="text-blue-900 text-lg leading-relaxed">
                {patientData.medical_history || "No significant history recorded."}
              </p>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}       