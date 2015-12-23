import React from 'react';
import ReactDOM from 'react-dom';


var Clock = React.createClass({
  getInitialState() {
    return { time: 'start' };
  },
  getCurrentTime() {
    var ws = new WebSocket(this.props.url);
    ws.onmessage = function(event) {
      this.setState({ time: event.data });
    }.bind(this);
  },
  componentWillMount() {
    this.getCurrentTime();
  },

  render() {
    return <div>{this.state.time}</div>
  }
});

ReactDOM.render(<Clock url={'ws://localhost:8090/ws'} />, document.getElementById('main'));
