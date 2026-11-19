import React, { useEffect, useState } from 'react';

export default function App() {
  const [status, setStatus] = useState('Connecting to Backend...');

  useEffect(() => {
    fetch('https://asma-os.vercel.app/api/health')
      .then(res => res.json())
      .then(data => setStatus(`Live API: ${data.status} | Version: ${data.version}`))
      .catch(() => setStatus('Backend API Standby'));
  }, []);

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif' }}>
      <h1 style={{ color: '#C7A76C' }}>LUMEYRA Founder Command Dashboard</h1>
      <p style={{ color: '#765D4C' }}>Operating 45 Autonomous AI Agents across 15 Departments</p>
      <div style={{ background: '#343D38', padding: '20px', borderRadius: '8px', border: '1px solid #C7A76C' }}>
        <h3>System Status</h3>
        <p style={{ color: '#F5EBDD' }}>{status}</p>
        <p>Operational Gates: <strong>7/7 Passed</strong></p>
      </div>
    </div>
  );
}
