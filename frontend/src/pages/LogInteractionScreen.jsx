import React, { useState } from 'react';
import ChatInterface from '../components/ChatInterface';
import InsightsPanel from '../components/InsightsPanel';
import StructuredForm from '../components/StructuredForm';
import { MessageSquare, LayoutList } from 'lucide-react';

const LogInteractionScreen = () => {
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' or 'form'

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>VeevaNext CRM</h1>
        <div className="tab-buttons">
          <button
            onClick={() => setActiveTab('chat')}
            className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
          >
            <MessageSquare size={16} />
            AI Chat
          </button>
          <button
            onClick={() => setActiveTab('form')}
            className={`tab-btn ${activeTab === 'form' ? 'active' : ''}`}
          >
            <LayoutList size={16} />
            Manual Entry
          </button>
        </div>
      </header>

      <main className="main-content">
        <div className="content-wrapper">
          
          <div className="primary-panel">
            {activeTab === 'chat' ? <ChatInterface /> : <StructuredForm />}
          </div>

          <div className="secondary-panel">
            <InsightsPanel />
          </div>

        </div>
      </main>
    </div>
  );
};

export default LogInteractionScreen;
