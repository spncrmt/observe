import React, { useState, useEffect } from 'react';
import { PanelProps } from '@grafana/data';
import { useTheme2 } from '@grafana/ui';
import { SimpleOptions } from 'types';

interface Props extends PanelProps<SimpleOptions> {}

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  action?: string;
  success?: boolean;
  timestamp: Date;
}

interface Context {
  dashboard_id?: string;
  dashboard_title?: string;
  panel_id?: string;
  current_query?: string;
}

export const AIAgentPanel: React.FC<Props> = ({ options, data, width, height }) => {
  const theme = useTheme2();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [context, setContext] = useState<Context>({});
  const [isConnected, setIsConnected] = useState(false);

  const AI_SERVICE_URL = 'http://localhost:5001';

  useEffect(() => {
    // Check AI service connection
    checkConnection();
    // Get initial context
    getContext();
  }, []);

  const checkConnection = async () => {
    try {
      const response = await fetch(`${AI_SERVICE_URL}/health`);
      if (response.ok) {
        setIsConnected(true);
        addMessage('🤖 AI Agent connected and ready!', false);
      } else {
        setIsConnected(false);
        addMessage('❌ AI Agent offline. Please check the service.', false, undefined, false);
      }
    } catch (error) {
      setIsConnected(false);
      addMessage('❌ Cannot connect to AI Agent. Is the service running?', false, undefined, false);
    }
  };

  const getContext = async () => {
    try {
      const response = await fetch(`${AI_SERVICE_URL}/ai/api/context`);
      const data = await response.json();
      if (data.success && data.data) {
        setContext(data.data);
        updateContextDisplay(data.data);
      }
    } catch (error) {
      console.error('Error getting context:', error);
    }
  };

  const updateContextDisplay = (ctx: Context) => {
    const contextInfo = `Dashboard: ${ctx.dashboard_title || 'None'} | Query: ${ctx.current_query || 'None'}`;
    // You could display this in the panel
  };

  const addMessage = (text: string, isUser: boolean, action?: string, success: boolean = true) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      isUser,
      action,
      success,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || !isConnected) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    addMessage(userMessage, true);
    setIsLoading(true);

    try {
      const response = await fetch(`${AI_SERVICE_URL}/ai/api/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: userMessage }),
      });

      const data = await response.json();
      
      addMessage(data.message || 'Sorry, I could not process your request.', false, data.action, data.success);
      
      if (data.data && data.context_updated) {
        setContext(data.data);
        updateContextDisplay(data.data);
      }
    } catch (error) {
      addMessage('❌ Error connecting to AI agent. Please check if the service is running.', false, undefined, false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const containerStyle: React.CSSProperties = {
    width,
    height,
    padding: theme.spacing(2),
    backgroundColor: theme.colors.background.primary,
    color: theme.colors.text.primary,
    display: 'flex',
    flexDirection: 'column',
  };

  const messagesContainerStyle: React.CSSProperties = {
    flex: 1,
    overflowY: 'auto',
    marginBottom: theme.spacing(2),
    padding: theme.spacing(1),
    backgroundColor: theme.colors.background.secondary,
    borderRadius: theme.shape.borderRadius(1),
  };

  const messageStyle = (isUser: boolean, success?: boolean): React.CSSProperties => ({
    marginBottom: theme.spacing(1),
    padding: theme.spacing(1),
    borderRadius: theme.shape.borderRadius(1),
    maxWidth: '80%',
    wordWrap: 'break-word',
    backgroundColor: isUser 
      ? theme.colors.primary.main 
      : success === false 
        ? theme.colors.error.main 
        : success === true 
          ? theme.colors.success.main 
          : theme.colors.background.secondary,
    color: isUser ? theme.colors.primary.contrastText : theme.colors.text.primary,
    marginLeft: isUser ? 'auto' : '0',
    textAlign: isUser ? 'right' : 'left',
  });

  const inputContainerStyle: React.CSSProperties = {
    display: 'flex',
    gap: theme.spacing(1),
  };

  const inputStyle: React.CSSProperties = {
    flex: 1,
    padding: theme.spacing(1),
    border: `1px solid ${theme.colors.border.weak}`,
    borderRadius: theme.shape.borderRadius(1),
    backgroundColor: theme.colors.background.secondary,
    color: theme.colors.text.primary,
  };

  const buttonStyle: React.CSSProperties = {
    padding: theme.spacing(1, 2),
    backgroundColor: theme.colors.primary.main,
    color: theme.colors.primary.contrastText,
    border: 'none',
    borderRadius: theme.shape.borderRadius(1),
    cursor: isConnected ? 'pointer' : 'not-allowed',
    opacity: isConnected ? 1 : 0.5,
  };

  const statusStyle: React.CSSProperties = {
    padding: theme.spacing(0.5, 1),
    borderRadius: theme.shape.borderRadius(1),
    fontSize: '12px',
    marginBottom: theme.spacing(1),
    textAlign: 'center',
    backgroundColor: isConnected ? theme.colors.success.main : theme.colors.error.main,
    color: isConnected ? theme.colors.success.contrastText : theme.colors.error.contrastText,
  };

  const actionBadgeStyle: React.CSSProperties = {
    display: 'inline-block',
    padding: '2px 6px',
    backgroundColor: theme.colors.primary.main,
    color: theme.colors.primary.contrastText,
    borderRadius: '10px',
    fontSize: '10px',
    marginLeft: '5px',
  };

  return (
    <div style={containerStyle}>
      <div style={statusStyle}>
        {isConnected ? '✅ AI Agent Online' : '❌ AI Agent Offline'}
      </div>
      
      <div style={messagesContainerStyle}>
        {messages.map((message) => (
          <div key={message.id} style={messageStyle(message.isUser, message.success)}>
            {message.text}
            {message.action && (
              <span style={actionBadgeStyle}>{message.action}</span>
            )}
          </div>
        ))}
        {isLoading && (
          <div style={messageStyle(false)}>
            🤔 Processing...
          </div>
        )}
      </div>
      
      <div style={inputContainerStyle}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={isConnected ? "Ask me anything about your system..." : "AI Agent offline"}
          disabled={!isConnected}
          style={inputStyle}
        />
        <button
          onClick={sendMessage}
          disabled={!isConnected || isLoading}
          style={buttonStyle}
        >
          Send
        </button>
      </div>
    </div>
  );
}; 