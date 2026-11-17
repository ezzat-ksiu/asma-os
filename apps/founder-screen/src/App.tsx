import { useCallback, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Activity, ArrowDownToLine, BookOpen, Check, ChevronRight, CircleDollarSign, Clock3, Fingerprint, LockKeyhole, LogIn, RefreshCw, ShieldCheck, WalletCards } from 'lucide-react';

type Dashboard = {
  pending_print_approvals?: Array<{ id: string; title: string; requested_at?: string; proof_status?: string }>;
  sla?: { uptime_percentage?: number; target_percentage?: number; status?: string };
  financial_ledger?: { revenue?: number; expenses?: number; net?: number; currency?: string; projected_arr?: number };
  artifacts?: Array<{ id: string; title: string; sha256?: string; status?: string }>;
};

const apiBase = (import.meta.env.VITE_ASMA_API_URL as string | undefined)?.replace(/\/$/, '');
const money = (value?: number, currency = 'USD') => typeof value === 'number' ? new Intl.NumberFormat(undefined, { style: 'currency', currency, maximumFractionDigits: 0 }).format(value) : '—';

export default function App() {
  const auth = useAuth0();
  const [data, setData] = useState<Dashboard | null>(null);
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState<string | null>(null);
  const configured = Boolean(apiBase && import.meta.env.VITE_AUTH0_DOMAIN && import.meta.env.VITE_AUTH0_CLIENT_ID);

  const load = useCallback(async () => {
    if (!configured || !auth.isAuthenticated) return;
    try {
      const token = await auth.getAccessTokenSilently();
      const response = await fetch(`${apiBase}/v1/founder/dashboard`, { headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' } });
      if (!response.ok) throw new Error(`Dashboard request failed (${response.status})`);
      setData(await response.json()); setMessage('');
    } catch (error) { setMessage(error instanceof Error ? error.message : 'Unable to load dashboard.'); }
  }, [auth.isAuthenticated, auth.getAccessTokenSilently, configured]);

  useEffect(() => { void load(); }, [load]);

  const signOff = async (artifactId: string) => {
    if (!apiBase || !artifactId) return;
    setBusy(artifactId); setMessage('');
    try {
      const token = await auth.getAccessTokenSilently();
      const response = await fetch(`${apiBase}/v1/artifacts/${encodeURIComponent(artifactId)}/sign-off`, {
        method: 'POST', headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json',
          'Idempotency-Key': `founder-sign-off:${artifactId}` }, body: JSON.stringify({ action: 'sha256_sign_off' }),
      });
      if (!response.ok) throw new Error(`Sign-off request failed (${response.status})`);
      const proof = await response.json();
      setMessage(`Artifact signed. SHA-256: ${proof.sha256 ?? 'recorded by server'} · Certificate: ${proof.certificate_id ?? 'issued'}`);
      await load();
    } catch (error) { setMessage(error instanceof Error ? error.message : 'Sign-off could not be completed.'); }
    finally { setBusy(null); }
  };

  const logout = () => auth.logout({ logoutParams: { returnTo: window.location.origin } });
  if (!configured) return <main className="setup"><div className="setup-card"><div className="brand-mark">A</div><p className="eyebrow">ASMA-OS · PRIVATE OPERATIONS</p><h1>Founder Console</h1><p>Configure <code>VITE_ASMA_API_URL</code>, <code>VITE_AUTH0_DOMAIN</code>, and <code>VITE_AUTH0_CLIENT_ID</code> to connect the authenticated production dashboard.</p><p className="muted">No sample metrics are displayed while the API is disconnected.</p></div></main>;
  if (auth.isLoading) return <main className="setup"><RefreshCw className="spin"/> Loading secure session…</main>;
  if (!auth.isAuthenticated) return <main className="setup"><div className="setup-card"><div className="brand-mark">A</div><p className="eyebrow">ASMA-OS · PRIVATE OPERATIONS</p><h1>Founder Console</h1><p>Sign in with your authorized founder account to review live operational records.</p><button className="primary" onClick={() => auth.loginWithRedirect()}><LogIn size={17}/> Sign in securely</button></div></main>;

  const approvals = data?.pending_print_approvals ?? [];
  const artifacts = data?.artifacts ?? [];
  const sla = data?.sla;
  const ledger = data?.financial_ledger;
  return <div className="app-shell"><aside className="sidebar"><div className="wordmark"><span className="brand-mark small">A</span><span>ASMA<span className="cyan">·</span>OS</span></div><div className="nav-label">WORKSPACE</div><a className="nav-item active"><Activity size={17}/> Overview</a><a className="nav-item"><BookOpen size={17}/> Print approvals</a><a className="nav-item"><WalletCards size={17}/> Financial ledger</a><a className="nav-item"><ShieldCheck size={17}/> Audit & security</a><div className="sidebar-bottom"><div className="live-tag"><i/> API connected</div><button className="nav-item logout" onClick={logout}><LockKeyhole size={16}/> Sign out</button></div></aside>
    <main className="main"><header className="topbar"><div><div className="eyebrow">OPERATIONS / OVERVIEW</div><h1>Good to see you.</h1></div><div className="top-actions"><span className="secure"><ShieldCheck size={15}/> Authenticated</span><button className="icon-button" aria-label="Refresh dashboard" onClick={() => void load()}><RefreshCw size={17}/></button><button className="avatar" aria-label="Sign out" onClick={logout}>{auth.user?.name?.[0]?.toUpperCase() ?? 'F'}</button></div></header>
      {message && <div className="notice" role="status">{message}</div>}
      {auth.error && <div className="notice error">Secure session error: {auth.error.message}</div>}
      {!data && !message && <div className="notice"><RefreshCw className="spin" size={16}/> Fetching live dashboard records…</div>}
      <section className="metrics"><Metric icon={<Activity/>} label="Service availability" value={sla ? `${sla.uptime_percentage?.toFixed(3)}%` : '—'} foot={sla?.status ?? 'No live SLA data'} good={sla?.status === 'COMPLIANT'}/><Metric icon={<CircleDollarSign/>} label="Ledger revenue" value={money(ledger?.revenue, ledger?.currency)} foot={ledger ? `Net ${money(ledger.net, ledger.currency)}` : 'No ledger data'} /><Metric icon={<ArrowDownToLine/>} label="Projected ARR" value={money(ledger?.projected_arr, ledger?.currency)} foot="From connected financial ledger"/><Metric icon={<Clock3/>} label="Awaiting approval" value={String(approvals.length)} foot="Print jobs requiring review"/></section>
      <section className="content-grid"><article className="panel"><div className="panel-heading"><div><p className="eyebrow">PRODUCTION</p><h2>Print approvals</h2></div><span className="count">{approvals.length} pending</span></div>{approvals.length ? <div className="rows">{approvals.map(item=><div className="approval-row" key={item.id}><div className="book-icon"><BookOpen size={18}/></div><div className="row-copy"><strong>{item.title}</strong><span>{item.id} · {item.requested_at ?? 'Request date unavailable'}</span></div><span className="status-pill">{item.proof_status ?? 'Needs review'}</span><ChevronRight size={17} className="muted"/></div>)}</div> : <Empty icon={<Check/>} text={data ? 'No print approvals are currently pending.' : 'Approval records will appear when the API is connected.'}/>}</article>
        <article className="panel"><div className="panel-heading"><div><p className="eyebrow">FINANCE</p><h2>Ledger summary</h2></div><WalletCards className="panel-icon"/></div><div className="ledger-lines"><LedgerLine label="Recognized revenue" value={money(ledger?.revenue, ledger?.currency)}/><LedgerLine label="Recorded expenses" value={money(ledger?.expenses, ledger?.currency)}/><LedgerLine label="Net balance" value={money(ledger?.net, ledger?.currency)} strong/></div><p className="panel-foot">Values reflect the authenticated API response.</p></article></section>
      <section className="panel artifacts"><div className="panel-heading"><div><p className="eyebrow">PROVENANCE</p><h2>Artifact sign-off</h2></div><Fingerprint className="panel-icon"/></div><p className="section-copy">Request a server-side SHA-256 fingerprint and cryptographic sign-off. Private signing keys remain in the protected backend.</p>{artifacts.length ? <div className="rows">{artifacts.map(item=><div className="approval-row" key={item.id}><div className="book-icon cyan-bg"><Fingerprint size={18}/></div><div className="row-copy"><strong>{item.title}</strong><span className="hash">{item.sha256 ?? `Artifact ${item.id}`} · {item.status ?? 'Ready for sign-off'}</span></div><button className="sign-button" disabled={busy===item.id} onClick={()=>void signOff(item.id)}>{busy===item.id?<RefreshCw size={15} className="spin"/>:<Fingerprint size={15}/>} {busy===item.id?'Signing…':'Sign off'}</button></div>)}</div> : <Empty icon={<Fingerprint/>} text={data ? 'No artifacts are currently available for sign-off.' : 'Artifact records will appear when available.'}/>}</section>
      <footer className="footer"><span>ASMA-OS · Secure founder operations</span><span><LockKeyhole size={13}/> Protected session</span></footer>
    </main></div>;
}

function Metric({icon,label,value,foot,good}:{icon:ReactNode;label:string;value:string;foot:string;good?:boolean}){return <article className="metric-card"><div className="metric-top"><span>{label}</span><span className="metric-icon">{icon}</span></div><strong>{value}</strong><small className={good?'good':''}>{foot}</small></article>}
function LedgerLine({label,value,strong}:{label:string;value:string;strong?:boolean}){return <div className={strong?'ledger-line total':'ledger-line'}><span>{label}</span><strong>{value}</strong></div>}
function Empty({icon,text}:{icon:ReactNode;text:string}){return <div className="empty"><span>{icon}</span><p>{text}</p></div>}
