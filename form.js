var React = require('react');
var ReactDOM = require('react-dom');


var Entry = React.createClass({
  
});

var Display = React.createClass({

});

var App = React.createClass({
  getInitialState: function() {
    return {found_class: false}
  },

  render: function() {
    if (this.state.found_class) {
      return <Display />
    } else {
      return <Entry />
    }
  }
});

var mountNode = document.getElementById('app');

ReactDOM.render(<App />, mountNode);
