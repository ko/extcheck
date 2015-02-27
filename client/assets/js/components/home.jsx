var React = require('react')
var io = require('socket.io-client').connect('http://localhost:3000');
var socket = io.connect();

var FileEntry = React.createClass({

    render: function() {
        return (
            <li onClick={this.props.onClick}>
                <b>
                    {this.props.direntry}
                </b>
            </li>
        )
    }
})

var Home = React.createClass({

    getInitialState: function() {

        socket.on('ls:return', this.lsReturn) 
        socket.on('browse:return', this.browseReturn)

        this.initialize()

        return { 
            dirPath:        '/', 
            dirContents:    [[]], 
            dirNames:       [], 
            filePath:       '/' 
        }
    },

    basename: function(input) {
        return input.split(/\.[^.]+$/)[0];
    },

    initialize: function() {

        this.ls('')
    },

    ls: function(filename) {
        var basepath = ''

        if (this.state && this.state.filePath) {
            basepath = this.state.filePath
        }
        socket.emit('ls', basepath + '/' + filename)
    },

    lsReturn: function(msg) {
        if (msg.isDir) {
            var dirContents = this.state.dirContents

            console.log(dirContents[0].length)

            if (dirContents[0].length == 0) {
                dirContents = [ msg.filenames ]
            } else {
                dirContents.push(msg.filenames)
            }

            console.log(dirContents)

            this.setState({ dirContents: dirContents })
        }
    },

    browseReturn: function(msg) {
        console.log('browseReturn: ' + msg.filename)

        if (msg.isDir) {
            var newDirpath = msg.filename

            console.log('browseReturn: ' + newDirpath)
            
            var newDirnames = this.state.dirNames
            console.log('newDirnames: '  + newDirnames)
            console.log('adding name: ' + this.basename(msg.filename))
            newDirnames.push(this.basename(msg.filename))

            this.setState({ dirNames: newDirnames })
            this.setState({ dirPath: newDirpath })
            this.ls(newDirpath)
        }
    },

    onFileClick: function(dirIdx, fileIdx) {

        var newPath = ''

        if (this.state.dirPath) {
            newPath = this.state.dirPath
        }
        if (newPath === '/') {
            newPath = ''
        }
        newPath +=  '/' + this.state.dirContents[dirIdx][fileIdx]

        socket.emit('browse', newPath)
    },

    render : function(){

        var dirIdx = 0

        console.log(this.state.dirNames)

        return (
            /*
            {this.state.dirNames.map(function(dir, dirIdx) {
            */
                <ul>
                    {this.state.dirContents[dirIdx].map(function(result, fileIdx) {
                        return <FileEntry onClick={this.onFileClick.bind(this,dirIdx,fileIdx)} key={fileIdx} direntry={result} />
                    }, this)}
                </ul>
            /*
            }, this)}
            */
        );
    }

})

module.exports = Home
