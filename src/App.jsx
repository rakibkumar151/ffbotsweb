
import React, { useState } from 'react';
import './App.css';

function App() {
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
    <div className="container" style={{ maxWidth: '900px', margin: '0 auto', padding: '50px 20px' }}>
      <header style={{ textAlign: 'center', marginBottom: '50px' }}>
        <h1 className="fire-text" style={{ fontSize: '3rem', marginBottom: '10px' }}>FREE FIRE</h1>
        <h2 className="neon-text" style={{ fontSize: '1.2rem', color: '#00f3ff' }}>UID PROFILE VIEWER</h2>
      </header>

      <div className="glass" style={{ padding: '40px', textAlign: 'center' }}>
        <p style={{ marginBottom: '20px', color: '#ccc' }}>Enter Player UID to Fetch Real-time Information</p>
        <div style={{ display: 'flex', gap: '10px', maxWidth: '500px', margin: '0 auto' }}>
          <input 
            type="text" 
            placeholder="e.g. 2545042710" 
            value={uid}
            onChange={(e) => setUid(e.target.value)}
            style={{ margin: 0 }}
          />
          <button onClick={fetchInfo} disabled={loading}>
            {loading ? 'SEARCHING...' : 'FETCH INFO'}
          </button>
        </div>

        {error && <p style={{ color: '#ff4b2b', marginTop: '20px' }}>❌ {error}</p>}
      </div>

      {loading && (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
          <div className="spinner" style={{ 
            width: '50px', height: '50px', border: '5px solid #333', 
            borderTopColor: '#00f3ff', borderRadius: '50%', 
            animation: 'spin 1s linear infinite', margin: '0 auto' 
          }}></div>
          <p style={{ marginTop: '10px' }}>Accessing Garena Servers...</p>
        </div>
      )}

      {data && (
        <div className="glass" style={{ marginTop: '40px', padding: '40px', borderTop: '2px solid #ff4b2b' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '30px' }}>
            <div>
              <h2 className="fire-text" style={{ fontSize: '2rem' }}>{data.name || 'Unknown Player'}</h2>
              <p style={{ color: '#aaa' }}>UID: {uid}</p>
            </div>
            <div className="glass" style={{ padding: '10px 20px', borderRadius: '50px', borderColor: '#00f3ff' }}>
              <span className="neon-text">Level {data.level || 'N/A'}</span>
            </div>
          </div>

          <div className="profile-grid">
            <div className="info-item">
              <div className="info-label">Likes</div>
              <div className="info-value">❤️ {data.likes || 'N/A'}</div>
            </div>
            <div className="info-item">
              <div className="info-label">Honor Score</div>
              <div className="info-value">⭐ {data.honor || 'N/A'}</div>
            </div>
            <div className="info-item">
              <div className="info-label">Exp</div>
              <div className="info-value">⚡ {data.exp || 'N/A'}</div>
            </div>
            <div className="info-item">
              <div className="info-label">BR Rank</div>
              <div className="info-value">🏆 {data.br_rank || 'N/A'}</div>
            </div>
            <div className="info-item">
              <div className="info-label">CS Points</div>
              <div className="info-value">🔫 {data.cs_points || 'N/A'}</div>
            </div>
            <div className="info-item">
              <div className="info-label">Prime Level</div>
              <div className="info-value">💎 {data.prime_level || 'N/A'}</div>
            </div>
            <div className="info-item">
              <div className="info-label">Account Created</div>
              <div className="info-value">📅 {data.created || 'N/A'}</div>
            </div>
            <div className="info-item">
              <div className="info-label">Last Login</div>
              <div className="info-value">🕒 {data.last_login || 'N/A'}</div>
            </div>
            <div className="info-item">
              <div className="info-label">BP Level</div>
              <div className="info-value">🎫 {data.bp_level || 'N/A'}</div>
            </div>
          </div>

          <div className="info-item" style={{ marginTop: '20px', borderLeftColor: '#00f3ff' }}>
            <div className="info-label">Bio</div>
            <div className="info-value" style={{ fontStyle: 'italic', color: '#ccc' }}>"{data.bio || 'No bio available'}"</div>
          </div>
        </div>
      )}

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
}

export default App;
