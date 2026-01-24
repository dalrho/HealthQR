"use client";
// We use "../../../" because we are now deeper in the folder structure 
// (app > register > page.tsx)
import RegisterForm from "../../components/RegisterForm";

export default function RegisterPage() {
  return (
    <main className="flex min-h-screen flex-col items-center p-12 bg-gray-50">
      <div className="z-10 max-w-5xl w-full items-center justify-between">
        <h1 className="text-4xl font-black text-center mb-10 text-blue-800 uppercase italic">
          Citizen Registration
        </h1>
        <RegisterForm />
      </div>
    </main>
  );
}