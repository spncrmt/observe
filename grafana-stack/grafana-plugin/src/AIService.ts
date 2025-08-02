import { AIRequest, AIResponse, GrafanaContext } from './types';

export class AIService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async processRequest(input: string, context?: GrafanaContext): Promise<AIResponse> {
    const response = await fetch(`${this.baseUrl}/ai/api/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        input,
        context,
      }),
    });

    if (!response.ok) {
      throw new Error(`AI service error: ${response.statusText}`);
    }

    return response.json();
  }

  async getCapabilities(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/capabilities`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to get capabilities: ${response.statusText}`);
    }

    return response.json();
  }

  async updateContext(context: GrafanaContext): Promise<void> {
    const response = await fetch(`${this.baseUrl}/ai/api/context`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(context),
    });

    if (!response.ok) {
      throw new Error(`Failed to update context: ${response.statusText}`);
    }
  }

  async executeQuery(query: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/ai/api/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`Failed to execute query: ${response.statusText}`);
    }

    return response.json();
  }

  async analyzeAnomaly(metric: string, timeRange: string = '1h'): Promise<any> {
    const response = await fetch(`${this.baseUrl}/ai/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ metric, time_range: timeRange }),
    });

    if (!response.ok) {
      throw new Error(`Failed to analyze anomaly: ${response.statusText}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        method: 'GET',
      });
      return response.ok;
    } catch {
      return false;
    }
  }
} 