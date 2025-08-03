import React, { useState, useEffect } from 'react';
import { GrafanaTheme2, Icon, Button } from '@grafana/ui';
import { css } from '@emotion/css';
import { AIAssistantUI } from './AIAssistantUI';

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

interface AISidebarPanelProps {
  theme: GrafanaTheme2;
  isOpen: boolean;
  onToggle: () => void;
}

export const AISidebarPanel: React.FC<AISidebarPanelProps> = ({ 
  theme, 
  isOpen, 
  onToggle 
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [capabilities, setCapabilities] = useState<any>(null);

  const aiServiceUrl = process.env.REACT_APP_AI_SERVICE_URL || 'http://localhost:5000';

  useEffect(() => {
    if (isOpen) {
      loadCapabilities();
    }
  }, [isOpen]);

  const loadCapabilities = async () => {
    try {
      const response = await fetch(`${aiServiceUrl}/api/capabilities`);
      const data = await response.json();
      setCapabilities(data);
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
      const response = await fetch(`${aiServiceUrl}/ai/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: input,
          context: await getCurrentDashboardContext(),
        }),
      });

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response || data.message,
        timestamp: new Date(),
        type: data.type || 'text',
        data: data.data,
      };

      setMessages(prev => [...prev, assistantMessage]);

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
      const response = await fetch('/api/dashboards/uid/current');
      const dashboard = await response.json();
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

  const quickActions: QuickAction[] = [
    {
      label: 'CPU Analysis',
      action: () => handleSendMessage('Analyze CPU usage'),
      icon: 'processor',
    },
    {
      label: 'Memory Check',
      action: () => handleSendMessage('Check memory usage'),
      icon: 'database',
    },
    {
      label: 'Find Issues',
      action: () => handleSendMessage('Find system issues'),
      icon: 'exclamation-triangle',
    },
  ];

  const styles = {
    container: css`
      position: fixed;
      top: 0;
      right: ${isOpen ? '0' : '-400px'};
      width: 400px;
      height: 100vh;
      background: ${theme.colors.background.primary};
      border-left: 1px solid ${theme.colors.border.weak};
      box-shadow: ${theme.shadows.z3};
      z-index: 1000;
      transition: right 0.3s ease;
      display: flex;
      flex-direction: column;
    `,
    toggleButton: css`
      position: fixed;
      top: 50%;
      right: ${isOpen ? '400px' : '0'};
      transform: translateY(-50%);
      z-index: 1001;
      background: ${theme.colors.primary.main};
      color: ${theme.colors.primary.contrastText};
      border: none;
      border-radius: ${theme.shape.borderRadius(1)} 0 0 ${theme.shape.borderRadius(1)};
      padding: ${theme.spacing(1)};
      cursor: pointer;
      box-shadow: ${theme.shadows.z2};
      transition: right 0.3s ease;
      
      &:hover {
        background: ${theme.colors.primary.shade};
      }
    `,
    header: css`
      padding: ${theme.spacing(1, 2)};
      background: ${theme.colors.background.secondary};
      border-bottom: 1px solid ${theme.colors.border.weak};
      display: flex;
      align-items: center;
      justify-content: space-between;
    `,
    headerTitle: css`
      font-weight: ${theme.typography.fontWeightMedium};
      color: ${theme.colors.text.primary};
      display: flex;
      align-items: center;
      gap: ${theme.spacing(1)};
    `,
    closeButton: css`
      background: none;
      border: none;
      color: ${theme.colors.text.secondary};
      cursor: pointer;
      padding: ${theme.spacing(0.5)};
      border-radius: ${theme.shape.borderRadius(1)};
      
      &:hover {
        background: ${theme.colors.action.hover};
      }
    `,
    content: css`
      flex: 1;
      overflow: hidden;
    `,
  };

  return (
    <>
      <button className={styles.toggleButton} onClick={onToggle}>
        <Icon name={isOpen ? 'angle-right' : 'angle-left'} />
      </button>
      
      <div className={styles.container}>
        <div className={styles.header}>
          <div className={styles.headerTitle}>
            <Icon name="robot" />
            AI Assistant
          </div>
          <button className={styles.closeButton} onClick={onToggle}>
            <Icon name="times" />
          </button>
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
          />
        </div>
      </div>
    </>
  );
}; 