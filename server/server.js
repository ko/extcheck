var express = require('express')
var fs = require('fs')

var app = express()

app.get('/', function(req,res) {
    var out = fs.readdirSync('/')
    res.send(out)
})

app.listen(3000)
