"use client";

import { useState } from "react";
import { CheckCircle, AlertCircle, Loader2 } from "lucide-react";

interface FormData {
  name: string;
  email: string;
  company: string;
  website: string;
  services: string[];
  industry: string;
  companySize: string;
  painPoints: string[];
  positioning: string;
  platforms: string[];
  contentTypes: string[];
  tone: string;
}

const initialFormData: FormData = {
  name: "",
  email: "",
  company: "",
  website: "",
  services: [],
  industry: "",
  companySize: "",
  painPoints: [],
  positioning: "",
  platforms: [],
  contentTypes: [],
  tone: "",
};

interface ClientIntakeFormProps {
  onSuccess?: (clientId: string) => void;
}

export default function ClientIntakeForm({ onSuccess }: ClientIntakeFormProps) {
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<"idle" | "success" | "error">("idle");
  const [errors, setErrors] = useState<Record<string, string>>({});

  const totalSteps = 4;

  const handleInputChange = (field: keyof FormData, value: string | string[]) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: "" }));
    }
  };

  const handleArrayToggle = (field: keyof FormData, value: string) => {
    const currentArray = formData[field] as string[];
    const newArray = currentArray.includes(value)
      ? currentArray.filter(item => item !== value)
      : [...currentArray, value];
    handleInputChange(field, newArray);
  };

  const validateStep = (step: number): boolean => {
    const newErrors: Record<string, string> = {};

    switch (step) {
      case 1:
        if (!formData.name.trim()) newErrors.name = "Name is required";
        if (!formData.email.trim()) newErrors.email = "Email is required";
        if (!formData.email.includes("@")) newErrors.email = "Please enter a valid email";
        break;
      case 2:
        if (formData.services.length === 0) newErrors.services = "Please select at least one service";
        if (!formData.industry.trim()) newErrors.industry = "Industry is required";
        if (!formData.companySize.trim()) newErrors.companySize = "Company size is required";
        break;
      case 3:
        if (formData.painPoints.length === 0) newErrors.painPoints = "Please select at least one pain point";
        if (!formData.positioning.trim()) newErrors.positioning = "Positioning statement is required";
        break;
      case 4:
        if (formData.platforms.length === 0) newErrors.platforms = "Please select at least one platform";
        if (formData.contentTypes.length === 0) newErrors.contentTypes = "Please select at least one content type";
        break;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, totalSteps));
    }
  };

  const handlePrevious = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const handleSubmit = async () => {
    if (!validateStep(currentStep)) return;

    setIsSubmitting(true);
    setSubmitStatus("idle");

    try {
      // Transform form data to match backend API structure
      const payload = {
        name: formData.name,
        email: formData.email,
        company: formData.company || undefined,
        website: formData.website || undefined,
        service_offering: {
          services: formData.services,
          pricing_tier: "premium", // Default for demo
        },
        icp_profile: {
          industry: formData.industry,
          company_size: formData.companySize,
          pain_points: formData.painPoints,
        },
        positioning_statement: formData.positioning,
        content_preferences: {
          platforms: formData.platforms,
          frequency: "weekly", // Default for demo
          content_types: formData.contentTypes,
          tone: formData.tone || "professional",
        },
        constraints: {
          brand_safety_level: "high", // Default for demo
        },
      };

      const response = await fetch("http://localhost:8000/api/clients/intake", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const result = await response.json();
        setSubmitStatus("success");
        // Call the success callback with the client ID
        if (onSuccess && result.id) {
          onSuccess(result.id);
        }
      } else {
        throw new Error("Failed to submit form");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      setSubmitStatus("error");
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <h2 className="font-headline text-2xl font-semibold text-gray-900">
              Basic Information
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => handleInputChange("name", e.target.value)}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                    errors.name ? "border-red-500" : "border-gray-300"
                  }`}
                  placeholder="Enter your full name"
                />
                {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address *
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange("email", e.target.value)}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                    errors.email ? "border-red-500" : "border-gray-300"
                  }`}
                  placeholder="Enter your email address"
                />
                {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Company Name
                </label>
                <input
                  type="text"
                  value={formData.company}
                  onChange={(e) => handleInputChange("company", e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="Enter your company name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Website URL
                </label>
                <input
                  type="url"
                  value={formData.website}
                  onChange={(e) => handleInputChange("website", e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="https://your-website.com"
                />
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <h2 className="font-headline text-2xl font-semibold text-gray-900">
              Business Details
            </h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Services You Offer *
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {["Content Strategy", "LinkedIn Management", "Newsletter Marketing", "SEO Services", "Social Media Management", "Brand Consulting"].map((service) => (
                  <button
                    key={service}
                    type="button"
                    onClick={() => handleArrayToggle("services", service)}
                    className={`p-3 text-sm rounded-lg border transition-colors ${
                      formData.services.includes(service)
                        ? "bg-purple-100 border-purple-500 text-purple-700"
                        : "bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
                    }`}
                  >
                    {service}
                  </button>
                ))}
              </div>
              {errors.services && <p className="text-red-500 text-sm mt-1">{errors.services}</p>}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Industry *
                </label>
                <select
                  value={formData.industry}
                  onChange={(e) => handleInputChange("industry", e.target.value)}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                    errors.industry ? "border-red-500" : "border-gray-300"
                  }`}
                >
                  <option value="">Select your industry</option>
                  <option value="SaaS">SaaS</option>
                  <option value="E-commerce">E-commerce</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Finance">Finance</option>
                  <option value="Education">Education</option>
                  <option value="Consulting">Consulting</option>
                  <option value="Other">Other</option>
                </select>
                {errors.industry && <p className="text-red-500 text-sm mt-1">{errors.industry}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Company Size *
                </label>
                <select
                  value={formData.companySize}
                  onChange={(e) => handleInputChange("companySize", e.target.value)}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                    errors.companySize ? "border-red-500" : "border-gray-300"
                  }`}
                >
                  <option value="">Select company size</option>
                  <option value="1-10 employees">1-10 employees</option>
                  <option value="11-50 employees">11-50 employees</option>
                  <option value="51-200 employees">51-200 employees</option>
                  <option value="201-500 employees">201-500 employees</option>
                  <option value="500+ employees">500+ employees</option>
                </select>
                {errors.companySize && <p className="text-red-500 text-sm mt-1">{errors.companySize}</p>}
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <h2 className="font-headline text-2xl font-semibold text-gray-900">
              Target Audience & Positioning
            </h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Main Pain Points You Solve *
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {[
                  "Inconsistent content",
                  "Low engagement",
                  "Lack of strategy",
                  "Time constraints",
                  "Poor ROI",
                  "Brand awareness",
                ].map((painPoint) => (
                  <button
                    key={painPoint}
                    type="button"
                    onClick={() => handleArrayToggle("painPoints", painPoint)}
                    className={`p-3 text-sm rounded-lg border transition-colors ${
                      formData.painPoints.includes(painPoint)
                        ? "bg-purple-100 border-purple-500 text-purple-700"
                        : "bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
                    }`}
                  >
                    {painPoint}
                  </button>
                ))}
              </div>
              {errors.painPoints && <p className="text-red-500 text-sm mt-1">{errors.painPoints}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Positioning Statement *
              </label>
              <textarea
                value={formData.positioning}
                onChange={(e) => handleInputChange("positioning", e.target.value)}
                rows={4}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.positioning ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="Describe how you position your services and what makes you unique..."
              />
              {errors.positioning && <p className="text-red-500 text-sm mt-1">{errors.positioning}</p>}
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <h2 className="font-headline text-2xl font-semibold text-gray-900">
              Content Preferences
            </h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Preferred Platforms *
              </label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {["linkedin", "newsletter", "blog", "twitter"].map((platform) => (
                  <button
                    key={platform}
                    type="button"
                    onClick={() => handleArrayToggle("platforms", platform)}
                    className={`p-3 text-sm rounded-lg border transition-colors capitalize ${
                      formData.platforms.includes(platform)
                        ? "bg-purple-100 border-purple-500 text-purple-700"
                        : "bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
                    }`}
                  >
                    {platform}
                  </button>
                ))}
              </div>
              {errors.platforms && <p className="text-red-500 text-sm mt-1">{errors.platforms}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Content Types *
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {["educational", "thought_leadership", "promotional", "case_study"].map((type) => (
                  <button
                    key={type}
                    type="button"
                    onClick={() => handleArrayToggle("contentTypes", type)}
                    className={`p-3 text-sm rounded-lg border transition-colors ${
                      formData.contentTypes.includes(type)
                        ? "bg-purple-100 border-purple-500 text-purple-700"
                        : "bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
                    }`}
                  >
                    {type.replace("_", " ")}
                  </button>
                ))}
              </div>
              {errors.contentTypes && <p className="text-red-500 text-sm mt-1">{errors.contentTypes}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Preferred Tone
              </label>
              <select
                value={formData.tone}
                onChange={(e) => handleInputChange("tone", e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="">Select tone (optional)</option>
                <option value="professional">Professional</option>
                <option value="casual">Casual</option>
                <option value="friendly">Friendly</option>
                <option value="authoritative">Authoritative</option>
                <option value="conversational">Conversational</option>
              </select>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  if (submitStatus === "success") {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 text-center">
        <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
        <h2 className="font-headline text-2xl font-semibold text-gray-900 mb-2">
          Client Profile Created!
        </h2>
        <p className="text-gray-600 mb-6">
          Your client profile has been successfully created. You can now generate AI-powered content using your profile information.
        </p>
        <p className="text-sm text-gray-500 mb-6">
          The content generator will appear below...
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Progress Bar */}
      <div className="bg-gray-50 px-8 py-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-600">
            Step {currentStep} of {totalSteps}
          </span>
          <span className="text-sm text-gray-500">
            {Math.round((currentStep / totalSteps) * 100)}% Complete
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-purple-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${(currentStep / totalSteps) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Form Content */}
      <div className="p-8">
        {renderStep()}

        {/* Error Message */}
        {submitStatus === "error" && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
            <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
            <p className="text-red-700">
              There was an error submitting your form. Please try again.
            </p>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-8">
          <button
            onClick={handlePrevious}
            disabled={currentStep === 1}
            className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>

          {currentStep < totalSteps ? (
            <button
              onClick={handleNext}
              className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Next Step
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isSubmitting && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              {isSubmitting ? "Submitting..." : "Submit Form"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
