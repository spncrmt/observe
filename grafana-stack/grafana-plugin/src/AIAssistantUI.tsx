import React, { useState, useRef, useEffect } from 'react';
import { GrafanaTheme2, Button, Icon, TextArea, LoadingPlaceholder } from '@grafana/ui';
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

interface AIAssistantUIProps {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  onSendMessage: (input: string) => void;
  quickActions: QuickAction[];
  capabilities: any;
  theme: GrafanaTheme2;
  onExecuteQuery?: (query: string) => void;
  onCreatePanel?: (config: any) => void;
}

export const AIAssistantUI: React.FC<AIAssistantUIProps> = ({
  messages,
  isLoading,
  error,
  onSendMessage,
  quickActions,
  capabilities,
  theme,
  onExecuteQuery,
  onCreatePanel,
}) => {
  const [input, setInput] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

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

  const renderMessage = (message: Message) => {
    const isUser = message.role === 'user';
    
    return (
      <div
        key={message.timestamp.getTime()}
        className={`${styles.message} ${isUser ? styles.userMessage : styles.assistantMessage}`}
      >
        <div className={`${styles.messageBubble} ${isUser ? styles.userBubble : styles.assistantBubble}`}>
          {message.type === 'query' && (
            <div className={styles.queryBlock}>
              <div className={styles.queryHeader}>
                <Icon name="database" size="sm" />
                <span>PromQL Query</span>
              </div>
              <code className={styles.queryCode}>{message.content}</code>
              {message.data && (
                <div className={styles.queryResult}>
                  <pre>{JSON.stringify(message.data, null, 2)}</pre>
                </div>
              )}
            </div>
          )}
          {message.type === 'chart' && (
            <div className={styles.chartBlock}>
              <div className={styles.chartHeader}>
                <Icon name="chart-line" size="sm" />
                <span>Chart Generated</span>
              </div>
              <div className={styles.chartPlaceholder}>
                Chart visualization would appear here
              </div>
            </div>
          )}
          {message.type === 'insight' && (
            <div className={styles.insightBlock}>
              <div className={styles.insightHeader}>
                <Icon name="lightbulb" size="sm" />
                <span>AI Insight</span>
              </div>
              <div className={styles.insightContent}>{message.content}</div>
            </div>
          )}
          {(!message.type || message.type === 'text') && (
            <div className={styles.textContent}>{message.content}</div>
          )}
          <div className={styles.messageTime}>
            {message.timestamp.toLocaleTimeString()}
          </div>
        </div>
      </div>
    );
  };

  const styles = {
    container: css`
      display: flex;
      flex-direction: column;
      height: 100%;
      background: ${theme.colors.background.primary};
      border-radius: ${theme.shape.borderRadius(1)};
      overflow: hidden;
      border: 1px solid ${theme.colors.border.weak};
    `,
    header: css`
      padding: ${theme.spacing(1, 2)};
      background: ${theme.colors.background.secondary};
      border-bottom: 1px solid ${theme.colors.border.weak};
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: ${theme.spacing(1)};
    `,
    headerLeft: css`
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
    expandButton: css`
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
    messagesContainer: css`
      flex: 1;
      overflow-y: auto;
      padding: ${theme.spacing(1)};
      display: flex;
      flex-direction: column;
      gap: ${theme.spacing(1)};
      min-height: 200px;
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
      padding: ${theme.spacing(1, 1.5)};
      border-radius: ${theme.shape.borderRadius(2)};
      position: relative;
    `,
    userBubble: css`
      background: ${theme.colors.primary.main};
      color: ${theme.colors.primary.contrastText};
    `,
    assistantBubble: css`
      background: ${theme.colors.background.secondary};
      border: 1px solid ${theme.colors.border.weak};
      color: ${theme.colors.text.primary};
    `,
    textContent: css`
      line-height: 1.4;
      white-space: pre-wrap;
    `,
    messageTime: css`
      font-size: ${theme.typography.size.xs};
      opacity: 0.7;
      margin-top: ${theme.spacing(0.5)};
    `,
    queryBlock: css`
      border: 1px solid ${theme.colors.border.medium};
      border-radius: ${theme.shape.borderRadius(1)};
      overflow: hidden;
    `,
    queryHeader: css`
      background: ${theme.colors.background.secondary};
      padding: ${theme.spacing(0.5, 1)};
      display: flex;
      align-items: center;
      gap: ${theme.spacing(0.5)};
      font-size: ${theme.typography.size.sm};
      font-weight: ${theme.typography.fontWeightMedium};
      color: ${theme.colors.text.secondary};
    `,
    queryCode: css`
      background: ${theme.colors.background.primary};
      padding: ${theme.spacing(1)};
      display: block;
      font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
      font-size: ${theme.typography.size.sm};
      color: ${theme.colors.text.primary};
      border-top: 1px solid ${theme.colors.border.weak};
    `,
    queryResult: css`
      background: ${theme.colors.background.primary};
      padding: ${theme.spacing(1)};
      border-top: 1px solid ${theme.colors.border.weak};
      max-height: 200px;
      overflow-y: auto;
      pre {
        margin: 0;
        font-size: ${theme.typography.size.xs};
        color: ${theme.colors.text.secondary};
      }
    `,
    chartBlock: css`
      border: 1px solid ${theme.colors.border.medium};
      border-radius: ${theme.shape.borderRadius(1)};
      overflow: hidden;
    `,
    chartHeader: css`
      background: ${theme.colors.background.secondary};
      padding: ${theme.spacing(0.5, 1)};
      display: flex;
      align-items: center;
      gap: ${theme.spacing(0.5)};
      font-size: ${theme.typography.size.sm};
      font-weight: ${theme.typography.fontWeightMedium};
      color: ${theme.colors.text.secondary};
    `,
    chartPlaceholder: css`
      padding: ${theme.spacing(2)};
      text-align: center;
      color: ${theme.colors.text.secondary};
      background: ${theme.colors.background.primary};
      border-top: 1px solid ${theme.colors.border.weak};
    `,
    insightBlock: css`
      border: 1px solid ${theme.colors.success.border};
      border-radius: ${theme.shape.borderRadius(1)};
      overflow: hidden;
    `,
    insightHeader: css`
      background: ${theme.colors.success.transparent};
      padding: ${theme.spacing(0.5, 1)};
      display: flex;
      align-items: center;
      gap: ${theme.spacing(0.5)};
      font-size: ${theme.typography.size.sm};
      font-weight: ${theme.typography.fontWeightMedium};
      color: ${theme.colors.success.text};
    `,
    insightContent: css`
      padding: ${theme.spacing(1)};
      background: ${theme.colors.background.primary};
      border-top: 1px solid ${theme.colors.success.border};
      line-height: 1.4;
    `,
    inputContainer: css`
      padding: ${theme.spacing(1)};
      border-top: 1px solid ${theme.colors.border.weak};
      background: ${theme.colors.background.primary};
    `,
    inputForm: css`
      display: flex;
      gap: ${theme.spacing(1)};
      align-items: flex-end;
    `,
    inputField: css`
      flex: 1;
      resize: none;
      min-height: 36px;
      max-height: 120px;
      font-family: inherit;
    `,
    sendButton: css`
      min-width: 36px;
      height: 36px;
    `,
    quickActions: css`
      display: flex;
      gap: ${theme.spacing(0.5)};
      padding: ${theme.spacing(0.5, 1)};
      border-bottom: 1px solid ${theme.colors.border.weak};
      background: ${theme.colors.background.secondary};
      overflow-x: auto;
    `,
    quickActionButton: css`
      white-space: nowrap;
      font-size: ${theme.typography.size.xs};
      padding: ${theme.spacing(0.5, 1)};
      height: auto;
    `,
    errorMessage: css`
      color: ${theme.colors.error.text};
      background: ${theme.colors.error.transparent};
      padding: ${theme.spacing(1)};
      border-radius: ${theme.shape.borderRadius(1)};
      margin: ${theme.spacing(1)};
      font-size: ${theme.typography.size.sm};
    `,
    loadingContainer: css`
      display: flex;
      align-items: center;
      justify-content: center;
      padding: ${theme.spacing(2)};
    `,
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <Icon name="robot" className={styles.headerIcon} />
          <span className={styles.headerTitle}>AI Assistant</span>
        </div>
        <button
          className={styles.expandButton}
          onClick={() => setIsExpanded(!isExpanded)}
          title={isExpanded ? 'Collapse' : 'Expand'}
        >
          <Icon name={isExpanded ? 'angle-up' : 'angle-down'} />
        </button>
      </div>

      {quickActions.length > 0 && (
        <div className={styles.quickActions}>
          {quickActions.map((action, index) => (
            <Button
              key={index}
              variant="secondary"
              size="sm"
              onClick={action.action}
              className={styles.quickActionButton}
              icon={action.icon as any}
            >
              {action.label}
            </Button>
          ))}
        </div>
      )}

      <div className={styles.messagesContainer}>
        {messages.length === 0 && !isLoading && (
          <div style={{ textAlign: 'center', color: theme.colors.text.secondary, padding: theme.spacing(2) }}>
            <Icon name="robot" size="lg" style={{ marginBottom: theme.spacing(1) }} />
            <div>Ask me about your metrics, create dashboards, or analyze anomalies!</div>
          </div>
        )}
        
        {messages.map(renderMessage)}
        
        {isLoading && (
          <div className={styles.loadingContainer}>
            <LoadingPlaceholder text="AI is thinking..." />
          </div>
        )}
        
        {error && (
          <div className={styles.errorMessage}>
            <Icon name="exclamation-triangle" /> {error}
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.inputContainer}>
        <form onSubmit={handleSubmit} className={styles.inputForm}>
          <TextArea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.currentTarget.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about your metrics, create dashboards, or analyze data..."
            className={styles.inputField}
            disabled={isLoading}
            rows={1}
          />
          <Button
            type="submit"
            disabled={!input.trim() || isLoading}
            className={styles.sendButton}
            icon="paper-plane"
          />
        </form>
      </div>
    </div>
  );
}; 