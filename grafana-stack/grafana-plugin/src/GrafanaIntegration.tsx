import React, { useState, useEffect } from 'react';
import { AISidebarPanel } from './AISidebarPanel';
import { useTheme2 } from '@grafana/ui';

export const GrafanaIntegration: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const theme = useTheme2();

  // Automatically inject the AI sidebar into Grafana's interface
  useEffect(() => {
    const injectAISidebar = () => {
      // Check if already injected
      if (document.getElementById('ai-sidebar-container')) {
        return;
      }

      // Create container for AI sidebar
      const aiContainer = document.createElement('div');
      aiContainer.id = 'ai-sidebar-container';
      aiContainer.style.cssText = `
        position: fixed;
        top: 0;
        right: -400px;
        width: 400px;
        height: 100vh;
        background: #1e1e1e;
        border-left: 1px solid #404040;
        box-shadow: -4px 0 12px rgba(0, 0, 0, 0.3);
        z-index: 9999;
        transition: right 0.3s ease;
        display: flex;
        flex-direction: column;
      `;

      // Create toggle button
      const toggleButton = document.createElement('button');
      toggleButton.id = 'ai-toggle-button';
      toggleButton.innerHTML = '🤖';
      toggleButton.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        background: #0066cc;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 16px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 8px;
      `;

      // Create header
      const header = document.createElement('div');
      header.style.cssText = `
        background: #2d2d2d;
        padding: 16px 20px;
        border-bottom: 1px solid #404040;
        display: flex;
        align-items: center;
        justify-content: space-between;
      `;

      const title = document.createElement('div');
      title.style.cssText = `
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
      `;
      title.innerHTML = '🤖 AI Assistant';

      const closeBtn = document.createElement('button');
      closeBtn.innerHTML = '✕';
      closeBtn.style.cssText = `
        background: none;
        border: none;
        color: #b0b0b0;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        font-size: 18px;
      `;

      // Create iframe for AI chat
      const iframe = document.createElement('iframe');
      iframe.src = 'https://ai-service.onrender.com/chat';
      iframe.style.cssText = `
        flex: 1;
        border: none;
        width: 100%;
      `;
      iframe.title = 'AI Assistant Chat';

      // Add event listeners
      toggleButton.onclick = function() {
        const container = document.getElementById('ai-sidebar-container');
        if (container) {
          const isVisible = container.style.right === '0px';
          container.style.right = isVisible ? '-400px' : '0px';
          toggleButton.style.right = isVisible ? '20px' : '420px';
        }
      };

      closeBtn.onclick = function() {
        const container = document.getElementById('ai-sidebar-container');
        if (container) {
          container.style.right = '-400px';
          toggleButton.style.right = '20px';
        }
      };

      // Assemble the components
      header.appendChild(title);
      header.appendChild(closeBtn);
      aiContainer.appendChild(header);
      aiContainer.appendChild(iframe);

      // Add to page
      document.body.appendChild(aiContainer);
      document.body.appendChild(toggleButton);

      // Keyboard shortcut (Ctrl/Cmd + K)
      document.addEventListener('keydown', function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
          event.preventDefault();
          toggleButton.click();
        }
      });

      console.log('🤖 AI Assistant automatically injected! Press Ctrl+K to toggle.');
    };

    // Wait for Grafana to be fully loaded
    const timer = setTimeout(injectAISidebar, 2000);
    
    return () => {
      clearTimeout(timer);
      const container = document.getElementById('ai-sidebar-container');
      const button = document.getElementById('ai-toggle-button');
      if (container) container.remove();
      if (button) button.remove();
    };
  }, []);

  return null; // This component doesn't render anything visible
}; 