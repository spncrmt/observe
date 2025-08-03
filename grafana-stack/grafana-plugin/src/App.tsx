import React, { useState, useEffect } from 'react';
import { AppRootProps } from '@grafana/data';
import { getBackendSrv } from '@grafana/runtime';
import { AIAssistantUI } from './AIAssistantUI';
import { GrafanaTheme2 } from '@grafana/ui';
import { css } from '@emotion/css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  type?: 'text' | 'query' | 'chart' | 'insight';
  data?: any;
}

interface QuickAction {
  label: string;
  action: () => void;
  icon?: string;
}

export const App: React.FC<AppRootProps> = ({ theme }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [capabilities, setCapabilities] = useState<any>(null);

  const aiServiceUrl = process.env.REACT_APP_AI_SERVICE_URL || 'http://localhost:5000';

  useEffect(() => {
    // Load initial capabilities
    loadCapabilities();
  }, []);

  const loadCapabilities = async () => {
    try {
      const response = await getBackendSrv().get(`${aiServiceUrl}/api/capabilities`);
      setCapabilities(response);
    } catch (err) {
      console.error('Failed to load AI capabilities:', err);
    }
  };

  const handleSendMessage = async (input: string) => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Get current dashboard context
      const dashboard = await getCurrentDashboardContext();
      
      const response = await getBackendSrv().post(`${aiServiceUrl}/ai/api/query`, {
        query: input,
        context: dashboard,
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response || response.message,
        timestamp: new Date(),
        type: response.type || 'text',
        data: response.data,
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Handle special actions
      if (response.action === 'create_panel' && response.panel_config) {
        await createPanel(response.panel_config);
      } else if (response.action === 'execute_query' && response.query) {
        await executeQuery(response.query);
      }

    } catch (err) {
      console.error('Failed to send message:', err);
      setError('Failed to get response from AI service');
    } finally {
      setIsLoading(false);
    }
  };

  const getCurrentDashboardContext = async () => {
    try {
      // Get current dashboard info from Grafana
      const dashboard = await getBackendSrv().get('/api/dashboards/uid/current');
      return {
        dashboard_id: dashboard.dashboard.uid,
        dashboard_title: dashboard.dashboard.title,
        panels: dashboard.dashboard.panels,
        time_range: {
          from: 'now-1h',
          to: 'now',
        },
      };
    } catch (err) {
      console.error('Failed to get dashboard context:', err);
      return null;
    }
  };

  const createPanel = async (panelConfig: any) => {
    try {
      const dashboard = await getCurrentDashboardContext();
      if (!dashboard) return;

      const response = await getBackendSrv().post('/api/dashboards/db', {
        dashboard: {
          ...dashboard,
          panels: [...dashboard.panels, panelConfig],
        },
      });

      if (response.status === 'success') {
        // Refresh the dashboard
        window.location.reload();
      }
    } catch (err) {
      console.error('Failed to create panel:', err);
    }
  };

  const executeQuery = async (query: string) => {
    try {
      const response = await getBackendSrv().get('/api/datasources/proxy/1/api/v1/query', {
        query,
        time: Date.now() / 1000,
      });
      return response;
    } catch (err) {
      console.error('Failed to execute query:', err);
    }
  };

  const quickActions: QuickAction[] = [
    {
      label: 'Analyze CPU',
      action: () => handleSendMessage('Analyze CPU usage and find anomalies'),
      icon: 'processor',
    },
    {
      label: 'Check Memory',
      action: () => handleSendMessage('Check memory usage and identify potential issues'),
      icon: 'database',
    },
    {
      label: 'Create Dashboard',
      action: () => handleSendMessage('Create a new dashboard with system metrics'),
      icon: 'plus',
    },
    {
      label: 'Find Anomalies',
      action: () => handleSendMessage('Find anomalies in the last 24 hours'),
      icon: 'exclamation-triangle',
    },
  ];

  const styles = {
    container: css`
      height: 100vh;
      display: flex;
      flex-direction: column;
      background: ${theme.colors.background.primary};
    `,
    header: css`
      padding: ${theme.spacing(2)};
      background: ${theme.colors.background.secondary};
      border-bottom: 1px solid ${theme.colors.border.weak};
      display: flex;
      align-items: center;
      justify-content: space-between;
    `,
    headerTitle: css`
      font-size: ${theme.typography.h4.fontSize};
      font-weight: ${theme.typography.fontWeightMedium};
      color: ${theme.colors.text.primary};
    `,
    headerSubtitle: css`
      font-size: ${theme.typography.size.sm};
      color: ${theme.colors.text.secondary};
      margin-top: ${theme.spacing(0.5)};
    `,
    content: css`
      flex: 1;
      overflow: hidden;
    `,
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <div className={styles.headerTitle}>AI Observability Assistant</div>
          <div className={styles.headerSubtitle}>
            Ask questions, create dashboards, and analyze your metrics
          </div>
        </div>
      </div>
      
      <div className={styles.content}>
        <AIAssistantUI
          messages={messages}
          isLoading={isLoading}
          error={error}
          onSendMessage={handleSendMessage}
          quickActions={quickActions}
          capabilities={capabilities}
          theme={theme}
          onExecuteQuery={executeQuery}
          onCreatePanel={createPanel}
        />
      </div>
    </div>
  );
}; 