"use client";

import { useState } from "react";
import { Loader2, Sparkles, CheckCircle, AlertCircle } from "lucide-react";
import { pipelineAPI, PipelineRequest } from "@/lib/api/pipeline";

interface ContentGeneratorProps {
  clientId: string;
}

export default function ContentGenerator({ clientId }: ContentGeneratorProps) {
  const [prompt, setPrompt] = useState("");
  const [contentType, setContentType] = useState("linkedin_post");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState<string>("");
  const [qualityScore, setQualityScore] = useState<number>(0);
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState(false);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError("Please enter a prompt");
      return;
    }

    setIsGenerating(true);
    setError("");
    setSuccess(false);
    setGeneratedContent("");

    try {
      const request: PipelineRequest = {
        client_id: clientId,
        content_type: contentType,
        prompt: prompt.trim(),
        context: {
          platform: contentType,
          tone: "professional",
        },
      };

      const response = await pipelineAPI.generateContent(request);
      
      setGeneratedContent(response.content);
      setQualityScore(response.quality_score);
      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate content");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    setPrompt("");
    setGeneratedContent("");
    setQualityScore(0);
    setError("");
    setSuccess(false);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <div className="flex items-center mb-6">
        <Sparkles className="w-6 h-6 text-purple-600 mr-2" />
        <h2 className="font-headline text-2xl font-semibold text-gray-900">
          AI Content Generator
        </h2>
      </div>

      {!success ? (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content Type
            </label>
            <select
              value={contentType}
              onChange={(e) => setContentType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="linkedin_post">LinkedIn Post</option>
              <option value="newsletter">Newsletter</option>
              <option value="blog_post">Blog Post</option>
              <option value="lead_magnet">Lead Magnet</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content Prompt *
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="Describe what kind of content you want to generate..."
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
                Generating Content...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5 mr-2" />
                Generate Content
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
                Content Generated Successfully!
              </h3>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">Quality Score:</span>
              <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                {qualityScore.toFixed(1)}/10
              </span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Generated Content
            </label>
            <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <pre className="whitespace-pre-wrap text-gray-800 font-sans">
                {generatedContent}
              </pre>
            </div>
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleReset}
              className="flex-1 bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              Generate New Content
            </button>
            <button
              onClick={() => navigator.clipboard.writeText(generatedContent)}
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
