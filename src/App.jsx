import { useState, useEffect } from 'react';
import './App.css';
import { EMOTES } from './emotesData';

function App() {
  const [teamCode, setTeamCode] = useState('');
  const [targetUids, setTargetUids] = useState(['', '', '', '', '']);
  const [logs, setLogs] = useState([]);
  const [loadingEmote, setLoadingEmote] = useState(null);
  const [isAutoStarting, setIsAutoStarting] = useState(false);
  const [loadingAction, setLoadingAction] = useState(null);
  const [botCount, setBotCount] = useState(0);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [currentMenu, setCurrentMenu] = useState('emote'); // 'emote' or 'levelup'
  const [isLevelUpUnlocked, setIsLevelUpUnlocked] = useState(false);
  const [levelUpPass, setLevelUpPass] = useState('');
  const [levelUpError, setLevelUpError] = useState('');
  const [matchStats, setMatchStats] = useState({ running: false, games_played: 0, runtime: 0, bot_uid: null });

  useEffect(() => {
    let interval;
    if (isLoggedIn && currentMenu === 'levelup') {
      const fetchStats = async () => {
        try {
          const res = await fetch('https://ffbots-1.onrender.com/api/match_bot_stats', { headers: getAuthHeaders() });
          const data = await res.json();
          setMatchStats(data);
        } catch (e) {}
      };
      fetchStats();
      interval = setInterval(fetchStats, 2000);
    }
    return () => clearInterval(interval);
  }, [isLoggedIn, currentMenu]);

  useEffect(() => {
    const savedKey = localStorage.getItem('niki_bot_key');
    const loginTime = localStorage.getItem('niki_bot_login_time');
    
    if (savedKey && loginTime) {
      const oneHour = 60 * 60 * 1000;
      const now = new Date().getTime();
      
      if (now - parseInt(loginTime) > oneHour) {
        // Session expired
        localStorage.removeItem('niki_bot_key');
        localStorage.removeItem('niki_bot_login_time');
        setIsLoggedIn(false);
      } else {
        verifyKey(savedKey);
      }
    }
  }, []);

  const verifyKey = async (token) => {
    try {
      // In a real app, we'd verify the token. 
      // For now, we assume if it's in localStorage, it's valid until a 401 occurs.
      setIsLoggedIn(true);
    } catch (e) {
      localStorage.removeItem('niki_bot_key');
    }
  };

  const onLoginSubmit = async (e) => {
    e.preventDefault();
    setLoginError('');
    setIsLoggingIn(true);
    try {
      const res = await fetch('https://ffbots-1.onrender.com/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (data.success) {
        setIsLoggedIn(true);
        const now = new Date().getTime();
        localStorage.setItem('niki_bot_key', data.token);
        localStorage.setItem('niki_bot_login_time', now.toString());
      } else {
        setLoginError(data.error || 'Invalid Credentials');
      }
    } catch (e) {
      setLoginError('Connection Error');
    } finally {
      setIsLoggingIn(false);
    }
  };

  const getAuthHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('niki_bot_key')}`
  });

  useEffect(() => {
    const fetchBots = async () => {
      try {
        const res = await fetch('https://ffbots-1.onrender.com/api/bots', {
          headers: getAuthHeaders()
        });
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
        headers: getAuthHeaders(),
        body: JSON.stringify({
          team_code: teamCode,
          target_uids: targetUids.filter(uid => uid.trim() !== ''),
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

  const handleLevelUpLogin = async (e) => {
    e.preventDefault();
    setLoadingAction('unlock');
    setLevelUpError('');
    try {
      const res = await fetch('https://ffbots-1.onrender.com/api/verify_github_pass', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ password: levelUpPass })
      });
      const data = await res.json();
      if (data.success) {
        setIsLevelUpUnlocked(true);
        addLog('🔓 Level Up Bot Unlocked!', 'success');
      } else {
        setLevelUpError(data.error || 'Invalid Password');
      }
    } catch (e) {
      setLevelUpError('Server Connection Failed');
    } finally {
      setLoadingAction(null);
    }
  };

  const formatRuntime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
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
        headers: getAuthHeaders(),
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
        headers: getAuthHeaders(),
        body: JSON.stringify({ limit, target_uid: targetUids[0] })
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

  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <div className="mesh-bg"></div>
        <div className="glow-circle top-left"></div>
        <div className="glow-circle bottom-right"></div>
        
        <div className="login-card glass-panel">
          <div className="brand-badge">PREMIUM ACCESS</div>
          <div className="login-header">
            <h1 className="title">NIKI <span className="highlight">BOT</span></h1>
            <p className="subtitle">Secure Administrator Portal</p>
          </div>
          
          <form onSubmit={onLoginSubmit}>
            <div className="input-group">
              <label>Username</label>
              <input 
                type="text" 
                placeholder="Enter admin username" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label>Password</label>
              <input 
                type="password" 
                placeholder="Enter your password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            
            {loginError && (
              <div className="error-box">
                <span>⚠️</span> {loginError}
              </div>
            )}
            
            <button 
              type="submit" 
              className={`login-btn ${isLoggingIn ? 'loading' : ''}`}
              disabled={isLoggingIn}
            >
              {isLoggingIn ? 'Authenticating...' : 'Sign In'}
            </button>
          </form>
          
          <div className="login-footer">
            <p>© 2026 NIKI BOT • All Rights Reserved</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-layout">
      <aside className="sidebar glass-panel">
        <div className="sidebar-header">
          <div className="logo">N</div>
          <h3>NIKI BOT</h3>
        </div>
        <nav className="nav-menu">
          <button 
            className={`nav-item ${currentMenu === 'emote' ? 'active' : ''}`}
            onClick={() => setCurrentMenu('emote')}
          >
            <span className="icon">🎭</span> Emote Control
          </button>
          <button 
            className={`nav-item ${currentMenu === 'levelup' ? 'active' : ''}`}
            onClick={() => setCurrentMenu('levelup')}
          >
            <span className="icon">⚡</span> Level Up Bot
          </button>
        </nav>
        <div className="sidebar-footer">
          <div className="bot-indicator">
            <span className={`status-dot ${botCount > 0 ? 'online' : 'offline'}`}></span>
            {botCount} Bots
          </div>
        </div>
      </aside>

      <main className="app-container">
        <div className="glow-circle top-left"></div>
        <div className="glow-circle bottom-right"></div>
        
        <header className="header">
          <h1 className="title">
            {currentMenu === 'emote' ? 'EMOTE' : 'LEVEL UP'} <span className="highlight">PORTAL</span>
          </h1>
          <p className="subtitle">
            {currentMenu === 'emote' ? 'Premium Emote Control System' : 'Automated Level Farming System'}
          </p>
        </header>

        {currentMenu === 'emote' ? (
          <div className="menu-content">
            <div className="main-content">
              <div className="control-panel glass-panel">
                <h2 className="panel-title">Target Setup</h2>
                <div className="input-group">
                  <label>Team Code <span className="required">*</span></label>
                  <input type="text" placeholder="Enter Team Code" value={teamCode} onChange={(e) => setTeamCode(e.target.value)} />
                </div>
                <div className="input-group">
                  <label>Target UIDs <span className="optional">(Multi-Target)</span></label>
                  <div className="uids-grid">
                    {targetUids.map((uid, idx) => (
                      <input key={idx} type="text" placeholder={`UID ${idx + 1}`} value={uid} onChange={(e) => {
                        const n = [...targetUids]; n[idx] = e.target.value; setTargetUids(n);
                      }} />
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
                  {logs.length === 0 ? <div className="log empty">Awaiting commands...</div> : logs.map((log, idx) => (
                    <div key={idx} className={`log ${log.type}`}><span className="time">[{log.time}]</span> {log.msg}</div>
                  ))}
                </div>
              </div>
            </div>

            {/* Group Invite Panel */}
            <div className="group-invite-panel glass-panel">
              <h2 className="panel-title">👥 Group Invite</h2>
              <div className="group-invite-inner">
                <div className="input-group" style={{flex: 1, minWidth: '200px'}}>
                  <label>Target UID <span className="optional">(Group Invite Target)</span></label>
                  <input
                    type="text"
                    placeholder="Enter Target UID"
                    value={targetUids[0]}
                    onChange={(e) => { const n = [...targetUids]; n[0] = e.target.value; setTargetUids(n); }}
                  />
                </div>
                <div className="group-btn-wrap">
                  <label style={{fontSize:'0.85rem', color:'var(--text-muted)', marginBottom:'0.5rem', display:'block'}}>Select Group Size</label>
                  <div className="grid-buttons">
                    {[3, 4, 5, 6].map(num => (
                      <button
                        key={num}
                        className="num-btn"
                        onClick={() => sendGroupInvite(num)}
                        disabled={loadingAction !== null}
                        title={`Send ${num}-player group invite`}
                      >
                        {loadingAction === `group-${num}` ? '...' : `/${num}`}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <section className="emotes-section">
              <h2 className="section-title">Available Emotes <span className="badge">{EMOTES.length}</span></h2>
              <div className="emotes-grid">
                {EMOTES.map(emote => (
                  <div key={emote.id} className="emote-card glass-panel">
                    <div className="emote-icon">
                      <img src={`https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/${emote.id}.png`} alt={emote.label} />
                    </div>
                    <div className="emote-info"><h3>{emote.label}</h3><p>ID: {emote.id}</p></div>
                    <button className={`send-btn ${loadingEmote === emote.name ? 'loading' : ''}`} onClick={() => sendEmote(emote)} disabled={loadingEmote !== null}>
                      {loadingEmote === emote.name ? 'Sending...' : 'Send Emote'}
                    </button>
                  </div>
                ))}
              </div>
            </section>
          </div>
        ) : (
          <div className="menu-content">
            {!isLevelUpUnlocked ? (
              <div className="unlock-screen glass-panel">
                <div className="lock-icon">🔒</div>
                <h2>Level Up Bot Locked</h2>
                <p>Please enter the GitHub-protected password to access this feature.</p>
                <form onSubmit={handleLevelUpLogin}>
                  <input 
                    type="password" 
                    placeholder="Enter Level-Up Password" 
                    value={levelUpPass} 
                    onChange={(e) => setLevelUpPass(e.target.value)}
                  />
                  {levelUpError && <p className="error-msg">{levelUpError}</p>}
                  <button type="submit" disabled={loadingAction === 'unlock'}>
                    {loadingAction === 'unlock' ? 'Verifying...' : 'Unlock Features'}
                  </button>
                </form>
              </div>
            ) : (
              <div className="levelup-dashboard">
                <div className="stats-grid">
                  <div className="stat-card glass-panel">
                    <span className="stat-label">Active Bot</span>
                    <span className="stat-value">{matchStats.bot_uid || 'None'}</span>
                  </div>
                  <div className="stat-card glass-panel">
                    <span className="stat-label">Games Played</span>
                    <span className="stat-value">{matchStats.games_played}</span>
                  </div>
                  <div className="stat-card glass-panel">
                    <span className="stat-label">Total Runtime</span>
                    <span className="stat-value">{formatRuntime(matchStats.runtime)}</span>
                  </div>
                  <div className="stat-card glass-panel">
                    <span className="stat-label">Status</span>
                    <span className={`stat-value ${matchStats.running ? 'online' : 'offline'}`}>
                      {matchStats.running ? 'RUNNING' : 'STOPPED'}
                    </span>
                  </div>
                </div>

                <div className="main-content">
                  <div className="control-panel glass-panel">
                    <h2 className="panel-title">Match Bot Controls</h2>
                    <div className="input-group">
                      <label>Auto-Start Team Code</label>
                      <input 
                        type="text" 
                        placeholder="Enter 8-digit Code" 
                        value={teamCode} 
                        onChange={(e) => setTeamCode(e.target.value)} 
                        disabled={matchStats.running}
                      />
                    </div>
                    <div className="button-row">
                      {!matchStats.running ? (
                        <button className="action-btn start" onClick={() => handleAutoStart('start')} disabled={loadingAction !== null}>
                          {loadingAction === 'auto-start' ? 'Starting...' : 'Start Match Bot'}
                        </button>
                      ) : (
                        <button className="action-btn stop" onClick={() => handleAutoStart('stop')} disabled={loadingAction !== null}>
                          {loadingAction === 'auto-stop' ? 'Stopping...' : 'Stop Match Bot'}
                        </button>
                      )}
                    </div>
                  </div>

                  <div className="terminal-panel glass-panel">
                    <div className="terminal-header">
                      <div className="dots"><span></span><span></span><span></span></div>
                      <span className="terminal-title">Level Up Logs</span>
                    </div>
                    <div className="terminal-body">
                      {matchStats.running ? (
                        <div className="log success">⚡ Bot is currently farming on {matchStats.team_code}...</div>
                      ) : (
                        <div className="log empty">System idle. Waiting for start...</div>
                      )}
                      {logs.filter(l => l.msg.includes('Match Bot')).map((log, idx) => (
                        <div key={idx} className={`log ${log.type}`}><span className="time">[{log.time}]</span> {log.msg}</div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
