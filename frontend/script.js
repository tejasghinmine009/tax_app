document.addEventListener('DOMContentLoaded', () => {
  const statusDiv = document.getElementById('health-status');
  statusDiv.textContent = 'Checking backend health...';
  fetch('http://localhost:8000/api/health')
    .then(res => res.json())
    .then(data => {
      if (data.status === 'ok') {
        statusDiv.textContent = 'Backend is online!';
        statusDiv.style.color = '#22c55e'; // green
      } else {
        statusDiv.textContent = 'Backend is not responding.';
        statusDiv.style.color = '#ef4444'; // red
      }
    })
    .catch(() => {
      statusDiv.textContent = 'Backend is not reachable.';
      statusDiv.style.color = '#ef4444'; // red
    });
}); 