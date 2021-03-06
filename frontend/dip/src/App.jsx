import React, { Component } from 'react';
import EvidenceTable from './components/EvidenceTable'
import DipAppBar from './components/DipAppBar'
import Login from './components/Login';
import OrgChartTree from './components/TreeChart'

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
        {/* <Login></Login> */}
        <EvidenceTable evidences={posts}></EvidenceTable>
        {/* <OrgChartTree></OrgChartTree> */}
      </div>
    );
  }
}
export default App;
