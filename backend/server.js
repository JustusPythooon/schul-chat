
const express = require('express')
const app = express()
const http = require('http').createServer(app)
const io = require('socket.io')(http,{cors:{origin:'*'}})
io.on('connection',(s)=>{s.on('msg',(m)=>io.emit('msg',m))})
http.listen(3000,()=>console.log('Server läuft'))
