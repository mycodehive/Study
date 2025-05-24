import React from 'react';
import { useState } from 'react';

function App() {
  const [content, setContent] = useState('');
  const [isPublic, setIsPublic] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async () => {
    const response = await fetch('http://localhost:8000/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, is_public: isPublic }),
    });
    const data = await response.json();
    setMessage(data.message);
  };

  return (
    <div>
      <h1>일기 저장</h1>
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <label>
        <input
          type="checkbox"
          checked={isPublic}
          onChange={(e) => setIsPublic(e.target.checked)}
        />
        공개 여부
      </label>
      <button onClick={handleSubmit}>저장</button>
      <p>{message}</p>
    </div>
  );
}

export default App;
