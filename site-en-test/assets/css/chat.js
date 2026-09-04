/* Chat widget styles */
#chat-toggle-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #6366f1;
  color: white;
  border: none;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

#chat-toggle-btn:hover {
  transform: scale(1.05);
  background-color: #4f46e5;
}

#chat-widget {
  position: fixed;
  bottom: 90px;
  right: 24px;
  width: 350px;
  height: 500px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  border: 1px solid #e5e7eb;
  opacity: 0;
  transform: translateY(20px);
  pointer-events: none;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

#chat-widget .header {
  padding: 16px;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8fafc;
}

#chat-widget h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

#chat-widget button {
  background: none;
  border: none;
  color: #6b7280;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

#chat-widget button:hover {
  background-color: #f3f4f6;
  color: #1f2937;
}

#chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-message {
  display: flex;
  flex-direction: row-reverse;
  align-items: flex-start;
  max-width: 80%;
}

.chat-message.user {
  margin-left: auto;
}

.chat-message.ai {
  margin-right: auto;
}

.chat-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
}
