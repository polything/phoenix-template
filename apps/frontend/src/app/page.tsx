"use client";

import { useState } from "react";
import ClientIntakeForm from "@/components/ClientIntakeForm";
import ContentGenerator from "@/components/ContentGenerator";

export default function Home() {
  const [clientId, setClientId] = useState<string>("");
  const [showContentGenerator, setShowContentGenerator] = useState(false);

  const handleFormSuccess = (clientId: string) => {
    setClientId(clientId);
    setShowContentGenerator(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="font-headline text-4xl font-bold text-gray-900 mb-4">
            AI-Enhanced Content Pipeline
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transform your content strategy with AI-powered automation. 
            Get started by telling us about your business.
          </p>
        </header>
        
        <main className="max-w-4xl mx-auto space-y-8">
          {!showContentGenerator ? (
            <ClientIntakeForm onSuccess={handleFormSuccess} />
          ) : (
            <ContentGenerator clientId={clientId} />
          )}
        </main>
      </div>
    </div>
  );
}
