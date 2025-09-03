"use client";

import { useState } from "react";
import ExampleForm from "@/components/ExampleForm";
import ExampleList from "@/components/ExampleList";
import AIDemo from "@/components/AIDemo";

export default function Home() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleItemSuccess = (_id: string) => {
    // Trigger a refresh of the list
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="font-headline text-4xl font-bold text-gray-900 mb-4">
            Phoenix Template
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            A modern full-stack application template with FastAPI backend and Next.js frontend. 
            Built with TypeScript, Tailwind CSS, and modern development practices.
          </p>
        </header>
        
        <main className="max-w-4xl mx-auto space-y-8">
          <AIDemo />
          <ExampleForm onSuccess={handleItemSuccess} />
          <ExampleList key={refreshKey} />
        </main>
      </div>
    </div>
  );
}
