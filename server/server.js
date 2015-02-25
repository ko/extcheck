var app = require('express')()
var http = require('http').Server(app)
var io = require('socket.io')(http)

var fs = require('fs')

app.get('/', function(req,res) {
    var out = fs.readdirSync('/')
    res.send(out)
})

io.on('connection', function(socket) {

    socket.on('ls', function(msg) {
        console.log('ls!')
        console.log(msg)
    })
})

http.listen(3000)
