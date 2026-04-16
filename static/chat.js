
const socket = io();
function send(){
  const i = document.getElementById('msg');
  socket.emit('message', i.value);
  i.value = '';
}
socket.on('message', d => {
  const div = document.createElement('div');
  div.innerText = d.user + ': ' + d.text;
  document.getElementById('chat').appendChild(div);
});
