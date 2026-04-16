
const socket = io();
let room='global';
const me=document.body.dataset.user;

joinRoom('global');

function joinRoom(r){
  room=r;
  document.getElementById('messages').innerHTML='';
  socket.emit('join', r);
}

function createGroup(){
  const n=prompt('Gruppenname');
  if(n) joinRoom(n);
}

function send(){
  const i=document.getElementById('msg');
  const f=document.getElementById('file').files[0];
  if(!i.value && !f) return;
  if(f){
    const fd=new FormData();
    fd.append('file',f);
    fetch('/upload',{method:'POST',body:fd})
      .then(r=>r.json())
      .then(d=>socket.emit('message',{text:i.value,file:d.file,room}));
  }else{
    socket.emit('message',{text:i.value,room});
  }
  i.value=''; document.getElementById('file').value='';
}

socket.on('history', msgs=>msgs.forEach(render));
socket.on('message', render);
socket.on('delete', id=>{
  const el=document.getElementById(id);
  if(el) el.remove();
});

function render(d){
  const div=document.createElement('div');
  div.id=d.id; div.className='msg '+(d.user===me?'me':'other');
  let html='<b>'+d.user+'</b><br>';
  if(d.file){
    if(d.file.match(/\.(png|jpg|jpeg|gif)$/))
      html+=`<img src="/uploads/${d.file}" width=120>`;
    else
      html+=`<a href="/uploads/${d.file}" target="_blank">Datei</a>`;
  }
  if(d.text) html+='<div>'+d.text+'</div>';
  html+=`<button onclick="del('${d.id}')">🗑</button>`;
  div.innerHTML=html;
  document.getElementById('messages').appendChild(div);
  div.scrollIntoView({behavior:'smooth'});
}

function del(id){
  socket.emit('delete_message',{id,room});
}

function toggleTheme(){
  document.body.classList.toggle('dark');
  localStorage.setItem('theme',document.body.classList.contains('dark'));
}
if(localStorage.getItem('theme')==='true') document.body.classList.add('dark');
