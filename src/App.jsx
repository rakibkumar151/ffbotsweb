
import React, { useState } from 'react';
import './App.css';
import { EMOTES } from './emotesData';

function App() {
  const [activeTab, setActiveTab] = useState('player-info');
  const [uid, setUid] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  const fetchInfo = async () => {
    if (!uid) return;
    setLoading(true);
    setError('');
    setData(null);

    try {
      const response = await fetch(`http://localhost:8000/info/${uid}`);
      if (!response.ok) throw new Error('UID not found or server error');
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      {/* Sidebar Navigation */}
      <aside className="sidebar glass">
        <div className="logo fire-text">FF PREMIUM</div>
        <nav>
          <div 
            className={`nav-item ${activeTab === 'player-info' ? 'active' : ''}`}
            onClick={() => setActiveTab('player-info')}
          >
            👤 PLAYER INFO
          </div>
          <div 
            className={`nav-item ${activeTab === 'emotes' ? 'active' : ''}`}
            onClick={() => setActiveTab('emotes')}
          >
            🎭 EMOTES LIST
          </div>
          <div className="nav-item">📈 RANK MODES</div>
          <div className="nav-item">⚙️ SETTINGS</div>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="content">
        {activeTab === 'player-info' && (
          <section className="player-info-section">
            <header style={{ marginBottom: '30px' }}>
              <h1 className="neon-text">Player Profile Viewer</h1>
              <p style={{ color: '#aaa' }}>Enter UID to get full account details directly from server</p>
            </header>

            <div className="glass search-box" style={{ padding: '30px', marginBottom: '30px' }}>
              <div style={{ display: 'flex', gap: '15px' }}>
                <input 
                  type="text" 
                  placeholder="Enter UID (e.g. 2545042710)" 
                  value={uid}
                  onChange={(e) => setUid(e.target.value)}
                />
                <button onClick={fetchInfo} disabled={loading} style={{ minWidth: '150px' }}>
                  {loading ? 'FETCHING...' : 'SEARCH UID'}
                </button>
              </div>
              {error && <p style={{ color: '#ff4b2b', marginTop: '15px' }}>❌ {error}</p>}
            </div>

            {loading && (
              <div className="spinner-container">
                <div className="spinner"></div>
                <p>Establishing Secure Session...</p>
              </div>
            )}

            {data && (
              <div className="glass result-card fadeIn">
                <div className="result-header">
                  <div>
                    <h2 className="fire-text">{data.name || 'Unknown'}</h2>
                    <p style={{ color: '#888' }}>UID: {uid} | Region: {data.region || 'IND'}</p>
                  </div>
                  <div className="level-badge glass neon-border">
                    LVL {data.level || '??'}
                  </div>
                </div>

                <div className="stats-grid">
                  <div className="stat-box">
                    <span className="stat-label">LIKES</span>
                    <span className="stat-value">❤️ {data.likes || '0'}</span>
                  </div>
                  <div className="stat-box">
                    <span className="stat-label">HONOR SCORE</span>
                    <span className="stat-value">⭐ {data.honor || '100'}</span>
                  </div>
                  <div className="stat-box">
                    <span className="stat-label">EXP</span>
                    <span className="stat-value">⚡ {data.exp || '0'}</span>
                  </div>
                  <div className="stat-box">
                    <span className="stat-label">BR RANK</span>
                    <span className="stat-value">🏆 {data.br_rank || 'Bronze'}</span>
                  </div>
                  <div className="stat-box">
                    <span className="stat-label">CS POINTS</span>
                    <span className="stat-value">🔫 {data.cs_points || '0'}</span>
                  </div>
                  <div className="stat-box">
                    <span className="stat-label">BP LEVEL</span>
                    <span className="stat-value">🎫 {data.bp_level || '0'}</span>
                  </div>
                  <div className="stat-box" style={{ gridColumn: 'span 2' }}>
                    <span className="stat-label">BIO</span>
                    <span className="stat-value" style={{ fontSize: '0.9rem', fontStyle: 'italic' }}>"{data.bio || 'No Bio'}"</span>
                  </div>
                </div>
              </div>
            )}
          </section>
        )}

        {activeTab === 'emotes' && (
          <section className="emotes-section fadeIn">
            <header style={{ marginBottom: '30px' }}>
              <h1 className="neon-text">Garena Emotes List</h1>
              <p style={{ color: '#aaa' }}>Total {EMOTES.length} emotes found in database</p>
            </header>
            <div className="emotes-grid">
              {EMOTES.map(emote => (
                <div key={emote.id} className="glass emote-card">
                  <div className="emote-icon">🎭</div>
                  <p className="fire-text" style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>{emote.label}</p>
                  <p style={{ fontSize: '0.7rem', color: '#666', marginTop: '5px' }}>ID: {emote.id}</p>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
