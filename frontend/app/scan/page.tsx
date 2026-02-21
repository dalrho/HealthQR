"use client";
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

export default function ScanPage() {
  const [patientData, setPatientData] = useState<any>(null);
  const [isScanning, setIsScanning] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = sessionStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    const verify = async () => {
      try {
        await axios.get('http://localhost:8000/medic/verify', {
          headers: { Authorization: `Bearer ${token}` }
        });
      } catch (err) {
        sessionStorage.removeItem('token');
        router.push('/login');
      }
    };
    verify();
  }, [router]);

  useEffect(() => {
    if (!isScanning) return;

    let scanner: any;

    const timer = setTimeout(async () => {
      const { Html5QrcodeScanner } = await import("html5-qrcode");
      
      scanner = new Html5QrcodeScanner(
        "reader", 
        { fps: 10, qrbox: { width: 250, height: 250 } }, 
        false
      );

      scanner.render(
        async (decodedText: string) => {
          try {
            await scanner.clear(); 
            onScanSuccess(decodedText);
          } catch (e) {
            console.error("Scanner clear failed", e);
          }
        },
        () => {} 
      );
    }, 300);

    return () => {
      clearTimeout(timer);
      if (scanner) {
        scanner.clear().catch((e: any) => console.warn(e));
      }
    };
  }, [isScanning]);

  const onScanSuccess = async (decodedText: string) => {
    try {
      const token = sessionStorage.getItem('token');
      const res = await axios.get(`http://localhost:8000/scan/${decodedText}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPatientData(res.data);
      setIsScanning(false);
    } catch (err) {
      alert("Access Denied or Patient Not Found.");
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('token');
    router.push('/login');
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <button 
        onClick={handleLogout}
        className="fixed top-6 right-6 bg-red-50 text-red-600 font-bold px-4 py-2 rounded-full hover:bg-red-600 hover:text-white transition-all shadow-sm z-50"
      >
        LOGOUT
      </button>

      <div className="max-w-3xl mx-auto mt-12">
        <h1 className="text-3xl font-black text-center mb-10 text-slate-800 tracking-tighter italic">NAGA MEDIC PORTAL</h1>
        
        {isScanning ? (
          <div className="bg-white p-4 rounded-3xl shadow-xl border-4 border-white overflow-hidden">
            <div id="reader" className="rounded-2xl overflow-hidden"></div>
            <p className="text-center mt-4 text-gray-400 font-medium">Scanning for HealthQR...</p>
          </div>
        ) : (
          <div className="bg-white p-8 rounded-3xl shadow-2xl animate-in zoom-in-95 border-t-8 border-blue-600">
             <div className="mb-6">
                <span className="text-xs font-bold text-blue-500 uppercase tracking-widest">Patient Identity</span>
                <h2 className="text-4xl font-black text-slate-900">{patientData?.full_name}</h2>
             </div>

             <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-red-50 p-4 rounded-2xl border border-red-100">
                   <span className="text-xs font-bold text-red-400 uppercase">Blood Type</span>
                   <p className="text-2xl font-black text-red-600">{patientData?.blood_type}</p>
                </div>
                <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                   <span className="text-xs font-bold text-slate-400 uppercase">Age</span>
                   <p className="text-2xl font-black text-slate-700">{patientData?.age}</p>
                </div>
             </div>

             <div className="space-y-4">
                <div className="bg-blue-50 p-4 rounded-2xl border border-blue-100">
                   <span className="text-xs font-bold text-blue-400 uppercase">Emergency Contact</span>
                   <p className="font-bold text-slate-800">{patientData?.emergency_contact_name}</p>
                   <p className="text-blue-600 font-mono">{patientData?.emergency_contact_phone}</p>
                </div>
                <div className="p-4 rounded-2xl border border-gray-100">
                   <span className="text-xs font-bold text-gray-400 uppercase">Known Allergies</span>
                   <p className="text-slate-700">{patientData?.allergies || "None declared"}</p>
                </div>
             </div>
             
             <button 
               onClick={() => setIsScanning(true)}
               className="w-full mt-10 bg-blue-600 text-white py-4 rounded-2xl font-black hover:bg-blue-700 shadow-lg shadow-blue-200 transition-all active:scale-95 uppercase tracking-widest"
             >
               Ready for Next Scan
             </button>
          </div>
        )}
      </div>
    </main>
  );
}