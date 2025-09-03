/**
 * Pipeline API client for content generation.
 * Handles communication with the backend pipeline endpoints.
 */

export interface PipelineRequest {
  client_id: string;
  content_type: string;
  prompt: string;
  context?: Record<string, unknown>;
  model?: string;
}

export interface PipelineResponse {
  pipeline_run_id: string;
  content: string;
  quality_score: number;
  processing_time: number;
  metadata: Record<string, unknown>;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class PipelineAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Generate content using the AI pipeline.
   */
  async generateContent(request: PipelineRequest): Promise<PipelineResponse> {
    const response = await fetch(`${this.baseUrl}/api/pipeline/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    return response.json();
  }

  /**
   * Get pipeline run details by ID.
   */
  async getPipelineRun(runId: string): Promise<PipelineResponse> {
    const response = await fetch(`${this.baseUrl}/api/pipeline/runs/${runId}`);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    return response.json();
  }

  /**
   * Get pipeline runs for a specific client.
   */
  async getClientPipelineRuns(
    clientId: string,
    limit: number = 10,
    offset: number = 0
  ): Promise<{ runs: PipelineResponse[]; total: number }> {
    const response = await fetch(
      `${this.baseUrl}/api/pipeline/clients/${clientId}/runs?limit=${limit}&offset=${offset}`
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    return response.json();
  }
}

// Export a default instance
export const pipelineAPI = new PipelineAPI();
