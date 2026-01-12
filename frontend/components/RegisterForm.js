"use client";
import { useState } from 'react';
import axios from 'axios';
import { QRCodeCanvas } from 'qrcode.react';

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    full_name: '', email: '', age: '',
    blood_type: '', emergency_contact_name: '',
    emergency_contact_phone: '', allergies: '', medical_history: ''
  });
  const [qrToken, setQrToken] = useState(null);

  // A cleaner way to update state for many fields
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // This sends all fields to your updated FastAPI /register endpoint
      const response = await axios.post('http://localhost:8000/register', formData);
      setQrToken(response.data.qr_token);
    } catch (error) {
      alert("Registration failed. Check if backend is running and database columns match.");
    }
  };

  const inputClass =
  "border border-gray-300 p-2 rounded text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500";


  return (
    
    
    <div className="p-4 max-w-xl mx-auto bg-white rounded-xl shadow-md border border-gray-100">
      {!qrToken ? (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <h2 className="text-xl font-bold text-blue-700 mb-2">Patient Information</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input name="full_name" type="text" placeholder="Full Name" onChange={handleChange} className={inputClass} required />
            <input name="email" type="email" placeholder="Email" onChange={handleChange} className={inputClass} required />
            <input name="age" type="number" placeholder="Age" onChange={handleChange} className={inputClass} required />
            
            {/* Blood Type Dropdown - Better than text input for data consistency */}
            <select name="blood_type" onChange={handleChange} className={inputClass} required>
              <option value="">Select Blood Type</option>
              {['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>

          <h2 className="text-xl font-bold text-blue-700 mt-4 mb-2">Emergency & Medical</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input name="emergency_contact_name" type="text" placeholder="Emergency Contact Name" onChange={handleChange} className={inputClass} />
            <input name="emergency_contact_phone" type="text" placeholder="Emergency Contact Phone" onChange={handleChange} className={inputClass} />
          </div>

          <textarea name="allergies" placeholder="Allergies (e.g. Penicillin, Peanuts)" onChange={handleChange} className={inputClass + " h-20"}/>
          <textarea name="medical_history" placeholder="Brief Medical History" onChange={handleChange} className={inputClass + " h-20"} />

          <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white font-bold p-3 rounded transition shadow-lg">
            Register & Generate HealthQR
          </button>
        </form>
      ) : (
        <div className="text-center p-6">
          <h2 className="text-2xl font-bold text-green-600 mb-6">Registration Successful!</h2>
          <div className="bg-white p-6 inline-block rounded-xl shadow-2xl border-4 border-blue-50">
            <QRCodeCanvas value={qrToken} size={256} />
          </div>
          <p className="mt-6 text-gray-500 italic">Save or screenshot this QR for medical use.</p>
          <button onClick={() => setQrToken(null)} className="mt-8 text-blue-500 hover:text-blue-700 font-medium">
            ← Register another patient
          </button>
        </div>
      )}
    </div>
  );
}