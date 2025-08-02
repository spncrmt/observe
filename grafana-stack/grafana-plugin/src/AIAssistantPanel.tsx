import React, { useState, useEffect, useCallback } from 'react';
import { PanelProps } from '@grafana/data';
import { useTheme2 } from '@grafana/ui';
import { AIAssistantOptions, AIRequest, AIResponse, GrafanaContext } from './types';
import { AIAssistantUI } from './AIAssistantUI';
import { AIService } from './AIService';

interface Props extends PanelProps<AIAssistantOptions> {}

export const AIAssistantPanel: React.FC<Props> = ({ options, data, width, height }) => {
  const theme = useTheme2();
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string; timestamp: Date }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [capabilities, setCapabilities] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const aiService = new AIService(options.aiServiceUrl);

  // Get current Grafana context
  const getCurrentContext = useCallback((): GrafanaContext => {
    const dashboard = (window as any).grafanaBootData?.settings;
    const timeRange = (window as any).grafanaBootData?.timeRange;
    
    return {
      dashboard_id: dashboard?.dashboard?.uid,
      time_range: timeRange ? {
        from: timeRange.from,
        to: timeRange.to,
      } : undefined,
      data_sources: ['prometheus'],
      selected_metrics: ['node_cpu_seconds_total', 'node_memory_MemTotal_bytes'],
    };
  }, []);

  // Load capabilities on mount
  useEffect(() => {
    const loadCapabilities = async () => {
      try {
        const caps = await aiService.getCapabilities();
        setCapabilities(caps);
      } catch (err) {
        console.error('Failed to load AI capabilities:', err);
        setError('Failed to connect to AI service');
      }
    };

    loadCapabilities();
  }, [aiService]);

  // Send message to AI service
  const sendMessage = async (input: string) => {
    if (!input.trim()) return;

    const userMessage = { role: 'user' as const, content: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const context = options.enableContextAwareness ? getCurrentContext() : undefined;
      const response = await aiService.processRequest(input, context);
      
      const assistantMessage = { 
        role: 'assistant' as const, 
        content: response.message, 
        timestamp: new Date() 
      };
      
      setMessages(prev => [...prev, assistantMessage]);

      // Handle actions
      if (response.type === 'action' && response.success) {
        // Could trigger panel creation, etc.
        console.log('AI Action executed:', response);
      }

    } catch (err) {
      console.error('Failed to process message:', err);
      setError('Failed to get response from AI service');
      
      const errorMessage = { 
        role: 'assistant' as const, 
        content: 'Sorry, I encountered an error. Please try again.', 
        timestamp: new Date() 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Quick actions
  const quickActions = [
    {
      label: 'Create CPU Panel',
      action: () => sendMessage('Create a panel showing CPU usage'),
    },
    {
      label: 'Explain Query',
      action: () => sendMessage('Explain the current query'),
    },
    {
      label: 'Check Anomalies',
      action: () => sendMessage('Check for anomalies in memory usage'),
    },
    {
      label: 'System Health',
      action: () => sendMessage('What is the current system health?'),
    },
  ];

  return (
    <div style={{ width, height, padding: theme.spacing(1) }}>
      <AIAssistantUI
        messages={messages}
        isLoading={isLoading}
        error={error}
        onSendMessage={sendMessage}
        quickActions={quickActions}
        capabilities={capabilities}
        theme={theme}
      />
    </div>
  );
}; 