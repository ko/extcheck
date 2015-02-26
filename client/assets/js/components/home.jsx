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

        return { dircontents: [], dirpath: '', filepath: ''}
    },

    initialize: function() {
        this.setState({ dirpath: '/' })
        this.setState({ filepath: '/' })
        this.ls('')
    },

    ls: function(filename) {
        var basepath = ''

        if (this.state && this.state.filepath) {
            basepath = this.state.filepath
        }
        socket.emit('ls', basepath + '/' + filename)
    },

    lsReturn: function(msg) {
        if (msg.isDir) {
            this.setState({ dircontents: msg.filenames })
        }
    },

    browseReturn: function(msg) {
        console.log('browseReturn: ' + msg.filename)

        if (msg.isDir) {
            var newDirpath = msg.filename

            this.setState({ dirpath: newDirpath })
            this.ls(newDirpath)
        }
    },

    onFileClick: function(i) {

        var newPath = ''

        if (this.state.dirpath) {
            newPath = this.state.dirpath
        }
        if (newPath === '/') {
            newPath = ''
        }
        newPath +=  '/' + this.state.dircontents[i]

        socket.emit('browse', newPath)
    },

    render : function(){

        return (
            <ul>
                {this.state.dircontents.map(function(result, i) {
                    return <FileEntry onClick={this.onFileClick.bind(this,i)} key={i} direntry={result} />
                }, this)}
            </ul>
        );
    }

})

module.exports = Home
