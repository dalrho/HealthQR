"use client";
import { useState, useRef } from 'react'; // 1. Added useRef
import axios from 'axios';
import { QRCodeCanvas } from 'qrcode.react';

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    full_name: '', email: '', age: '',
    blood_type: '', emergency_contact_name: '',
    emergency_contact_phone: '', allergies: '', medical_history: ''
  });
  const [qrToken, setQrToken] = useState(null);

  // 2. Create the "tether" to grab the QR Canvas later
  const qrRef = useRef(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 3. The logic to convert pixels to a file
  const downloadQR = () => {
    // Find the <canvas> element inside our qrRef div
    const canvas = qrRef.current.querySelector("canvas");
    if (!canvas) return;

    // Convert the canvas to a Base64 image string
    const image = canvas.toDataURL("image/png");
    
    // Create a temporary link and "click" it to trigger the download
    const link = document.createElement("a");
    link.href = image;
    link.download = `HealthQR-${formData.full_name}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/register', formData);
      setQrToken(response.data.qr_token);
    } catch (error) {
      alert("Registration failed. Check if backend is running.");
    }
  };

  const inputClass = "border border-gray-300 p-2 rounded text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500";

  return (
    <div className="p-4 max-w-xl mx-auto bg-white rounded-xl shadow-md border border-gray-100">
      {!qrToken ? (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <h2 className="text-xl font-bold text-blue-700 mb-2">Patient Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input name="full_name" type="text" placeholder="Full Name" onChange={handleChange} className={inputClass} required />
            <input name="email" type="email" placeholder="Email" onChange={handleChange} className={inputClass} required />
            <input name="age" type="number" placeholder="Age" onChange={handleChange} className={inputClass} required />
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

          <textarea name="allergies" placeholder="Allergies" onChange={handleChange} className={inputClass + " h-20"}/>
          <textarea name="medical_history" placeholder="Medical History" onChange={handleChange} className={inputClass + " h-20"} />

          <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white font-bold p-3 rounded transition shadow-lg">
            Register & Generate HealthQR
          </button>
        </form>
      ) : (
        <div className="text-center p-6">
          <h2 className="text-2xl font-bold text-green-600 mb-6">Registration Successful!</h2>
          
          {/* 4. We wrap the QR in a div and give it the 'ref' */}
          <div ref={qrRef} className="bg-white p-6 inline-block rounded-xl shadow-2xl border-4 border-blue-50">
            <QRCodeCanvas value={qrToken} size={256} />
          </div>

          <div className="mt-8 flex flex-col gap-3">
            {/* 5. The new Download Button */}
            <button 
              onClick={downloadQR}
              className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition shadow-md flex items-center justify-center gap-2"
            >
              <span>📥</span> Download QR Image
            </button>
            
            <button onClick={() => setQrToken(null)} className="text-blue-500 hover:text-blue-700 font-medium">
              ← Register another patient
            </button>
          </div>
        </div>
      )}
    </div>
  );
}