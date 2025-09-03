"use client";

import { useState, useEffect } from "react";
import { Loader2, AlertCircle, RefreshCw } from "lucide-react";

interface ExampleItem {
  id: string;
  name: string;
  description?: string;
  email?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export default function ExampleList() {
  const [items, setItems] = useState<ExampleItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>("");

  const fetchItems = async () => {
    try {
      setIsLoading(true);
      setError("");
      
      const response = await fetch("http://localhost:8000/api/example/items");
      
      if (response.ok) {
        const data = await response.json();
        setItems(data);
      } else {
        throw new Error("Failed to fetch items");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch items");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleRefresh = () => {
    fetchItems();
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 text-center">
        <Loader2 className="w-8 h-8 text-purple-600 mx-auto mb-4 animate-spin" />
        <p className="text-gray-600">Loading items...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-headline text-2xl font-semibold text-gray-900">
            Example Items
          </h2>
          <button
            onClick={handleRefresh}
            className="flex items-center px-4 py-2 text-sm text-purple-600 hover:text-purple-700 transition-colors"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </button>
        </div>
        
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
          <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="font-headline text-2xl font-semibold text-gray-900">
          Example Items ({items.length})
        </h2>
        <button
          onClick={handleRefresh}
          className="flex items-center px-4 py-2 text-sm text-purple-600 hover:text-purple-700 transition-colors"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </button>
      </div>

      {items.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-500 mb-4">No items found.</p>
          <p className="text-sm text-gray-400">
            Create your first item using the form above.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <div
              key={item.id}
              className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {item.name}
                  </h3>
                  {item.description && (
                    <p className="text-gray-600 text-sm mb-2">
                      {item.description}
                    </p>
                  )}
                  {item.email && (
                    <p className="text-gray-500 text-sm">
                      {item.email}
                    </p>
                  )}
                </div>
                <div className="flex items-center space-x-2 ml-4">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      item.is_active
                        ? "bg-green-100 text-green-800"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {item.is_active ? "Active" : "Inactive"}
                  </span>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-400">
                Created: {new Date(item.created_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
