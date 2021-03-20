import React, { Component } from 'react';
import Navigator from './components/Navigator'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: []
    }
  }

  render() {
    return (
      <div>
        <Navigator />
      </div>
    );
  }
}
export default App;
