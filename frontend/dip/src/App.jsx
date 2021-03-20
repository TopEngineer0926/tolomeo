import React, { Component } from 'react';
import Menu from './components/Menu'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: []
    }
  }

  render() {
    const { posts } = this.state;
    return (
      <div>
        <Menu />
      </div>
    );
  }
}
export default App;
