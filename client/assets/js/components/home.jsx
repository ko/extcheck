var React = require('react')
var io = require('socket.io-client').connect('http://localhost:3000');
var socket = io.connect();


var Home = React.createClass({

    test: function() {
        if (window.File && window.FileReader && window.FileList && window.Blob) {
            // Great success! All the File APIs are supported.

            return "true"
        } else {
            alert('The File APIs are not fully supported in this browser.');
        }
    },

    tester: function(evt) {
        var files = evt.target.files;
        var output = []
        for (var i = 0, f; f = files[i]; i++) {
            output.push('<li><strong>', escape(f.name), '</strong></li>')
        }
        document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>'
    },

    render : function(){

        var output = this.test()

        socket.emit('ls', 'file!')

        return (
            <div>
                {output}
                <input type="file" id="files" name="files[]" multiple onChange={this.tester} />
                <output id="list"></output>
            </div>
        );
    }

})

module.exports = Home
