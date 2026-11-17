import React, { useState, useEffect } from 'react';

export default function App() {
  const [gates, setGates] = useState([]);
  const [goal, setGoal] = useState('');
  const [planResult, setPlanResult] = useState(null);
  const [loadingPlan, setLoadingPlan] = useState(false);
  const [invoiceStatus, setInvoiceStatus] = useState('');

  const API_BASE = 'http://localhost:8000/api';

  useEffect(() => {
    fetch(`${API_BASE}/gates`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') setGates(data.gates);
      })
      .catch(() => {
        setGates([
          { gate_number: 1, gate_name: 'Autonomous Identity & Branding', status: 'active' },
          { gate_number: 2, gate_name: 'Product Storefront & Publishing', status: 'active' },
          { gate_number: 3, gate_name: 'Multi-Channel Distribution Engine', status: 'active' },
          { gate_number: 4, gate_name: 'Autonomous Operations & Treasury', status: 'active' },
          { gate_number: 5, gate_name: 'Real-time Founder Command OS', status: 'active' },
          { gate_number: 6, gate_name: 'Self-Healing AI Governance', status: 'active' }
        ]);
      });
  }, []);

  const handleGeneratePlan = async () => {
    if (!goal) return;
    setLoadingPlan(true);
    setPlanResult(null);
    try {
      const res = await fetch(`${API_BASE}/plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal, budget: 1500.0 })
      });
      const data = await res.json();
      setPlanResult(data.plan);
    } catch (err) {
      setPlanResult({ error: 'Failed to generate plan. Ensure API is online.' });
    } finally {
      setLoadingPlan(false);
    }
  };

  const handleCreateTestInvoice = async () => {
    setInvoiceStatus('Generating Invoice PDF...');
    try {
      const res = await fetch(`${API_BASE}/documents/invoice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_name: 'Enterprise Client',
          invoice_id: `INV-${Date.now().toString().slice(-6)}`,
          amount: 7500.0,
          currency: 'EGP',
          services: [{ name: 'ASMA-OS Autonomous Setup', qty: 1, price: 7500.0 }]
        })
      });
      const data = await res.json();
      if (data.status === 'success') {
        setInvoiceStatus(`✅ Generated PDF: ${data.pdf_path}`);
      } else {
        setInvoiceStatus('❌ Failed to generate PDF');
      }
    } catch (err) {
      setInvoiceStatus('❌ Error calling API');
    }
  };

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem', maxWidth: '1000px', margin: '0 auto', color: '#1e293b' }}>
      <header style={{ borderBottom: '2px solid #e2e8f0', pb: '1rem', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', color: '#0f172a', margin: 0 }}>ASMA-OS V6.0 Founder Command Center</h1>
        <p style={{ color: '#64748b', margin: '0.5rem 0 0' }}>Autonomous Operating System & Operational Gates Controller</p>
      </header>

      <section style={{ marginBottom: '2rem', background: '#f8fafc', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <h2 style={{ fontSize: '1.25rem', marginTop: 0 }}>🛡️ Operational Gates Status (6/6 Active)</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
          {gates.map((g) => (
            <div key={g.gate_number} style={{ background: '#fff', padding: '1rem', borderRadius: '6px', border: '1px solid #cbd5e1', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>Gate {g.gate_number}:</strong> {g.gate_name}
              </div>
              <span style={{ background: '#dcfce7', color: '#166534', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.85rem', fontWeight: 'bold' }}>
                {g.status}
              </span>
            </div>
          ))}
        </div>
      </section>

      <section style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
        <div style={{ background: '#fff', padding: '1.5rem', borderRadius: '8px', border: '1px solid #cbd5e1' }}>
          <h2 style={{ fontSize: '1.2rem', marginTop: 0 }}>🤖 DeepSeek AI Strategic Planner</h2>
          <input
            type="text"
            placeholder="e.g. Launch AI B2B SaaS platform in Egypt"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid #cbd5e1', marginBottom: '1rem', boxSizing: 'border-box' }}
          />
          <button
            onClick={handleGeneratePlan}
            disabled={loadingPlan}
            style={{ background: '#0284c7', color: '#fff', border: 'none', padding: '0.75rem 1.5rem', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', width: '100%' }}
          >
            {loadingPlan ? 'Analyzing Strategy...' : 'Generate Plan via DeepSeek AI'}
          </button>

          {planResult && (
            <pre style={{ background: '#0f172a', color: '#38bdf8', padding: '1rem', borderRadius: '6px', marginTop: '1rem', overflowX: 'auto', fontSize: '0.85rem' }}>
              {JSON.stringify(planResult, null, 2)}
            </pre>
          )}
        </div>

        <div style={{ background: '#fff', padding: '1.5rem', borderRadius: '8px', border: '1px solid #cbd5e1' }}>
          <h2 style={{ fontSize: '1.2rem', marginTop: 0 }}>📄 Typst Document & Payment Action</h2>
          <p style={{ fontSize: '0.9rem', color: '#64748b' }}>Generate official PDF invoice and initiate billing flow.</p>
          <button
            onClick={handleCreateTestInvoice}
            style={{ background: '#10b981', color: '#fff', border: 'none', padding: '0.75rem 1.5rem', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', width: '100%', marginTop: '1rem' }}
          >
            Generate Typst PDF Invoice
          </button>

          {invoiceStatus && (
            <p style={{ marginTop: '1rem', fontWeight: 'bold', fontSize: '0.9rem', wordBreak: 'break-all' }}>
              {invoiceStatus}
            </p>
          )}
        </div>
      </section>
    </div>
  );
}
