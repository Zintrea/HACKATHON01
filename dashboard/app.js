const data = window.H1_DASHBOARD_DATA;

const fmt = (n) => typeof n === 'number' ? n.toLocaleString() : n;
const pct = (value, max) => max ? Math.max(2, Math.round((value / max) * 100)) : 0;

function renderOverview() {
  const o = data.overview;
  const total5xx = (o.status_counts['500'] || 0) + (o.status_counts['504'] || 0);
  const cards = [
    ['Parsed lines', fmt(o.parsed_lines), 'Raw log rows processed'],
    ['Suspicious IPs', fmt(o.suspicious_ips), 'High-confidence group'],
    ['Server errors', fmt(total5xx), '500 + 504 responses'],
    ['Suffix clue', o.suffix_sequence, 'Ordered endpoint suffixes'],
    ['Malformed', fmt(o.malformed_lines), 'Rows skipped safely'],
  ];
  document.getElementById('overview').innerHTML = cards.map(([label, value, note]) => `
    <article class="card"><div class="label">${label}</div><div class="value">${value}</div><div class="label">${note}</div></article>
  `).join('');
}

function renderAttackers() {
  const maxScore = Math.max(...data.attackers.map(a => a.score));
  document.getElementById('attackers').innerHTML = `
    <table><thead><tr><th>#</th><th>IP</th><th>Score</th><th>500s</th><th>Total Req</th><th>Reasons</th></tr></thead><tbody>
    ${data.attackers.map((a, i) => `
      <tr>
        <td>${i + 1}</td><td><code>${a.ip}</code></td>
        <td>${fmt(a.score)}<div class="bar"><span style="width:${pct(a.score, maxScore)}%"></span></div></td>
        <td>${fmt(a.status_500)}</td><td>${fmt(a.total_requests)}</td><td>${a.reasons}</td>
      </tr>`).join('')}
    </tbody></table>`;
}

function statusLine(label, value, max, tone='') {
  return `<div class="status-row"><span>${label}</span><div class="bar"><span style="width:${pct(value, max)}%; background:${tone || ''}"></span></div><b>${fmt(value)}</b></div>`;
}

function renderEndpointComparison() {
  const pairs = [['/cart','/cart_'], ['/search','/search_'], ['/products','/products_'], ['/checkout','/checkout_'], ['/api/v1/user','/api/v1/user_'], ['/index.html','/index_.html']];
  const byEp = Object.fromEntries(data.endpoints.map(e => [e.endpoint, e]));
  document.getElementById('endpoint-comparison').innerHTML = `<div class="endpoint-grid">${pairs.map(([normal, variant]) => {
    const n = byEp[normal], v = byEp[variant];
    if (!n || !v) return '';
    const max = Math.max(n.total_requests, v.total_requests, n.status_200, n.status_404, v.status_5xx);
    return `<div class="endpoint-card">
      <h3><code>${normal}</code> vs <code>${variant}</code></h3>
      <p class="label">Normal endpoint has user traffic; variant endpoint is almost pure 5xx.</p>
      <h4>${normal}</h4>
      ${statusLine('200', n.status_200, max, 'var(--ok)')}
      ${statusLine('304', n.status_304, max, 'var(--accent)')}
      ${statusLine('404', n.status_404, max, 'var(--warning)')}
      ${statusLine('5xx', n.status_5xx, max, 'var(--danger)')}
      <h4>${variant}</h4>
      ${statusLine('500', v.status_500, max, 'var(--danger)')}
      ${statusLine('504', v.status_504, max, 'var(--danger)')}
      ${statusLine('5xx', v.status_5xx, max, 'var(--danger)')}
    </div>`;
  }).join('')}</div>`;
}

function renderSuffixes() {
  document.getElementById('suffix-sequence').textContent = data.overview.suffix_sequence;
  const max = Math.max(...data.suffixes.map(s => s.total_5xx));
  document.getElementById('suffix-table').innerHTML = `
    <table><thead><tr><th>Order</th><th>Suffix</th><th>Total 5xx</th><th>Endpoint Count</th><th>Examples</th></tr></thead><tbody>
      ${data.suffixes.map((s, i) => `<tr>
        <td>${i + 1}</td><td><code>${s.suffix}</code></td>
        <td>${fmt(s.total_5xx)}<div class="bar"><span style="width:${pct(s.total_5xx, max)}%"></span></div></td>
        <td>${s.endpoint_count}</td><td><code>${String(s.examples).split(';').slice(0,4).join('</code>, <code>')}</code></td>
      </tr>`).join('')}
    </tbody></table>`;
}

function renderIncidents() {
  document.getElementById('incidents').innerHTML = `
    <table><thead><tr><th>#</th><th>Start</th><th>End</th><th>State</th><th>Peak 5xx/min</th><th>Reason</th></tr></thead><tbody>
      ${data.incidents.slice(0, 25).map((w, i) => `<tr>
        <td>${i + 1}</td><td>${w.start_time}</td><td>${w.end_time}</td><td>${w.states_seen}</td><td>${fmt(w.peak_5xx)}</td><td>${w.reason}</td>
      </tr>`).join('')}
    </tbody></table>`;
}

function renderEvidence() {
  document.getElementById('evidence').innerHTML = `
    <table><thead><tr><th>Line</th><th>Time</th><th>IP</th><th>Endpoint</th><th>Status</th><th>Reasons</th></tr></thead><tbody>
      ${data.evidence.slice(0, 30).map(e => `<tr>
        <td>${e.line_number}</td><td>${e.timestamp}</td><td><code>${e.ip}</code></td><td><code>${e.endpoint}</code></td><td>${e.status}</td><td>${e.reasons}</td>
      </tr>`).join('')}
    </tbody></table>`;
}

renderOverview();
renderAttackers();
renderEndpointComparison();
renderSuffixes();
renderIncidents();
renderEvidence();
