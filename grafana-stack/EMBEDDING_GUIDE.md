# 🎯 AI Chat Embedding Guide

This guide shows you **5 different ways** to embed the AI chat interface into Grafana, from simple to advanced.

## 🚀 **Method 1: Direct URL Access (Easiest)**

**Simply visit the AI chat directly:**
```
https://ai-service.onrender.com/chat
```

**Or from your domain:**
```
https://awtospx.com/chat
```

✅ **Pros:** No setup required, works immediately
❌ **Cons:** Separate from Grafana interface

---

## 🎯 **Method 2: Dashboard Panel (Recommended)**

**Import the AI chat as a dashboard panel:**

### **Step 1: Import Dashboard**
1. Go to Grafana → Dashboards → Import
2. Upload the `embed-ai-panel.json` file
3. The AI chat will appear as a panel

### **Step 2: Manual Panel Creation**
1. Create a new dashboard
2. Add a **Text** panel
3. Set panel mode to **HTML**
4. Add this code:
```html
<iframe 
    src="https://ai-service.onrender.com/chat" 
    style="width: 100%; height: 600px; border: none; border-radius: 8px;"
></iframe>
```

✅ **Pros:** Integrated into dashboard, can resize
❌ **Cons:** Limited to dashboard view

---

## 🎨 **Method 3: Floating Chat (Cursor-style)**

**Add a floating AI chat that appears on every page:**

### **Step 1: Browser Bookmarklet**
1. Create a new bookmark in your browser
2. Name it "🤖 AI Assistant"
3. Set the URL to the content of `ai-bookmarklet.js`
4. Click the bookmark on any Grafana page

### **Step 2: Manual Injection**
Add this to your browser console:
```javascript
// Copy the entire content of ai-bookmarklet.js
// Paste and run in browser console
```

### **Step 3: Keyboard Shortcut**
- Press `Ctrl+K` (or `Cmd+K` on Mac) to toggle the AI chat

✅ **Pros:** Always accessible, keyboard shortcuts
❌ **Cons:** Requires manual activation

---

## 🔧 **Method 4: Custom Navigation**

**Add AI Assistant to Grafana's navigation:**

### **Step 1: Custom HTML Page**
1. Create a custom HTML page with the AI chat
2. Use the `grafana-custom-nav.html` as a template
3. Host it on your server

### **Step 2: Add to Grafana**
1. Go to Grafana → Configuration → Plugins
2. Add a custom plugin or use iframe embedding
3. Link to your AI chat page

✅ **Pros:** Permanent integration
❌ **Cons:** Requires server setup

---

## 🎯 **Method 5: Browser Extension (Advanced)**

**Create a browser extension for permanent integration:**

### **manifest.json**
```json
{
  "manifest_version": 3,
  "name": "Grafana AI Assistant",
  "version": "1.0",
  "description": "AI Assistant for Grafana",
  "permissions": ["activeTab"],
  "content_scripts": [
    {
      "matches": ["*://*.grafana.com/*", "*://awtospx.com/*"],
      "js": ["content.js"],
      "css": ["styles.css"]
    }
  ],
  "action": {
    "default_title": "🤖 AI Assistant"
  }
}
```

### **content.js**
```javascript
// Inject AI chat when extension is clicked
chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['ai-inject.js']
  });
});
```

✅ **Pros:** Permanent, automatic integration
❌ **Cons:** Requires extension development

---

## 🎨 **Customization Options**

### **Styling the Chat**
```css
/* Custom colors */
.ai-chat {
  --primary-color: #0066cc;
  --background-color: #1e1e1e;
  --text-color: #ffffff;
}

/* Custom size */
.ai-chat {
  width: 500px;  /* Default: 400px */
  height: 80vh;  /* Default: 100vh */
}
```

### **Positioning**
```css
/* Top-right (default) */
.ai-chat {
  top: 0;
  right: 0;
}

/* Bottom-right */
.ai-chat {
  bottom: 0;
  right: 0;
}

/* Center overlay */
.ai-chat {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

---

## 🚀 **Quick Start - Choose Your Method**

### **For Immediate Use:**
1. **Method 1** - Visit `https://ai-service.onrender.com/chat`

### **For Dashboard Integration:**
1. **Method 2** - Import the dashboard JSON file

### **For Cursor-like Experience:**
1. **Method 3** - Use the bookmarklet

### **For Permanent Integration:**
1. **Method 4** - Custom navigation setup

---

## 🎯 **Recommended Workflow**

1. **Start with Method 1** - Test the AI chat directly
2. **Add Method 2** - Embed in your main dashboard
3. **Use Method 3** - Bookmarklet for quick access
4. **Consider Method 4** - For production deployment

---

## 🔧 **Troubleshooting**

### **Chat Not Loading:**
- Check if AI service is running: `https://ai-service.onrender.com/health`
- Verify CORS settings
- Check browser console for errors

### **Styling Issues:**
- Ensure iframe has proper dimensions
- Check for CSS conflicts
- Verify dark theme compatibility

### **Integration Problems:**
- Test with different browsers
- Check Grafana version compatibility
- Verify HTTPS requirements

---

## 🎉 **Result**

You now have **multiple ways** to access your AI assistant:

1. **Direct URL** - Quick access
2. **Dashboard Panel** - Integrated monitoring
3. **Floating Chat** - Always available
4. **Custom Navigation** - Professional setup
5. **Browser Extension** - Permanent integration

Choose the method that works best for your workflow! 🚀 