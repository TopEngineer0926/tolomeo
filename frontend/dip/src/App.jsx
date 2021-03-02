import React, { Component } from 'react';
import EvidenceTable from './components/EvidenceTable'
import DipAppBar from './components/DipAppBar'

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
        <DipAppBar />
        <EvidenceTable evidences={posts}></EvidenceTable>
      </div>
    );
  }
}
export default App;
