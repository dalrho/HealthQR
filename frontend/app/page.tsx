"use client";

// The "../" means "go out of the app folder and into the frontend folder"
import RegisterForm from "../components/RegisterForm";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-10 text-blue-600">
          HealthQR: Naga Smart City
        </h1>
        <RegisterForm />
      </div>
    </main>
  );
}