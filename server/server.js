var app = require('express')()
var http = require('http').Server(app)
var io = require('socket.io')(http)

var fs = require('fs')

app.get('/', function(req,res) {
    var out = fs.readdirSync('/')
    res.send(out)
})

io.on('connection', function(socket) {

    socket.on('ls', function(filepath) {

        var out = []
        var isDir = fs.statSync(filepath).isDirectory()

        if (isDir) {
            out = fs.readdirSync(filepath)
        }

        console.log(out)

        socket.emit('ls:return', { isDir: isDir,  filenames: out })
    })

    socket.on('browse', function(filepath) {
        
        var out = []
        var isDir = fs.statSync(filepath).isDirectory()

        socket.emit('browse:return', { isDir: isDir, filename: filepath })
    })
})

http.listen(3000)
