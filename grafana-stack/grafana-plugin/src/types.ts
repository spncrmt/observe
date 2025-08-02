export interface AIAssistantOptions {
  aiServiceUrl: string;
  enableContextAwareness: boolean;
  defaultModel: string;
}

export interface AIRequest {
  input: string;
  context?: GrafanaContext;
}

export interface AIResponse {
  type: 'response' | 'action' | 'error' | 'anomaly';
  message: string;
  action?: string;
  success?: boolean;
  panel_config?: any;
  suggestions?: string[];
  analysis?: any;
  query?: string;
  result?: any;
}

export interface GrafanaContext {
  dashboard_id?: string;
  panel_id?: string;
  time_range?: {
    from: string;
    to: string;
  };
  variables?: Record<string, any>;
  data_sources?: string[];
  selected_metrics?: string[];
}

export interface AICapabilities {
  natural_language: {
    description: string;
    examples: string[];
  };
  panel_management: {
    description: string;
    actions: string[];
  };
  query_generation: {
    description: string;
    supported_metrics: string[];
  };
  anomaly_detection: {
    description: string;
    methods: string[];
  };
  context_awareness: {
    description: string;
    context_items: string[];
  };
} 