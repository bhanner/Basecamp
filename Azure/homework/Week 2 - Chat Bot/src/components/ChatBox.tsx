import React, { useEffect, useRef, useState } from 'react';
import Message from './Message';
import '../styles/ChatBox.css';
import { callOpenAI } from '../services/OpenAIService';
import { MessageProps } from '../models/MessageProps';

interface ChatBoxProps {
  message: MessageProps[];
  username: string;
}

const ChatBox: React.FC<ChatBoxProps> = ({ message, username }) => {
  const [messages, setMessages] = useState<MessageProps[]>(message);
  const [inputValue, setInputValue] = useState('Where was Mr.Hugo Biscuits birthday held?');
  const [streamingResponse, setStreamingResponse] = useState<string>('');

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, streamingResponse]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() !== '') {
      setInputValue('');
      const newMessage: MessageProps = { role: 'user', content: inputValue };
      const chatHistory = [...messages, newMessage];
      setMessages([...messages, newMessage]);
      try {
        const stream = await callOpenAI(chatHistory);

        let response = '';
        for await (const chunk of stream) {
          response += chunk;
          setStreamingResponse(response);
        }

        const responseMessage: MessageProps = { role: 'assistant', content: response };
        setMessages([...messages, newMessage, responseMessage]);
        setStreamingResponse('');
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  return (
    <div className="chat-box">
      <div className="messages">
        {messages.map((msg, index) => (
          <Message
            key={index}
            content={msg.content}
            role={msg.role === 'user' ? username : msg.role === 'assistant' ? 'AI' : msg.role}
          />
        ))}
        {streamingResponse && (
          <div>
            <Message content={streamingResponse} role={'AI'} />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-container">
        <input
          type="text"
          className="chat-input"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Type a message..."
          onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
        />
        <button className="send-button" onClick={handleSendMessage} disabled={inputValue.trim() === ''}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBox;