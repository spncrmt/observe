import { PanelPlugin } from '@grafana/data';
import { AIAssistantPanel } from './AIAssistantPanel';
import { AIAssistantOptions } from './types';

export const plugin = new PanelPlugin<AIAssistantOptions>(AIAssistantPanel).setPanelOptions((builder) => {
  return builder
    .addTextInput({
      path: 'aiServiceUrl',
      name: 'AI Service URL',
      description: 'URL of the AI service endpoint',
      defaultValue: 'http://localhost:5001',
    })
    .addBooleanSwitch({
      path: 'enableContextAwareness',
      name: 'Enable Context Awareness',
      description: 'Allow AI to access dashboard context',
      defaultValue: true,
    })
    .addSelect({
      path: 'defaultModel',
      name: 'Default AI Model',
      description: 'Default AI model to use',
      defaultValue: 'gpt-4',
      options: [
        { value: 'gpt-4', label: 'GPT-4' },
        { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
        { value: 'claude-3', label: 'Claude-3' },
      ],
    });
}); 