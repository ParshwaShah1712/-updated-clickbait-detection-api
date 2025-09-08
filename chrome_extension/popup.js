const DEFAULT_API = 'http://127.0.0.1:5000/predict_batch';

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('scan');
  const status = document.getElementById('status');
  const input = document.getElementById('apiBase');

  chrome.storage.sync.get(['apiBase'], (res) => {
    input.value = res.apiBase || DEFAULT_API;
  });

  input.addEventListener('change', () => {
    const val = input.value.trim() || DEFAULT_API;
    chrome.storage.sync.set({ apiBase: val });
  });

  btn.addEventListener('click', () => {
    status.textContent = 'Scanning...';
    chrome.runtime.sendMessage({ type: 'POPUP_SCAN_REQUEST' }, () => {
      status.textContent = 'Requested scan. Check panel on page.';
      window.close();
    });
  });
});


