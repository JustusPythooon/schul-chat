
const socket = io();
let room='';
function join(r){room=r;document.getElementById('chat').innerHTML='';socket.emit('join',r)}
function send(){const i=document.getElementById('msg');socket.emit('send',{room,text:i.value});i.value=''}
socket.on('message',m=>{const d=document.createElement('div');d.innerText=m.user+': '+m.text;document.getElementById('chat').appendChild(d)})
