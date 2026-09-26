async function json(url, options){const r=await fetch(url,options);return r.json()}
async function loadDevices(){const d=await json('/api/devices');document.querySelector('#devices').textContent=JSON.stringify(d,null,2)}
async function shell(){const command=document.querySelector('#command').value;const d=await json('/api/adb/shell',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({command})});document.querySelector('#output').textContent=JSON.stringify(d,null,2)}
async function scan(){const f=document.querySelector('#apk').files[0];if(!f)return;const fd=new FormData();fd.append('file',f);const d=await json('/api/security/scan',{method:'POST',body:fd});document.querySelector('#scan').textContent=JSON.stringify(d,null,2)}
json('/api/health').then(d=>{document.querySelector('#state').textContent=d.ok?'Сервер работает':'Ошибка'});loadDevices();
