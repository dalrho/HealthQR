"use client";
import { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const res = await axios.post('http://localhost:8000/medic/login', formData);
      
      // SWITCHED: Use sessionStorage instead of localStorage
      sessionStorage.setItem('token', res.data.access_token);
      
      router.push('/scan');
    } catch (err) {
      alert("Unauthorized access denied.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 p-6">
      <form onSubmit={handleLogin} className="bg-white p-8 rounded-3xl shadow-2xl w-full max-w-md">
        <h1 className="text-2xl font-black mb-8 text-center text-slate-800 uppercase italic">Medic Portal</h1>
        <input 
          type="text" placeholder="Username" disabled={isLoading}
          className="w-full p-4 mb-4 border rounded-2xl bg-slate-50 outline-none focus:ring-2 focus:ring-blue-500"
          onChange={(e) => setUsername(e.target.value)}
        />
        <input 
          type="password" placeholder="Password" disabled={isLoading}
          className="w-full p-4 mb-8 border rounded-2xl bg-slate-50 outline-none focus:ring-2 focus:ring-blue-500"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button disabled={isLoading} className="w-full bg-blue-600 text-white font-bold py-4 rounded-2xl hover:bg-blue-700 transition flex items-center justify-center gap-2">
          {isLoading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : "LOGIN"}
        </button>
      </form>
    </div>
  );
}