import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-blue-600 text-white p-6">
      <div className="text-center mb-12">
        <h1 className="text-6xl font-black italic tracking-tighter mb-2">NAGA HealthQR</h1>
        <p className="text-blue-100 text-lg font-medium opacity-90">Secure Medical Response System</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-2xl">
        {/* Redirects to app/register/page.tsx */}
        <Link href="/register" className="bg-white text-blue-600 p-10 rounded-[2.5rem] shadow-2xl hover:scale-105 transition-all group flex flex-col items-center">
          <span className="text-5xl block mb-4 group-hover:animate-bounce">📋</span>
          <span className="text-2xl font-black uppercase block">Citizen</span>
          <span className="text-sm opacity-70">Register & Get QR</span>
        </Link>
        
        {/* Redirects to app/login/page.tsx */}
        <Link href="/login" className="bg-blue-800 text-white p-10 rounded-[2.5rem] shadow-2xl border-4 border-blue-400 hover:scale-105 transition-all group flex flex-col items-center">
          <span className="text-5xl block mb-4 group-hover:rotate-12 transition-transform">🏥</span>
          <span className="text-2xl font-black uppercase block">Medic</span>
          <span className="text-sm opacity-70">Scanner Portal</span>
        </Link>
      </div>
      
      <footer className="mt-16 text-blue-300 text-xs font-mono">
        OFFICIAL NAGA CITY HEALTH PROTOCOL v1.0
      </footer>
    </div>
  );
}