import { useState, useEffect } from 'react';
import './App.css';
import { EMOTES } from './emotesData';

function App() {
  const [teamCode, setTeamCode] = useState('');
  const [targetUid, setTargetUid] = useState('');
  const [logs, setLogs] = useState([]);
  const [loadingEmote, setLoadingEmote] = useState(null);
  const [isAutoStarting, setIsAutoStarting] = useState(false);
  const [loadingAction, setLoadingAction] = useState(null);
  const [botCount, setBotCount] = useState(0);

  useEffect(() => {
    const fetchBots = async () => {
      try {
        const res = await fetch('https://ffbots-1.onrender.com/api/bots');
        const data = await res.json();
        if (data.bots) setBotCount(data.bots.length);
      } catch (e) {
        console.error("Bot check failed", e);
      }
    };
    fetchBots();
    const interval = setInterval(fetchBots, 10000);
    return () => clearInterval(interval);
  }, []);

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
      const response = await fetch('https://ffbots-1.onrender.com/api/emote', {
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

  const handleAutoStart = async (action) => {
    if (action === 'start' && !teamCode) {
      addLog('Error: Team Code required for Auto Start!', 'error');
      return;
    }

    setLoadingAction(action === 'start' ? 'auto-start' : 'auto-stop');
    addLog(`${action === 'start' ? 'Starting' : 'Stopping'} Match Bot...`, 'warning');

    try {
      const response = await fetch('https://ffbots-1.onrender.com/api/auto_start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, team_code: teamCode })
      });
      const data = await response.json();
      if (!response.ok || data.error) throw new Error(data.error);
      
      setIsAutoStarting(action === 'start');
      addLog(`✅ Match Bot ${action === 'start' ? 'Started' : 'Stopped'}!`, 'success');
    } catch (error) {
      addLog(`❌ Error: ${error.message}`, 'error');
    } finally {
      setLoadingAction(null);
    }
  };

  const sendGroupInvite = async (limit) => {
    setLoadingAction(`group-${limit}`);
    addLog(`Sending ${limit}-Player Group Invitation...`, 'warning');

    try {
      const response = await fetch('https://ffbots-1.onrender.com/api/group_invite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ limit, target_uid: targetUid })
      });
      const data = await response.json();
      if (!response.ok || data.error) throw new Error(data.error);
      
      addLog(`✅ Successfully sent ${limit}-player invitation!`, 'success');
    } catch (error) {
      addLog(`❌ Error: ${error.message}`, 'error');
    } finally {
      setLoadingAction(null);
    }
  };

  return (
    <div className="app-container">
      <div className="glow-circle top-left"></div>
      <div className="glow-circle bottom-right"></div>
      
      <header className="header">
        <h1 className="title">NIKI <span className="highlight">BOT</span></h1>
        <p className="subtitle">Premium Emote Control System</p>
        <div className="status-bar">
          <span className={`status-dot ${botCount > 0 ? 'online' : 'offline'}`}></span>
          {botCount} Bots Online
        </div>
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
              Auto Leave
            </label>
            <label className="checkbox-label">
              <input type="checkbox" />
              <span className="checkbox-custom"></span>
              Triple Packet
            </label>
          </div>
        </div>

        <div className="features-panel glass-panel">
          <h2 className="panel-title">Bot Features</h2>
          
          <div className="feature-group">
            <label>Match Bot (Auto Start)</label>
            <div className="button-row">
              {!isAutoStarting ? (
                <button 
                  className="action-btn start" 
                  onClick={() => handleAutoStart('start')}
                  disabled={loadingAction !== null}
                >
                  {loadingAction === 'auto-start' ? 'Starting...' : 'Start Match Bot'}
                </button>
              ) : (
                <button 
                  className="action-btn stop" 
                  onClick={() => handleAutoStart('stop')}
                  disabled={loadingAction !== null}
                >
                  {loadingAction === 'auto-stop' ? 'Stopping...' : 'Stop Match Bot'}
                </button>
              )}
            </div>
          </div>

          <div className="feature-group">
            <label>Group Generator</label>
            <div className="grid-buttons">
              {[3, 4, 5, 6].map(num => (
                <button 
                  key={num}
                  className="num-btn"
                  onClick={() => sendGroupInvite(num)}
                  disabled={loadingAction !== null}
                >
                  {loadingAction === `group-${num}` ? '...' : `${num}P`}
                </button>
              ))}
            </div>
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
