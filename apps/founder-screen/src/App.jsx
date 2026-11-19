import React, { useEffect, useState } from 'react';
import './App.css';

const apiBase = import.meta.env.VITE_API_BASE_URL;

export default function App() {
  const [health, setHealth] = useState(null);
  const [connection, setConnection] = useState('NOT_CONFIGURED');

  useEffect(() => {
    if (!apiBase) return;
    const controller = new AbortController();
    fetch(`${apiBase.replace(/\/$/, '')}/api/health`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`API returned ${response.status}`);
        return response.json();
      })
      .then((data) => { setHealth(data); setConnection('CONNECTED'); })
      .catch((error) => {
        if (error.name !== 'AbortError') setConnection('UNAVAILABLE');
      });
    return () => controller.abort();
  }, []);

  const gateSummary = health
    ? `${health.gates_passed ?? 0} verified / ${health.gates_total ?? 'unknown'} total`
    : 'UNKNOWN';

  return (
    <main className="founder-shell">
      <header>
        <p className="eyebrow">ASMA-OS · PRIVATE OPERATIONS CONSOLE</p>
        <h1>FOLIAVERE — Founder workspace</h1>
        <p className="notice" role="status">Demo interface. Founder authentication and operational data are not configured; no actions are available.</p>
      </header>
      <section className="status-grid" aria-label="Operational status">
        <article><h2>API connection</h2><p>{connection}</p></article>
        <article><h2>System readiness</h2><p>{health?.readiness ?? 'UNKNOWN'}</p></article>
        <article><h2>Gate evidence</h2><p>{gateSummary}</p></article>
        <article><h2>Print approvals</h2><p>NOT CONFIGURED</p></article>
        <article><h2>Financial ledger</h2><p>NOT CONFIGURED</p></article>
        <article><h2>SLA measurements</h2><p>NOT CONFIGURED</p></article>
      </section>
      <footer>Provisional brand identity · No customer, payment, or production records are connected.</footer>
    </main>
  );
}
