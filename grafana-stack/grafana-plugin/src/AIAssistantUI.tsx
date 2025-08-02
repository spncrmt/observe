import React, { useState, useRef, useEffect } from 'react';
import { GrafanaTheme2 } from '@grafana/ui';
import { css } from '@emotion/css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface QuickAction {
  label: string;
  action: () => void;
}

interface AIAssistantUIProps {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  onSendMessage: (input: string) => void;
  quickActions: QuickAction[];
  capabilities: any;
  theme: GrafanaTheme2;
}

export const AIAssistantUI: React.FC<AIAssistantUIProps> = ({
  messages,
  isLoading,
  error,
  onSendMessage,
  quickActions,
  capabilities,
  theme,
}) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const styles = {
    container: css`
      display: flex;
      flex-direction: column;
      height: 100%;
      background: ${theme.colors.background.primary};
      border-radius: ${theme.shape.borderRadius(1)};
      overflow: hidden;
    `,
    header: css`
      padding: ${theme.spacing(1, 2)};
      background: ${theme.colors.background.secondary};
      border-bottom: 1px solid ${theme.colors.border.weak};
      display: flex;
      align-items: center;
      gap: ${theme.spacing(1)};
    `,
    headerIcon: css`
      color: ${theme.colors.primary.main};
      font-size: 18px;
    `,
    headerTitle: css`
      font-weight: ${theme.typography.fontWeightMedium};
      color: ${theme.colors.text.primary};
    `,
    messagesContainer: css`
      flex: 1;
      overflow-y: auto;
      padding: ${theme.spacing(1)};
      display: flex;
      flex-direction: column;
      gap: ${theme.spacing(1)};
    `,
    message: css`
      display: flex;
      gap: ${theme.spacing(1)};
      align-items: flex-start;
    `,
    userMessage: css`
      justify-content: flex-end;
    `,
    assistantMessage: css`
      justify-content: flex-start;
    `,
    messageBubble: css`
      max-width: 80%;
      padding: ${theme.spacing(1, 2)};
      border-radius: ${theme.shape.borderRadius(2)};
      word-wrap: break-word;
    `,
    userBubble: css`
      background: ${theme.colors.primary.main};
      color: ${theme.colors.primary.contrastText};
    `,
    assistantBubble: css`
      background: ${theme.colors.background.secondary};
      color: ${theme.colors.text.primary};
      border: 1px solid ${theme.colors.border.weak};
    `,
    inputContainer: css`
      padding: ${theme.spacing(1, 2)};
      border-top: 1px solid ${theme.colors.border.weak};
      background: ${theme.colors.background.primary};
    `,
    inputForm: css`
      display: flex;
      gap: ${theme.spacing(1)};
      align-items: flex-end;
    `,
    input: css`
      flex: 1;
      padding: ${theme.spacing(1, 2)};
      border: 1px solid ${theme.colors.border.medium};
      border-radius: ${theme.shape.borderRadius(1)};
      background: ${theme.colors.background.primary};
      color: ${theme.colors.text.primary};
      font-size: ${theme.typography.size.sm};
      
      &:focus {
        outline: none;
        border-color: ${theme.colors.primary.main};
        box-shadow: 0 0 0 2px ${theme.colors.primary.transparent};
      }
      
      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    `,
    sendButton: css`
      padding: ${theme.spacing(1, 2)};
      background: ${theme.colors.primary.main};
      color: ${theme.colors.primary.contrastText};
      border: none;
      border-radius: ${theme.shape.borderRadius(1)};
      cursor: pointer;
      font-size: ${theme.typography.size.sm};
      
      &:hover:not(:disabled) {
        background: ${theme.colors.primary.shade};
      }
      
      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    `,
    quickActions: css`
      display: flex;
      flex-wrap: wrap;
      gap: ${theme.spacing(0.5)};
      padding: ${theme.spacing(1, 2)};
      border-top: 1px solid ${theme.colors.border.weak};
      background: ${theme.colors.background.secondary};
    `,
    quickActionButton: css`
      padding: ${theme.spacing(0.5, 1)};
      background: ${theme.colors.background.primary};
      border: 1px solid ${theme.colors.border.medium};
      border-radius: ${theme.shape.borderRadius(1)};
      color: ${theme.colors.text.primary};
      font-size: ${theme.typography.size.xs};
      cursor: pointer;
      
      &:hover {
        background: ${theme.colors.background.secondary};
        border-color: ${theme.colors.border.strong};
      }
    `,
    error: css`
      color: ${theme.colors.error.main};
      font-size: ${theme.typography.size.sm};
      padding: ${theme.spacing(1, 2)};
      background: ${theme.colors.error.transparent};
      border-radius: ${theme.shape.borderRadius(1)};
      margin: ${theme.spacing(1, 2)};
    `,
    loading: css`
      display: flex;
      align-items: center;
      gap: ${theme.spacing(1)};
      color: ${theme.colors.text.secondary};
      font-size: ${theme.typography.size.sm};
      padding: ${theme.spacing(1, 2)};
    `,
    capabilities: css`
      padding: ${theme.spacing(1, 2)};
      background: ${theme.colors.background.secondary};
      border-top: 1px solid ${theme.colors.border.weak};
      font-size: ${theme.typography.size.xs};
      color: ${theme.colors.text.secondary};
    `,
  };

  return (
    <div className={styles.container}>
      {/* Header */}
      <div className={styles.header}>
        <span className={styles.headerIcon}>🤖</span>
        <span className={styles.headerTitle}>AI Assistant</span>
      </div>

      {/* Messages */}
      <div className={styles.messagesContainer}>
        {messages.length === 0 && (
          <div className={styles.assistantBubble}>
            <p>Hello! I'm your AI observability assistant. I can help you:</p>
            <ul>
              <li>Create dashboard panels with natural language</li>
              <li>Explain PromQL queries</li>
              <li>Detect and analyze anomalies</li>
              <li>Provide insights about your system</li>
            </ul>
            <p>Try asking me something like "Create a panel showing CPU usage" or "Check for anomalies in memory".</p>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`${styles.message} ${
              message.role === 'user' ? styles.userMessage : styles.assistantMessage
            }`}
          >
            <div
              className={`${styles.messageBubble} ${
                message.role === 'user' ? styles.userBubble : styles.assistantBubble
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className={styles.loading}>
            <span>🤔</span>
            <span>Thinking...</span>
          </div>
        )}

        {error && <div className={styles.error}>Error: {error}</div>}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      {quickActions.length > 0 && (
        <div className={styles.quickActions}>
          {quickActions.map((action, index) => (
            <button
              key={index}
              className={styles.quickActionButton}
              onClick={action.action}
              disabled={isLoading}
            >
              {action.label}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className={styles.inputContainer}>
        <form onSubmit={handleSubmit} className={styles.inputForm}>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything about your observability..."
            className={styles.input}
            disabled={isLoading}
          />
          <button
            type="submit"
            className={styles.sendButton}
            disabled={isLoading || !input.trim()}
          >
            Send
          </button>
        </form>
      </div>

      {/* Capabilities Info */}
      {capabilities && (
        <div className={styles.capabilities}>
          Connected to AI service • {capabilities.supported_actions?.length || 0} actions available
        </div>
      )}
    </div>
  );
}; 