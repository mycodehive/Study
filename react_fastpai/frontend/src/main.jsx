import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // ← 여기에서 상대 경로 ./App 확인

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
