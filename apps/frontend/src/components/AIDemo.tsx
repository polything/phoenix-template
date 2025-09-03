"use client";

import { useState } from "react";
import { Loader2, Sparkles, CheckCircle, AlertCircle, Brain } from "lucide-react";

interface AIResponse {
  content: string;
  model_used: string;
  langsmith_enabled: boolean;
}

export default function AIDemo() {
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [response, setResponse] = useState<AIResponse | null>(null);
  const [error, setError] = useState<string>("");

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError("Please enter a prompt");
      return;
    }

    setIsGenerating(true);
    setError("");
    setResponse(null);

    try {
      const res = await fetch("http://localhost:8000/api/ai/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });

      if (res.ok) {
        const data = await res.json();
        setResponse(data);
      } else {
        throw new Error("Failed to generate content");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate content");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    setPrompt("");
    setResponse(null);
    setError("");
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <div className="flex items-center mb-6">
        <Brain className="w-6 h-6 text-purple-600 mr-2" />
        <h2 className="font-headline text-2xl font-semibold text-gray-900">
          AI Demo
        </h2>
      </div>

      {!response ? (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              AI Prompt *
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="Enter a prompt for the AI to generate content..."
            />
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
              <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
              <p className="text-red-700">{error}</p>
            </div>
          )}

          <button
            onClick={handleGenerate}
            disabled={isGenerating || !prompt.trim()}
            className="w-full bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isGenerating ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5 mr-2" />
                Generate with AI
              </>
            )}
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <CheckCircle className="w-6 h-6 text-green-500 mr-2" />
              <h3 className="font-headline text-xl font-semibold text-gray-900">
                AI Generated Content
              </h3>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">Model:</span>
              <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                {response.model_used}
              </span>
              {response.langsmith_enabled && (
                <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                  LangSmith
                </span>
              )}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Generated Content
            </label>
            <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <pre className="whitespace-pre-wrap text-gray-800 font-sans">
                {response.content}
              </pre>
            </div>
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleReset}
              className="flex-1 bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              Try Another Prompt
            </button>
            <button
              onClick={() => navigator.clipboard.writeText(response.content)}
              className="flex-1 bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Copy to Clipboard
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
