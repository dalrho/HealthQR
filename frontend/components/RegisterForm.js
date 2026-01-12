"use client";

import { useState } from 'react';
import axios from 'axios';
import { QRCodeCanvas } from 'qrcode.react';

export default function RegisterForm() {
  const [formData, setFormData] = useState({ full_name: '', email: '', age: '' });
  const [qrToken, setQrToken] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/register', formData);
      setQrToken(response.data.qr_token);
    } catch (error) {
      console.error("Registration failed", error);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      {!qrToken ? (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input 
            type="text" placeholder="Full Name" 
            onChange={(e) => setFormData({...formData, full_name: e.target.value})} 
            className="border p-2 rounded"
          />
          <input 
            type="email" placeholder="Email" 
            onChange={(e) => setFormData({...formData, email: e.target.value})} 
            className="border p-2 rounded"
          />
          <input 
            type="number" placeholder="Age" 
            onChange={(e) => setFormData({...formData, age: e.target.value})} 
            className="border p-2 rounded"
          />
          <button type="submit" className="bg-blue-600 text-white p-2 rounded">
            Register & Generate QR
          </button>
        </form>
      ) : (
        <div className="text-center">
          <h2 className="text-xl font-bold mb-4">Your HealthQR Code</h2>
          <div className="bg-white p-4 inline-block rounded shadow-lg">
            <QRCodeCanvas value={qrToken} size={256} />
          </div>
          <p className="mt-4 text-gray-600">Scan this at any HealthQR station.</p>
          <button onClick={() => setQrToken(null)} className="mt-4 text-blue-500 underline">
            Register another patient
          </button>
        </div>
      )}
    </div>
  );
}