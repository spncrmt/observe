// AI Assistant Bookmarklet
// Copy this entire code and create a bookmark with it as the URL

javascript:(function(){
    // Check if AI chat is already injected
    if (document.getElementById('ai-assistant-container')) {
        return;
    }
    
    // Create AI chat container
    const aiContainer = document.createElement('div');
    aiContainer.id = 'ai-assistant-container';
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
    closeBtn.onclick = function() {
        aiContainer.style.right = '-400px';
        toggleBtn.style.right = '20px';
    };
    
    header.appendChild(title);
    header.appendChild(closeBtn);
    
    // Create iframe
    const iframe = document.createElement('iframe');
    iframe.src = 'https://ai-service.onrender.com/chat';
    iframe.style.cssText = `
        flex: 1;
        border: none;
        width: 100%;
    `;
    iframe.title = 'AI Assistant Chat';
    
    // Create toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.innerHTML = '🤖';
    toggleBtn.style.cssText = `
        position: fixed;
        top: 20px;
        right: -60px;
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
    `;
    toggleBtn.onclick = function() {
        if (aiContainer.style.right === '0px') {
            aiContainer.style.right = '-400px';
            toggleBtn.style.right = '20px';
        } else {
            aiContainer.style.right = '0px';
            toggleBtn.style.right = '420px';
        }
    };
    
    // Add elements to page
    aiContainer.appendChild(header);
    aiContainer.appendChild(iframe);
    document.body.appendChild(aiContainer);
    document.body.appendChild(toggleBtn);
    
    // Show the chat
    setTimeout(() => {
        aiContainer.style.right = '0px';
        toggleBtn.style.right = '420px';
    }, 100);
    
    // Keyboard shortcut (Ctrl/Cmd + K)
    document.addEventListener('keydown', function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            toggleBtn.click();
        }
    });
    
    console.log('🤖 AI Assistant injected! Press Ctrl+K to toggle.');
})(); 