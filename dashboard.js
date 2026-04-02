// dashboard.js

async function loadBugsFromCSV() {
  try {
    const response = await fetch('bugs.csv');
    const csvText = await response.text();

    const rows = csvText.trim().split('\n');
    const tbody = document.querySelector('#bugsTable tbody');
    tbody.innerHTML = '';

    rows.forEach(row => {
      const [id, ...rest] = row.split(':');
      const description = rest.join(':').trim();

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${id.trim()}</td>
        <td>${description}</td>
      `;
      tbody.appendChild(tr);
    });

    $('#bugsTable').DataTable({
      paging: true,
      searching: true,
      info: true,
      order: [[0, 'desc']]
    });

  } catch (error) {
    console.error('Error loading bugs CSV:', error);
  }
}

async function loadCSV(file) {
  const response = await fetch(file + '?t=' + new Date().getTime());
  const text = await response.text();
  return Papa.parse(text, { header: true }).data.filter(r => Object.values(r).some(v => v));
}

async function initDashboard() {
  await loadBugsFromCSV();

  const issues = await loadCSV('dateClosevsNew.csv');

  const issuesBody = document.getElementById('issuesBody');
  issuesBody.innerHTML = '';

  issues.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${r.date}</td><td>${r.new}</td><td>${r.closed}</td>`;
    issuesBody.appendChild(tr);
  });

  const totalNew = issues.reduce((sum, r) => sum + parseInt(r.new || 0), 0);
  const totalClosed = issues.reduce((sum, r) => sum + parseInt(r.closed || 0), 0);
  document.getElementById('closedIssuesCount').textContent = totalClosed;
  document.getElementById('openIssuesCount').textContent = totalNew - totalClosed;

  const ctx = document.getElementById('issuesChart');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: issues.map(r => r.date),
      datasets: [
        { label: 'New Issues', data: issues.map(r => parseInt(r.new || 0)), borderColor: '#d69d2f', backgroundColor: 'rgba(214,157,47,0.08)', tension: 0.4, fill: true },
        { label: 'Closed Issues', data: issues.map(r => parseInt(r.closed || 0)), borderColor: '#2f8e3c', backgroundColor: 'rgba(47,142,60,0.08)', tension: 0.4, fill: true }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
  });

  $('#issuesTable').DataTable({ paging: false, info: false, searching: false, order: [[0, 'desc']] });

  const pending = await loadCSV('pending.csv');
  const pendEl = document.getElementById('pendingList');
  pendEl.innerHTML = '';
  pending.forEach(p => {
    const li = document.createElement('li');
    li.textContent = p.item;
    pendEl.appendChild(li);
  });

  const features = await loadCSV('feature.csv');
  const featEl = document.getElementById('featureRelease');
  featEl.innerHTML = '';
  features.forEach(p => {
    const li = document.createElement('li');
    li.textContent = p.feature;
    featEl.appendChild(li);
  });
}

initDashboard();
