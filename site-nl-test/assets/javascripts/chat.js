(function () {
  'use strict';
  console.log('FreeLLM Chat Widget: Initializing...');

  // Chat widget state
  let isOpen = false;
  let messages = [];

  // Create chat button
  function createChatButton() {
    const btn = document.createElement('button');
    btn.id = 'chat-toggle-btn';
    btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>';
    btn.style.position = 'fixed';
    btn.style.bottom = '24px';
    btn.style.right = '24px';
    btn.style.width = '56px';
    btn.style.height = '56px';
    btn.style.borderRadius = '50%';
    btn.style.backgroundColor = '#6366f1';
    btn.style.color = 'white';
    btn.style.border = 'none';
    btn.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
    btn.style.cursor = 'pointer';
    btn.style.zIndex = '1000';
    btn.style.display = 'flex';
    btn.style.alignItems = 'center';
    btn.style.justifyContent = 'center';
    btn.style.transition = 'all 0.3s ease';
    btn.onmouseover = () => {
      btn.style.transform = 'scale(1.05)';
      btn.style.backgroundColor = '#4f46e5';
    };
    btn.onmouseout = () => {
      btn.style.transform = 'scale(1)';
      btn.style.backgroundColor = '#6366f1';
    };
    btn.onclick = toggleChat;
    document.body.appendChild(btn);
  }

  // Create chat widget
  function createChatWidget() {
    const widget = document.createElement('div');
    widget.id = 'chat-widget';
    widget.style.position = 'fixed';
    widget.style.bottom = '90px';
    widget.style.right = '24px';
    widget.style.width = '350px';
    widget.style.height = '500px';
    widget.style.backgroundColor = 'white';
    widget.style.borderRadius = '16px';
    widget.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)';
    widget.style.display = 'flex';
    widget.style.flexDirection = 'column';
    widget.style.zIndex = '1000';
    widget.style.border = '1px solid #e5e7eb';
    widget.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    widget.style.opacity = '0';
    widget.style.transform = 'translateY(20px)';
    widget.style.pointerEvents = 'none';

    // Chat header
    const header = document.createElement('div');
    header.style.padding = '16px';
    header.style.borderBottom = '1px solid #f3f4f6';
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';
    header.style.backgroundColor = '#f8fafc';
    
    const title = document.createElement('h3');
    title.textContent = 'Chat with AI';
    title.style.margin = '0';
    title.style.fontSize = '1.25rem';
    title.style.fontWeight = '600';
    title.style.color = '#1f2937';
    
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18"></path><path d="m6 6 12 12"></path></svg>';
    closeBtn.style.background = 'none';
    closeBtn.style.border = 'none';
    closeBtn.style.color = '#6b7280';
    closeBtn.style.fontSize = '1.25rem';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.padding = '4px';
    closeBtn.style.borderRadius = '50%';
    closeBtn.style.width = '36px';
    closeBtn.height = '36px';
    closeBtn.style.display = 'flex';
    closeBtn.style.alignItems = 'center';
    closeBtn.style.justifyContent = 'center';
    closeBtn.onmouseover = () => {
      closeBtn.style.backgroundColor = '#f3f4f6';
    };
    closeBtn.onmouseout = () => {
      closeBtn.style.color = '#6b7280';
    };
    closeBtn.onclick = () => {
      closeChat();
    };
    header.appendChild(title);
    header.appendChild(closeBtn);
    widget.appendChild(header);

    // Chat messages container
    const messagesContainer = document.createElement('div');
    messagesContainer.id = 'chat-messages';
    messagesContainer.style.flex = '1';
    messagesContainer.style.overflowY = 'auto';
    messagesContainer.style.padding = '16px';
    messagesContainer.style.display = 'flex';
    messagesContainer.style.flexDirection = 'column';
    messagesContainer.style.gap = '12px';
    widget.appendChild(messagesContainer);

    // Chat input
    const inputContainer = document.createElement('div');
    inputContainer.style.padding = '16px';
    inputContainer.style.borderTop = '1px solid #f3f4f6';
    inputContainer.style.display = 'flex';
    inputContainer.style.gap = '12px';
    inputContainer.style.backgroundColor = '#f8fafc';
    
    const input = document.createElement('input');
    input.id = 'chat-input';
    input.type = 'text';
    input.placeholder = 'Ask me anything...';
    input.style.flex = '1';
    input.style.padding = '12px 16px';
    input.style.border = '1px solid #e5e7eb';
    input.style.borderRadius = '12px';
    input.style.fontSize = '1rem';
    input.style.outline = 'none';
    input.style.transition = 'border-color 0.2s ease';
    input.onfocus = () => {
      input.style.borderColor = '#6366f1';
    };
    input.onblur = () => {
      input.style.borderColor = '#e5e7eb';
    };
    input.onkeypress = (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    };
    
    const sendBtn = document.createElement('button');
    sendBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.5 19.5 0 0 1 6 6 19.79 19.79 0 0 1 3.07 8.67A2 2 0 0 1 21.18 22v-3a2.82 2.82 0 0 0 .82-2.12l-3-4a2.82 2.82 0 0 0-1.06-2.82 2.82 0 0 0-2.82-1.06l-4-3A2.82 2.82 0 0 0 2 4.11v3a2.82 2.82 0 0 0-1.18 2.12A11.79 11.79 0 0 0 5 12c0 1.35.28 2.65.75 3.82l4 4a2.82 2.82 0 0 0 2.82 1.06l4-3A2.82 2.82 0 0 0 16.07 8h3a2.82 2.82 0 0 0 2.12-.82z"></path></svg>';
    sendBtn.style.backgroundColor = '#6366f1';
    sendBtn.style.color = 'white';
    sendBtn.style.border = 'none';
    sendBtn.style.borderRadius = '50%';
    sendBtn.style.width = '40px';
    sendBtn.style.height = '40px';
    sendBtn.style.cursor = 'pointer';
    sendBtn.style.display = 'flex';
    sendBtn.style.alignItems = 'center';
    sendBtn.style.justifyContent = 'center';
    sendBtn.style.boxShadow = '0 2px 4px -1px rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.06)';
    sendBtn.onmouseover = () => {
      sendBtn.style.backgroundColor = '#4f46e5';
    };
    sendBtn.onmouseout = () => {
      sendBtn.style.backgroundColor = '#6366f1';
    };
    sendBtn.onclick = sendMessage;
    
    inputContainer.appendChild(input);
    inputContainer.appendChild(sendBtn);
    widget.appendChild(inputContainer);
    
    document.body.appendChild(widget);
  }

  function toggleChat() {
    isOpen = !isOpen;
    const widget = document.getElementById('chat-widget');
    if (isOpen) {
      widget.style.opacity = '1';
      widget.style.transform = 'translateY(0)';
      widget.style.pointerEvents = 'all';
      document.getElementById('chat-input').focus();
    } else {
      widget.style.opacity = '0';
      widget.style.transform = 'translateY(20px)';
      widget.style.pointerEvents = 'none';
    }
  }

  function closeChat() {
    isOpen = false;
    const widget = document.getElementById('chat-widget');
    widget.style.opacity = '0';
    widget.style.transform = 'translateY(20px)';
    widget.style.pointerEvents = 'none';
  }

  function addMessage(content, isUser = false) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.display = 'flex';
    messageDiv.style.flexDirection = isUser ? 'row-reverse' : 'row';
    messageDiv.style.alignItems = 'flex-start';
    messageDiv.style.maxWidth = '80%';
    
    const avatar = document.createElement('div');
    avatar.style.width = '32px';
    avatar.style.height = '32px';
    avatar.style.borderRadius = '50%';
    avatar.style.display = 'flex';
    avatar.style.alignItems = 'center';
    avatar.style.justifyContent = 'center';
    avatar.style.fontSize = '0.875rem';
    avatar.style.fontWeight = '600';
    avatar.style.color = 'white';
    avatar.style.margin = isUser ? '0 0 0 8px' : '0 8px 0 0';
    
    if (isUser) {
      avatar.style.backgroundColor = '#6366f1';
      avatar.textContent = 'U';
      messageDiv.style.marginLeft = 'auto';
    } else {
      avatar.style.backgroundColor = '#f3f4f6';
      avatar.textContent = 'AI';
      avatar.style.color = '#6b7280';
      messageDiv.style.marginRight = 'auto';
    }
    
    const messageContent = document.createElement('div');
    messageContent.style.padding = '12px 16px';
    messageContent.style.borderRadius = isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px';
    messageContent.style.backgroundColor = isUser ? '#6366f1' : '#f3f4f6';
    messageContent.style.color = isUser ? 'white' : '#1f2937';
    messageContent.style.lineHeight = '1.5';
    messageContent.style.fontSize = '0.95rem';
    messageContent.style.wordWrap = 'break-word';
    messageContent.style.maxWidth = '100%';
    
    // Handle markdown-like formatting (simple)
    messageContent.textContent = content;
    
    messageDiv.appendChild(isUser ? messageContent : avatar);
    messageDiv.appendChild(!isUser ? messageContent : avatar);
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    // Add user message
    addMessage(message, true);
    input.value = '';
    
    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.style.display = 'flex';
    typingDiv.style.alignItems = 'center';
    typingDiv.style.maxWidth = '80%';
    typingDiv.style.marginLeft = 'auto';
    
    const typingAvatar = document.createElement('div');
    typingAvatar.style.width = '32px';
    typingAvatar.style.height = '32px';
    typingAvatar.style.borderRadius = '50%';
    typingAvatar.style.backgroundColor = '#f3f4f6';
    typingAvatar.style.display = 'flex';
    typingAvatar.style.alignItems = 'center';
    typingAvatar.style.justifyContent = 'center';
    typingAvatar.style.fontSize = '0.875rem';
    typingAvatar.style.fontWeight = '600';
    typingAvatar.style.color = '#6b7280';
    typingAvatar.textContent = 'AI';
    
    const typingContent = document.createElement('div');
    typingContent.style.padding = '12px 16px';
    typingContent.style.borderRadius = '16px 16px 16px 4px';
    typingContent.style.backgroundColor = '#f3f4f6';
    typingContent.style.color = '#1f2937';
    typingContent.style.lineHeight = '1.5';
    typingContent.style.fontSize = '0.95rem';
    
    const typingDots = document.createElement('span');
    typingDots.id = 'typing-dots';
    typingDots.style.display = 'inline-block';
    typingDots.innerHTML = '<span>.</span><span>.</span><span>.</span>';
    typingDots.style.animation = 'typing 1.5s infinite';
    
    typingContent.appendChild(typingDots);
    
    typingDiv.appendChild(typingAvatar);
    typingDiv.appendChild(typingContent);
    
    document.getElementById('chat-messages').appendChild(typingDiv);
    document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
    
    try {
      // Call RAG API
      const response = await fetch('https://rag.aldof.duckdns.org/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': '{{RAG_API_KEY}}' // Placeholder for build-time replacement
        },
        body: JSON.stringify({
          question: message,
          k: 3
        })
      });
      
      const data = await response.json();
      
      // Remove typing indicator
      if (typingDiv) {
        typingDiv.remove();
      }
      
      if (data && data.answer) {
        // Optionally, log sources and confidence for debugging
        console.log('RAG response:', data);
        addMessage(data.answer, false);
        // If we want to show sources, we could do it here, but the UI doesn't have a place for them yet.
        // For now, we just log them.
        if (data.sources) {
          console.log('Sources:', data.sources);
        }
      } else {
        addMessage('Sorry, I encountered an error. Please try again.', false);
      }
    } catch (error) {
      // Remove typing indicator
      if (typingDiv) {
        typingDiv.remove();
      }
      
      addMessage('Sorry, I encountered an error. Please check your connection and try again.', false);
      console.error('Chat error:', error);
    }
  }

  // Initialize
  document.addEventListener('DOMContentLoaded', function() {
    createChatButton();
    createChatWidget();
  });
});