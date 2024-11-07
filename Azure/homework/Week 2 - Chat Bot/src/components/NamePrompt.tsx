import React, { useState } from 'react';

interface NamePromptProps {
  onSubmit: (name: string) => void;
}

const NamePrompt: React.FC<NamePromptProps> = ({ onSubmit }) => {
  const [name, setName] = useState<string>('GianPiero');
  const [submitted, setSubmitted] = useState<boolean>(false);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    setSubmitted(true);
    setTimeout(() => onSubmit(name), 500); // Delay to allow fade-out effect
  };

  return (
    <div className={`name-prompt ${submitted ? 'fade-out' : ''}`}>
      {!submitted ? (
        <form onSubmit={handleSubmit}>
          <label>
            Please enter your name:
            <input
              type="text"
              value={name}
              className="chat-input"
              onChange={(e) => setName(e.target.value)}
              required
            />
          </label>
          <button type="submit" className="send-button">Submit</button>
        </form>
      ) : (
        <h1>Hello, {name}!</h1>
      )}
    </div>
  );
};

export default NamePrompt;