import { AppPlugin } from '@grafana/data';
import { App } from './App';
import { AIAssistantPage } from './AIAssistantPage';
import { AIChatPage } from './AIChatPage';

export const plugin = new AppPlugin()
  .setRootPage(App)
  .addConfigPage({
    title: 'AI Assistant',
    body: AIAssistantPage,
    id: 'ai-assistant',
  })
  .addPage({
    title: 'AI Chat',
    body: AIChatPage,
    path: '/ai-chat',
  }); 