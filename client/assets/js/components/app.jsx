var React = require('react')
var Router = require('react-router');

var ReactBootstrap = require('react-bootstrap');
var Navbar = require('react-bootstrap').Navbar;
var Nav = require('react-bootstrap').Nav;
var NavItem = require('react-bootstrap').NavItem;

var Link = Router.Link;


var App = React.createClass({

    getInitialState: function() {
        return null
    },

    render : function(){

        var layout;

        layout = <Router.RouteHandler />;

        return (
            <div>
                <div className="app-container">
                    {layout}
                </div>
            </div>
        );
    }
})

module.exports = App
