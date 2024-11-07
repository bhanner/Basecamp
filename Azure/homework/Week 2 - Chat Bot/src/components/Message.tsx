import React from 'react';
import '../styles/Message.css';
import { MessageProps } from '../models/MessageProps';

const Message: React.FC<MessageProps> = ({ content, role }) => {
  return (
    <div className="message">
      <span className="role">{role}:</span>
      <span className="content">{content}</span>
    </div>
  );
};

export default Message;