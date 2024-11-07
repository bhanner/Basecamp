import React, { useState } from 'react';
import ChatBox from './components/ChatBox';
import NamePrompt from './components/NamePrompt';
import './styles/App.css';
import { MessageProps } from './models/MessageProps';

const App: React.FC = () => {
  const [messages] = useState<MessageProps[]>([]);
  const [username, setUsername] = useState<string | null>(null);

  const handleUsernameSubmit = (name: string) => {
    setUsername(name);
  };

  return (
    <div className="App">
      <h1 className="App-header">The Amazing Chat-o-tron 5000</h1>
      <div className="Chat-container">
        {username ? (
          <ChatBox message={messages} username={username} />
        ) : (
          <NamePrompt onSubmit={handleUsernameSubmit} />
        )}
      </div>
    </div>
  );
};

export default App;