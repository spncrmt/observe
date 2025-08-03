import React, { useState, useEffect } from 'react';
import { AISidebarPanel } from './AISidebarPanel';
import { useTheme2 } from '@grafana/ui';

export const GrafanaIntegration: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const theme = useTheme2();

  // Inject the AI sidebar into Grafana's interface
  useEffect(() => {
    const injectAISidebar = () => {
      // Create a container for the AI sidebar
      const aiContainer = document.createElement('div');
      aiContainer.id = 'ai-sidebar-container';
      document.body.appendChild(aiContainer);

      // Create React root and render the AI sidebar
      const { createRoot } = require('react-dom/client');
      const root = createRoot(aiContainer);
      
      const AISidebarWrapper = () => {
        const [sidebarOpen, setSidebarOpen] = useState(false);
        
        return (
          <AISidebarPanel
            theme={theme}
            isOpen={sidebarOpen}
            onToggle={() => setSidebarOpen(!sidebarOpen)}
          />
        );
      };
      
      root.render(<AISidebarWrapper />);
    };

    // Wait for Grafana to be fully loaded
    const timer = setTimeout(injectAISidebar, 1000);
    
    return () => {
      clearTimeout(timer);
      const container = document.getElementById('ai-sidebar-container');
      if (container) {
        container.remove();
      }
    };
  }, [theme]);

  return null; // This component doesn't render anything visible
}; 