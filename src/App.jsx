import { useState } from 'react';
import './App.css';
import { EMOTES } from './emotesData';

function App() {
  const [teamCode, setTeamCode] = useState('');
  const [targetUid, setTargetUid] = useState('');
  const [logs, setLogs] = useState([]);
  const [loadingEmote, setLoadingEmote] = useState(null);

  const addLog = (msg, type = 'info') => {
    setLogs(prev => [...prev, { time: new Date().toLocaleTimeString(), msg, type }]);
  };

  const sendEmote = async (emote) => {
    if (!teamCode) {
      addLog('Error: Team Code is required!', 'error');
      return;
    }

    setLoadingEmote(emote.name);
    addLog(`Sending ${emote.label} to Team ${teamCode}...`, 'warning');

    try {
      const response = await fetch('https://ff-botf.onrender.com/api/emote', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          team_code: teamCode,
          target_uid: targetUid,
          emote_id: emote.id
        })
      });
      
      const data = await response.json();
      
      if (!response.ok || data.error) {
        throw new Error(data.error || 'Failed to connect to Bot Server');
      }
      
      addLog(`✅ Successfully sent ${emote.label}!`, 'success');
    } catch (error) {
      addLog(`❌ Error: ${error.message}`, 'error');
    } finally {
      setLoadingEmote(null);
    }
  };

  return (
    <div className="app-container">
      <div className="glow-circle top-left"></div>
      <div className="glow-circle bottom-right"></div>
      
      <header className="header">
        <h1 className="title">B25 <span className="highlight">CHEATS</span></h1>
        <p className="subtitle">Advanced Fast Emote System</p>
      </header>

      <main className="main-content">
        <div className="control-panel glass-panel">
          <h2 className="panel-title">Target Setup</h2>
          
          <div className="input-group">
            <label>Team Code <span className="required">*</span></label>
            <input 
              type="text" 
              placeholder="Enter 8-digit Team Code" 
              value={teamCode}
              onChange={(e) => setTeamCode(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Target UID <span className="optional">(Optional)</span></label>
            <input 
              type="text" 
              placeholder="Leave blank for self" 
              value={targetUid}
              onChange={(e) => setTargetUid(e.target.value)}
            />
          </div>

          <div className="settings-row">
            <label className="checkbox-label">
              <input type="checkbox" defaultChecked />
              <span className="checkbox-custom"></span>
              Auto Leave (Millisecond Mode)
            </label>
            <label className="checkbox-label">
              <input type="checkbox" />
              <span className="checkbox-custom"></span>
              Lag Mode (Anti-Ban)
            </label>
          </div>
        </div>

        <div className="terminal-panel glass-panel">
          <div className="terminal-header">
            <div className="dots"><span></span><span></span><span></span></div>
            <span className="terminal-title">System Logs</span>
          </div>
          <div className="terminal-body">
            {logs.length === 0 ? (
              <div className="log empty">Awaiting commands...</div>
            ) : (
              logs.map((log, idx) => (
                <div key={idx} className={`log ${log.type}`}>
                  <span className="time">[{log.time}]</span> {log.msg}
                </div>
              ))
            )}
          </div>
        </div>
      </main>

      <section className="emotes-section">
        <h2 className="section-title">Available Emotes <span className="badge">{EMOTES.length}</span></h2>
        <div className="emotes-grid">
          {EMOTES.map(emote => (
            <div key={emote.id} className="emote-card glass-panel">
              <div className="emote-icon">
                <img 
                  src={`https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/${emote.id}.png`} 
                  alt={emote.label} 
                  loading="lazy"
                />
              </div>
              <div className="emote-info">
                <h3>{emote.label}</h3>
                <p>ID: {emote.id}</p>
              </div>
              <button 
                className={`send-btn ${loadingEmote === emote.name ? 'loading' : ''}`}
                onClick={() => sendEmote(emote)}
                disabled={loadingEmote !== null}
              >
                {loadingEmote === emote.name ? 'Sending...' : 'Send Emote'}
              </button>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;
