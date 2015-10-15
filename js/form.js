var React = require('react');
var ReactDOM = require('react-dom');


var Entry = React.createClass({
  handleLogin: function() {

  },

  render: function() {
    return (
      <form>
      Building: <input type='text' name='building'/>
      Room: <input type='text' name='room'/>
      Day:  <select>
              <option value="m">Monday</option>
              <option value="tu">Tuesday</option>
              <option value="w">Wednesday</option>
              <option value="th">Thursday</option>
              <option value="f">Friday</option>
            </select>
      Time: <input type='text' name='time'/>
      <button onClick={this.handleLogin} type='button'>Submit</button>
      </form>
    )
  }
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
