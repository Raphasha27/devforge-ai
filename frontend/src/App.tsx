import { useState, useEffect } from "react";

const GITHUB_USER = "Raphasha27";
const API_BASE = "http://localhost:8000";

export default function App() {
  const [trends, setTrends] = useState<string[]>([]);
  const [status, setStatus] = useState<string>("System Idle");
  const [logs, setLogs] = useState<any[]>([]);
  const [evolution, setEvolution] = useState<any[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [pending, setPending] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [sentiment, setSentiment] = useState<any>(null);
  const [performance, setPerformance] = useState<any>(null);
  const [quota, setQuota] = useState<any>(null);
  const [markets, setMarkets] = useState<any[]>([]);
  const [memory, setMemory] = useState<any>(null);
  const [directive, setDirective] = useState("");
  const [graphData, setGraphData] = useState<{nodes: any[], links: any[]}>({nodes: [], links: []});
  const [strategy, setStrategy] = useState<any>(null);
  const [projects, setProjects] = useState<any[]>([]);
  const [isExecuting, setIsExecuting] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const trendRes = await fetch(`${API_BASE}/trending`);
        const trendData = await trendRes.json();
        setTrends(trendData.signals || []);

        const projectRes = await fetch(`${API_BASE}/projects/${GITHUB_USER}`);
        const projectData = await projectRes.json();
        if (projectData.data?.user?.projectsV2?.nodes) {
          setProjects(projectData.data.user.projectsV2.nodes);
        }

        const collabRes = await fetch(`${API_BASE}/collaboration`);
        const collabData = await collabRes.json();
        setMessages(collabData.messages || []);

        const pendingRes = await fetch(`${API_BASE}/governance/pending`);
        const pendingData = await pendingRes.json();
        setPending(pendingData.pending || []);

        const eventRes = await fetch(`${API_BASE}/events`);
        const eventData = await eventRes.json();
        setEvents(eventData.events || []);

        const sentimentRes = await fetch(`${API_BASE}/market-sentiment`);
        const sentimentData = await sentimentRes.json();
        setSentiment(sentimentData);

        const perfRes = await fetch(`${API_BASE}/performance`);
        const perfData = await perfRes.json();
        setPerformance(perfData);

        const quotaRes = await fetch(`${API_BASE}/quota`);
        const quotaData = await quotaRes.json();
        setQuota(quotaData);

        const marketRes = await fetch(`${API_BASE}/ecosystem/markets`);
        const marketData = await marketRes.json();
        setMarkets(marketData || []);

        const memoryRes = await fetch(`${API_BASE}/neural-memory`);
        const memoryData = await memoryRes.json();
        setMemory(memoryData);

        const graphRes = await fetch(`${API_BASE}/ecosystem/graph`);
        const graphData = await graphRes.json();
        setGraphData(graphData);
      } catch (err) {
        console.error("Failed to sync with DevForge Core:", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); 
    return () => clearInterval(interval);
  }, []);

  const approveAction = async (id: number) => {
    await fetch(`${API_BASE}/governance/approve/${id}`, { method: "POST" });
    setPending(prev => prev.filter(p => p.id !== id));
    setStatus("Action Approved");
  };

  const sendDirective = async () => {
    if (!directive) return;
    await fetch(`${API_BASE}/swarm/directive`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ directive })
    });
    setDirective("");
    setStatus("Directive Delegated");
  };

  const runCycle = async () => {
    if (isExecuting) return;
    setIsExecuting(true);
    setStatus("Analyzing Ecosystem...");
    
    try {
      const res = await fetch(`${API_BASE}/company-cycle`, { method: "POST" });
      const data = await res.json();
      
      setStrategy(data.strategy);
      setLogs(prev => [...(data.results || []), ...prev]);
      setEvolution(data.evolution || []);
      setStatus("Cycle Synchronized");
      
      if (data.roadmap) {
        await fetch(`${API_BASE}/projects/sync/${GITHUB_USER}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data.roadmap)
        });
      }
    } catch (err) {
      setStatus("Cycle Failed");
    } finally {
      setIsExecuting(false);
      setTimeout(() => setStatus("System Idle"), 3000);
    }
  };

  return (
    <div style={{ position: 'relative', minHeight: '100vh', padding: 'inherit' }}>
      <div className="grid-overlay" />
      <div className="scanline-overlay" />

      {/* Status Marquee */}
      <div style={{ 
        background: 'var(--bg-card)', borderBottom: '1px solid var(--border-neon)', 
        padding: '0.5rem', marginBottom: '2rem', overflow: 'hidden', whiteSpace: 'nowrap' 
      }}>
        <div className="neon-text" style={{ display: 'inline-block', animation: 'marquee 30s linear infinite', fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.1rem' }}>
          CORE STATUS: OPERATIONAL | POLICIES: STRICT_TYPESCRIPT=ON, AUTO_FIX_SECURITY=ON | SYSTEM HEALTH: 98% | ACTIVE REPOS: {graphData.nodes.length} | PENDING MUTATIONS: {pending.length}
        </div>
      </div>

      {/* Header Section */}
      <header style={{ 
        display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end',
        borderBottom: '1px solid var(--border-dim)', paddingBottom: '1.5rem', marginBottom: '3rem'
      }}>
        <div>
          <h1 className="wide-tracking" style={{ fontSize: '2.5rem', fontWeight: 700 }}>
            DevForge <span className="neon-text">Core</span>
          </h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            Autonomous OS Product Studio | Governance v12.5
          </p>
          <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.5rem' }}>
            <input 
              type="text" 
              placeholder="ENTER CEO DIRECTIVE..."
              value={directive}
              onChange={(e) => setDirective(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendDirective()}
              style={{ 
                background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-neon)',
                color: 'var(--text-primary)', padding: '0.8rem 1.2rem', borderRadius: '4px',
                width: '400px', fontSize: '0.8rem', fontFamily: 'monospace'
              }}
            />
            <button onClick={sendDirective} style={{ background: 'var(--neon-green)', color: '#000', border: 'none', padding: '0 1.5rem', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer', fontSize: '0.7rem' }}>DELEGATE</button>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '3rem', alignItems: 'center' }}>
          {sentiment && (
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>MARKET VIBE</div>
              <div style={{ 
                color: sentiment.sentiment_score > 70 ? 'var(--neon-green)' : sentiment.sentiment_score > 40 ? 'var(--neon-blue)' : '#FF4B4B',
                fontWeight: 'bold', fontSize: '1.2rem'
              }}>
                {sentiment.vibe.toUpperCase()} ({sentiment.sentiment_score}%)
              </div>
            </div>
          )}
          {quota && (
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>API QUOTA</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ width: '60px', height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
                  <div style={{ width: `${quota.percent}%`, height: '100%', background: quota.percent > 80 ? '#FF4B4B' : 'var(--neon-green)' }} />
                </div>
                <span style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>{quota.percent}%</span>
              </div>
              <div style={{ fontSize: '0.6rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>${quota.spend} / ${quota.budget}</div>
            </div>
          )}
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>SYSTEM STATUS</div>
            <div className="neon-text" style={{ fontWeight: 'bold' }}>
              ● {status.toUpperCase()}
            </div>
          </div>
        </div>
      </header>

      {/* Visual Dependency Map */}
      <section className="glass-card" style={{ padding: '2rem', marginBottom: '3rem', minHeight: '300px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <h2 className="wide-tracking" style={{ fontSize: '0.9rem', marginBottom: '2rem', color: 'var(--text-secondary)', width: '100%' }}>Ecosystem Architecture</h2>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '2rem', justifyContent: 'center', alignItems: 'center' }}>
          {graphData.nodes.length > 0 ? graphData.nodes.map(node => (
            <div key={node.id} style={{ 
              width: '120px', height: '120px', borderRadius: '50%', border: '1px solid var(--border-neon)',
              display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center',
              padding: '1rem', fontSize: '0.7rem', fontWeight: 'bold', background: 'var(--bg-card)',
              boxShadow: '0 0 15px rgba(0, 255, 156, 0.1)'
            }}>
              {node.id}
            </div>
          )) : (
            <div style={{ color: 'var(--text-secondary)' }}>Neural graph offline. Awaiting ecosystem signal...</div>
          )}
        </div>
      </section>

      <div className="dashboard-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 3fr', gap: '2rem' }}>
        {/* Sidebar Controls */}
        <aside style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          {performance && (
            <section className="glass-card" style={{ padding: '1.5rem', borderLeft: '4px solid var(--neon-blue)' }}>
              <h2 className="wide-tracking" style={{ fontSize: '0.9rem', marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>Company Performance</h2>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <div style={{ fontSize: '0.6rem', color: 'var(--text-secondary)' }}>EST. MRR</div>
                  <div className="neon-text" style={{ fontSize: '1.1rem', fontWeight: 'bold' }}>${performance.estimated_mrr}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.6rem', color: 'var(--text-secondary)' }}>LAUNCHES</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 'bold' }}>{performance.total_launches}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.6rem', color: 'var(--text-secondary)' }}>REJECTIONS</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#FF4B4B' }}>{performance.security_rejections}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.6rem', color: 'var(--text-secondary)' }}>REFAC. IMPACT</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: 'var(--neon-blue)' }}>+{performance.refactor_impact}</div>
                </div>
              </div>
            </section>
          )}

          <section className="glass-card" style={{ padding: '1.5rem', borderLeft: '4px solid var(--neon-green)' }}>
            <h2 className="wide-tracking" style={{ fontSize: '0.9rem', marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>Blue Ocean Opportunities</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
              {markets.length > 0 ? markets.map(m => (
                <div key={m.name} style={{ fontSize: '0.8rem', padding: '0.8rem', background: 'rgba(0, 255, 156, 0.05)', border: '1px solid var(--border-neon)', borderRadius: '4px' }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '0.3rem' }}>{m.name}</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.7rem', marginBottom: '0.5rem' }}>{m.gap}</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ flex: 1, height: '3px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px' }}>
                      <div style={{ width: `${m.dominance_potential}%`, height: '100%', background: 'var(--neon-green)' }} />
                    </div>
                    <span style={{ fontSize: '0.6rem' }}>{m.dominance_potential}%</span>
                  </div>
                </div>
              )) : (
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', textAlign: 'center' }}>Scanning for market gaps...</p>
              )}
            </div>
          </section>

          <section className="glass-card" style={{ padding: '1.5rem' }}>
            <h2 className="wide-tracking" style={{ fontSize: '0.9rem', marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>Market Intelligence</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
              {trends.map(s => (
                <div key={s} style={{ 
                  fontSize: '0.85rem', padding: '0.8rem', background: 'rgba(255,255,255,0.03)', 
                  border: '1px solid var(--border-dim)', borderRadius: '4px' 
                }}>
                  <span className="neon-text" style={{ marginRight: '0.5rem' }}>📡</span> {s}
                </div>
              ))}
            </div>
          </section>

          <section className="glass-card" style={{ padding: '1.5rem' }}>
            <h2 className="wide-tracking" style={{ fontSize: '0.9rem', marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>Active Projects</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
              {projects.length > 0 ? projects.map(p => (
                <a key={p.id} href={p.url} target="_blank" rel="noreferrer" style={{ 
                  textDecoration: 'none', color: 'var(--text-primary)', fontSize: '0.85rem',
                  padding: '0.8rem', background: 'rgba(0, 255, 156, 0.05)', border: '1px solid var(--border-neon)',
                  borderRadius: '4px', display: 'flex', alignItems: 'center'
                }}>
                  <span style={{ marginRight: '0.8rem' }}>📋</span> {p.title}
                </a>
              )) : (
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', textAlign: 'center' }}>No remote projects found</p>
              )}
            </div>
          </section>

          {memory && memory.success_patterns && (
            <section className="glass-card" style={{ padding: '1.5rem', borderLeft: '4px solid var(--neon-blue)', boxShadow: '0 0 15px rgba(0, 163, 255, 0.1)' }}>
              <h2 className="wide-tracking" style={{ fontSize: '0.9rem', marginBottom: '1.5rem', color: 'var(--neon-blue)' }}>Neural Intelligence Layer</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                {memory.success_patterns.slice(-3).map((p: any, idx: number) => (
                  <div key={idx} style={{ fontSize: '0.7rem', padding: '0.8rem', background: 'rgba(0, 163, 255, 0.05)', border: '1px solid rgba(0, 163, 255, 0.2)', borderRadius: '4px' }}>
                    <div style={{ color: 'var(--neon-blue)', fontWeight: 'bold', marginBottom: '0.2rem' }}>PATTERN_DETECTED_{idx}</div>
                    <div style={{ color: '#aaa' }}>{p.action}: {p.repo}</div>
                  </div>
                ))}
                <div style={{ fontSize: '0.65rem', textAlign: 'center', color: '#666', marginTop: '0.5rem' }}>ACTIVE PATTERNS: {memory.success_patterns.length}</div>
              </div>
            </section>
          )}

          <section className="glass-card" style={{ padding: '1.5rem' }}>
            <h2 className="wide-tracking" style={{ fontSize: '0.9rem', marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>Ecosystem Evolution</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
              {evolution.length > 0 ? evolution.map(e => (
                <div key={e.repo} style={{ fontSize: '0.8rem', padding: '0.8rem', background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-dim)', borderRadius: '4px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ fontWeight: 'bold' }}>{e.repo}</span>
                    <span style={{ 
                      fontSize: '0.6rem', padding: '2px 6px', borderRadius: '10px', 
                      background: e.stage === 'mature' ? 'var(--neon-green)' : e.stage === 'scaling' ? 'var(--neon-blue)' : 'rgba(255,255,255,0.1)',
                      color: e.stage === 'mature' ? '#000' : '#fff', textTransform: 'uppercase'
                    }}>
                      {e.stage}
                    </span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ color: e.action === 'maintain' ? 'var(--text-secondary)' : 'var(--neon-blue)', textTransform: 'uppercase', fontSize: '0.7rem' }}>{e.action}</span>
                  </div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.75rem' }}>{e.plan}</div>
                </div>
              )) : (
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', textAlign: 'center' }}>Waiting for next audit...</p>
              )}
            </div>
          </section>

          <section className="glass-card" style={{ padding: '1.5rem', flex: 1, display: 'flex', flexDirection: 'column', maxHeight: '400px' }}>
            <h2 className="wide-tracking" style={{ fontSize: '0.9rem', marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>Collaboration Hub</h2>
            <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem', paddingRight: '0.5rem' }} className="scrollbar-hide">
              {messages.length > 0 ? messages.map(m => (
                <div key={m.id} style={{ fontSize: '0.8rem', borderLeft: '2px solid var(--border-dim)', paddingLeft: '0.8rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.2rem' }}>
                    <span>{m.emoji}</span>
                    <span style={{ fontWeight: 'bold', color: 'var(--neon-green)' }}>{m.actor}</span>
                    <span style={{ fontSize: '0.65rem', color: 'var(--text-secondary)' }}>{m.timestamp}</span>
                  </div>
                  <div style={{ color: 'var(--text-primary)', lineHeight: '1.4' }}>{m.text}</div>
                </div>
              )) : (
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', textAlign: 'center' }}>No internal comms intercepted.</p>
              )}
            </div>
          </section>

          <button 
            onClick={runCycle}
            disabled={isExecuting}
            style={{ 
              width: '100%', padding: '1.2rem', background: isExecuting ? 'transparent' : 'var(--neon-green)', 
              color: isExecuting ? 'var(--neon-green)' : '#0d1117', border: `2px solid var(--neon-green)`,
              borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer', transition: 'all 0.3s ease',
              boxShadow: isExecuting ? 'none' : '0 0 20px rgba(0, 255, 156, 0.2)'
            }}
          >
            {isExecuting ? "EXECUTING..." : "TRIGGER BUSINESS CYCLE"}
          </button>
        </aside>

        {/* Main Feed */}
        <main style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          {strategy && (
            <section className="glass-card" style={{ padding: '2rem', borderLeft: '4px solid var(--neon-green)' }}>
              <h2 className="neon-text wide-tracking" style={{ fontSize: '1.1rem', marginBottom: '1.5rem' }}>CEO Strategic Directive</h2>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                <div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>CORE FOCUS</div>
                  <div style={{ fontSize: '0.9rem' }}>{strategy.focus_areas.join(" • ")}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>RISK ASSESSMENT</div>
                  <div style={{ fontSize: '0.9rem' }}>{strategy.risk_assessment}</div>
                </div>
              </div>
            </section>
          )}

          {/* Viral Growth Campaigns */}
          {events.filter(e => e.type === 'growth_campaign_launched').length > 0 && (
            <section className="glass-card" style={{ padding: '2rem', borderLeft: '4px solid #FF00E5' }}>
              <h2 className="wide-tracking" style={{ fontSize: '1.1rem', marginBottom: '1.5rem', color: '#FF00E5' }}>Viral Growth Engine</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {events.filter(e => e.type === 'growth_campaign_launched').map((e, idx) => (
                  <div key={idx} style={{ background: 'rgba(255,0,229,0.05)', padding: '1.2rem', borderRadius: '8px', border: '1px solid rgba(255,0,229,0.2)' }}>
                    <div style={{ fontSize: '1rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>{e.payload.repo}</div>
                    <div style={{ fontSize: '0.9rem', color: '#FF00E5', marginBottom: '0.8rem', fontStyle: 'italic' }}>"{e.payload.campaign.tagline}"</div>
                    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                      {e.payload.campaign.seo_keywords.map((k: string) => (
                        <span key={k} style={{ fontSize: '0.7rem', color: '#aaa', border: '1px solid #444', padding: '2px 8px', borderRadius: '4px' }}>#{k}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {pending.length > 0 && (
            <section className="glass-card" style={{ padding: '2rem', borderLeft: '4px solid var(--neon-blue)' }}>
              <h2 className="wide-tracking" style={{ fontSize: '1.1rem', marginBottom: '1.5rem', color: 'var(--neon-blue)' }}>Governance Approval Queue</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {pending.map(p => (
                  <div key={p.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(255,255,255,0.03)', padding: '1.2rem', borderRadius: '8px', border: '1px solid var(--border-dim)' }}>
                    <div>
                      <div style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>{p.repo}</div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.3rem' }}>{p.suggestion}</div>
                    </div>
                    <div style={{ display: 'flex', gap: '0.8rem' }}>
                      <button onClick={() => approveAction(p.id)} style={{ background: 'var(--neon-blue)', color: '#0d1117', border: 'none', padding: '6px 12px', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer', fontSize: '0.75rem' }}>APPROVE</button>
                      <button style={{ background: 'transparent', color: 'var(--text-secondary)', border: '1px solid var(--border-dim)', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem' }}>REJECT</button>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          <section className="glass-card" style={{ padding: '1.5rem', background: '#000', border: '1px solid #333' }}>
            <h2 className="wide-tracking" style={{ fontSize: '0.9rem', marginBottom: '1rem', color: '#666' }}>System Activity Console</h2>
            <div style={{ height: '200px', overflowY: 'auto', fontFamily: 'monospace', fontSize: '0.8rem', display: 'flex', flexDirection: 'column-reverse' }} className="scrollbar-hide">
              {events.length > 0 ? events.map(e => (
                <div key={e.id} style={{ marginBottom: '0.4rem', display: 'flex', gap: '1rem' }}>
                  <span style={{ color: '#444' }}>[{new Date(e.timestamp).toLocaleTimeString()}]</span>
                  <span style={{ color: 'var(--neon-green)' }}>{e.type.toUpperCase()}</span>
                  <span style={{ color: '#aaa' }}>{e.payload.repo || 'System'}</span>
                  <span style={{ color: '#666' }}>→ {JSON.stringify(e.payload.intelligence?.tech_stack || e.payload.action || '')}</span>
                </div>
              )) : (
                <div style={{ color: '#444' }}>Initializing stream...</div>
              )}
            </div>
          </section>

          <section>
            <h2 className="wide-tracking" style={{ fontSize: '1.1rem', marginBottom: '1.5rem' }}>Engineering Pipeline</h2>
            {logs.length === 0 ? (
              <div className="glass-card" style={{ padding: '4rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                Waiting for mission start...
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {logs.map((log, i) => (
                  <div key={i} className="glass-card" style={{ padding: '1.5rem', animation: 'fadeIn 0.5s ease backwards' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                      <h3 className="neon-text" style={{ fontSize: '1.2rem' }}>{log.product.product_name}</h3>
                      <span style={{ fontSize: '0.7rem', background: 'rgba(0, 255, 156, 0.1)', color: 'var(--neon-green)', padding: '4px 8px', borderRadius: '4px' }}>
                        QUALITY SCORE: {log.score}%
                      </span>
                    </div>
                    <p style={{ fontSize: '0.95rem', color: 'var(--text-primary)', marginBottom: '1.2rem' }}>{log.product.value_proposition}</p>
                    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                      {log.files_generated.map((f: string) => (
                        <span key={f} style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', background: 'rgba(255,255,255,0.05)', padding: '2px 8px', borderRadius: '2px', border: '1px solid var(--border-dim)' }}>
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </main>
      </div>
    </div>
  );
}
