async function loadModule(moduleName) {
  const res = await fetch(`/api/${moduleName}`);
  const data = await res.json();
  const table = document.getElementById('data-table');
  if (!Array.isArray(data) || data.length === 0) {
    table.innerHTML = '<tr><td>Sem dados</td></tr>';
    return;
  }
  const headers = Object.keys(data[0]);
  table.innerHTML = '<tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr>' +
    data.map(row => '<tr>' + headers.map(h => `<td>${row[h]}</td>`).join('') + '</tr>').join('');
}
