import React from 'react';
import { App } from './App';
import { AppRootProps } from '@grafana/data';

export const AIChatPage: React.FC<AppRootProps> = (props) => {
  return <App {...props} />;
}; 