(function () {
  'use strict';
  console.log('FreeLLM Chat Widget: Initializing...');

  // Detect language from browser preference or URL fallback
  const browserLang = navigator.language || navigator.userLanguage;
  const isNL = browserLang.startsWith('nl') || window.location.pathname.startsWith('/nl/');
  const chatTitle = isNL ? 'AIdo — je OKF assistent' : 'AIdo — your OKF assistant';
  const chatPlaceholder = isNL ? 'Vraag me iets...' : 'Ask me anything...';

  // Chat widget state
  let isOpen = false;
  let messages = [];

  // Create chat button
  function createChatButton() {
    const btn = document.createElement('button');
    btn.id = 'chat-toggle-btn';
    btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>';
    btn.style.position = 'fixed';
    btn.style.bottom = '24px';
    btn.style.right = '24px';
    btn.style.width = '56px';
    btn.style.height = '56px';
    btn.style.borderRadius = '50%';
    btn.style.backgroundColor = 'var(--md-primary-fg-color, #6366f1)';
    btn.style.color = 'white';
    btn.style.border = 'none';
    btn.style.boxShadow = 'var(--md-shadow-z2, 0 4px 6px -1px rgba(0,0,0,0.1))';
    btn.style.cursor = 'pointer';
    btn.style.zIndex = '1000';
    btn.style.display = 'flex';
    btn.style.alignItems = 'center';
    btn.style.justifyContent = 'center';
    btn.style.transition = 'all 0.3s ease';
    btn.onmouseover = () => {
      btn.style.transform = 'scale(1.05)';
      btn.style.backgroundColor = 'var(--md-accent-fg-color, #4f46e5)';
    };
    btn.onmouseout = () => {
      btn.style.transform = 'scale(1)';
      btn.style.backgroundColor = 'var(--md-primary-fg-color, #6366f1)';
    };
    btn.onclick = toggleChat;
    document.body.appendChild(btn);
  }

  // Create chat widget
  function createChatWidget() {
    const widget = document.createElement('div');
    widget.id = 'chat-widget';
    widget.style.position = 'fixed';
    widget.style.bottom = '5vh';
    widget.style.right = '2.5vw';
    widget.style.width = '95vw';
    widget.style.height = '90vh';
    widget.style.backgroundColor = 'var(--md-default-bg-color, white)';
    widget.style.borderRadius = '16px';
    widget.style.boxShadow = 'var(--md-shadow-z2, 0 10px 25px -5px rgba(0,0,0,0.1))';
    widget.style.display = 'flex';
    widget.style.flexDirection = 'column';
    widget.style.zIndex = '1000';
    widget.style.border = '1px solid var(--md-divider-color, #e5e7eb)';
    widget.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    widget.style.opacity = '0';
    widget.style.transform = 'translateY(20px)';
    widget.style.pointerEvents = 'none';

    // Chat header
    const header = document.createElement('div');
    header.className = 'chat-header';
    header.style.padding = '16px';
    header.style.borderBottom = '1px solid var(--md-divider-color, #f3f4f6)';
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';
    header.style.backgroundColor = 'var(--md-default-bg-color--container, #f8fafc)';

    const title = document.createElement('h3');
    title.textContent = chatTitle;
    title.style.margin = '0';
    title.style.fontSize = '1.25rem';
    title.style.fontWeight = '600';
    title.style.color = 'var(--md-default-fg-color, #1f2937)';

    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';
    closeBtn.style.background = 'none';
    closeBtn.style.border = 'none';
    closeBtn.style.color = 'var(--md-default-fg-color--medium, #6b7280)';
    closeBtn.style.fontSize = '1.25rem';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.padding = '4px';
    closeBtn.style.borderRadius = '50%';
    closeBtn.style.width = '36px';
    closeBtn.style.height = '36px';
    closeBtn.style.display = 'flex';
    closeBtn.style.alignItems = 'center';
    closeBtn.style.justifyContent = 'center';
    closeBtn.onmouseover = () => {
      closeBtn.style.backgroundColor = 'var(--md-default-bg-color--light, #f3f4f6)';
    };
    closeBtn.onmouseout = () => {
      closeBtn.style.color = 'var(--md-default-fg-color--medium, #6b7280)';
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
    inputContainer.className = 'chat-input-container';
    inputContainer.style.padding = '16px';
    inputContainer.style.borderTop = '1px solid var(--md-divider-color, #f3f4f6)';
    inputContainer.style.display = 'flex';
    inputContainer.style.gap = '12px';
    inputContainer.style.backgroundColor = 'var(--md-default-bg-color--container, #f8fafc)';

    const input = document.createElement('input');
    input.id = 'chat-input';
    input.type = 'text';
    input.placeholder = chatPlaceholder;
    input.style.flex = '1';
    input.style.padding = '12px 16px';
    input.style.border = '1px solid var(--md-input-border-color, #e5e7eb)';
    input.style.borderRadius = '12px';
    input.style.fontSize = '1rem';
    input.style.outline = 'none';
    input.style.transition = 'border-color 0.2s ease';
    input.onfocus = () => {
      input.style.borderColor = 'var(--md-primary-fg-color, #6366f1)';
    };
    input.onblur = () => {
      input.style.borderColor = 'var(--md-input-border-color, #e5e7eb)';
    };
    input.onkeypress = (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    };

    const sendBtn = document.createElement('button');
    sendBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>';
    sendBtn.style.backgroundColor = 'var(--md-primary-fg-color, #6366f1)';
    sendBtn.style.color = 'white';
    sendBtn.style.border = 'none';
    sendBtn.style.borderRadius = '50%';
    sendBtn.style.width = '40px';
    sendBtn.style.height = '40px';
    sendBtn.style.cursor = 'pointer';
    sendBtn.style.display = 'flex';
    sendBtn.style.alignItems = 'center';
    sendBtn.style.justifyContent = 'center';
    sendBtn.style.boxShadow = 'var(--md-shadow-z1, 0 2px 4px -1px rgba(0,0,0,0.1))';
    sendBtn.onmouseover = () => {
      sendBtn.style.backgroundColor = 'var(--md-accent-fg-color, #4f46e5)';
    };
    sendBtn.onmouseout = () => {
      sendBtn.style.backgroundColor = 'var(--md-primary-fg-color, #6366f1)';
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
      avatar.style.backgroundColor = 'var(--md-primary-fg-color, #6366f1)';
      avatar.textContent = 'U';
      avatar.style.backgroundColor = '#6366f1';
      avatar.style.color = 'white';
      avatar.style.fontWeight = '700';
      avatar.style.fontSize = '0.75rem';
      avatar.style.display = 'flex';
      avatar.style.alignItems = 'center';
      avatar.style.justifyContent = 'center';
      avatar.style.borderRadius = '50%';
      messageDiv.style.marginLeft = 'auto';
    } else {
      avatar.style.backgroundColor = 'var(--md-default-fg-color--light, #f3f4f6)';
      avatar.textContent = 'AIdo';
      avatar.style.backgroundColor = '#6366f1';
      avatar.style.color = 'white';
      avatar.style.fontWeight = '700';
      avatar.style.fontSize = '0.75rem';
      avatar.style.display = 'flex';
      avatar.style.alignItems = 'center';
      avatar.style.justifyContent = 'center';
      avatar.style.borderRadius = '50%';
      messageDiv.style.marginRight = 'auto';
    }

    const messageContent = document.createElement('div');
    messageContent.className = 'chat-bubble-content';
    messageDiv.className = isUser ? 'chat-bubble user' : 'chat-bubble ai';
    messageContent.style.padding = '12px 16px';
    messageContent.style.borderRadius = isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px';
    messageContent.style.backgroundColor = isUser ? 'var(--md-primary-fg-color, #6366f1)' : 'var(--md-default-fg-color--light, #f3f4f6)';
    messageContent.style.color = isUser ? 'white' : 'var(--md-default-fg-color, #1f2937)';
    messageContent.style.lineHeight = '1.5';
    messageContent.style.fontSize = '0.8rem';
    messageContent.style.wordWrap = 'break-word';
    messageContent.style.maxWidth = '100%';

    messageContent.textContent = content;

    messageDiv.appendChild(isUser ? messageContent : avatar);
    messageDiv.appendChild(!isUser ? messageContent : avatar);

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return messageDiv;
  }

  async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

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
    typingAvatar.style.backgroundColor = 'var(--md-default-fg-color--light, #f3f4f6)';
    typingAvatar.style.display = 'flex';
    typingAvatar.style.alignItems = 'center';
    typingAvatar.style.justifyContent = 'center';
    typingAvatar.style.fontSize = '0.875rem';
    typingAvatar.style.fontWeight = '600';
    typingAvatar.style.color = 'var(--md-default-fg-color--medium, #6b7280)';
    typingAvatar.textContent = 'AI';

    const typingContent = document.createElement('div');
    typingContent.style.padding = '12px 16px';
    typingContent.style.borderRadius = '16px 16px 16px 4px';
    typingContent.style.backgroundColor = 'var(--md-default-fg-color--light, #f3f4f6)';
    typingContent.style.color = 'var(--md-default-fg-color, #1f2937)';
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
      // Call RAG API — API key injected at build time from GitHub Secret
      const response = await fetch('https://rag.aldof.duckdns.org/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'aido_rag_813606c1cf96d6712e7a95196881e7e9',
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
        console.log('RAG response:', data);
        const bubble = addMessage(data.answer, false);
        // Show sources as inline citations below the assistant message (XSS-safe)
        if (data.sources && Array.isArray(data.sources)) {
          const sourcesDiv = document.createElement('div');
          sourcesDiv.className = 'chat-sources';
          sourcesDiv.style.cssText = 'font-size:0.75rem;color:var(--md-default-fg-color--medium);margin-top:4px;padding-left:12px;';
          const escape = s => String(s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;')
            .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
          sourcesDiv.innerHTML = '<strong>Sources:</strong> ' + data.sources.map(s => {
            const url = (s.url || s.link || '#').trim();
            const title = escape(s.title || s.source || 'Reference');
            const safeUrl = url.startsWith('http') ? escape(url) : '#';
            return '<a href="' + safeUrl + '" target="_blank" rel="noopener noreferrer">' + title + '</a>';
          }).join(', ');
          if (bubble) bubble.appendChild(sourcesDiv);
        }
      } else if (data && data.detail) {
        // RAG returned an error (e.g. auth failure, upstream failure)
        addMessage('RAG service error: ' + data.detail, false);
      } else {
        addMessage('Sorry, I encountered an error. Please try again.', false);
      }
    } catch (error) {
      if (typingDiv) {
        typingDiv.remove();
      }
      addMessage('Sorry, I encountered an error. Please check your connection and try again.', false);
      console.error('Chat error:', error);
    }
  }

  // RAG health check — verify the endpoint is reachable and returns a valid response
  // before revealing the FAB. Invalid/missing API key or unreachable service → button stays hidden.
  async function checkRagHealth() {
    try {
      const res = await fetch('https://rag.aldof.duckdns.org/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'aido_rag_813606c1cf96d6712e7a95196881e7e9',
        },
        body: JSON.stringify({ question: '_health_check_', k: 1 })
      });
      if (!res.ok) return false;
      const json = await res.json();
      // A valid response has at least an 'answer' string with content
      return !!(json && typeof json.answer === 'string' && json.answer.trim().length > 0);
    } catch (_) {
      return false;
    }
  }

  // Initialize
  async function init() {
    const isHealthy = await checkRagHealth();
    if (!isHealthy) {
      console.log('RAG unavailable — chat button hidden');
      return; // FAB + widget never created
    }
    createChatButton();
    createChatWidget();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    setTimeout(init, 0);
  }
})();