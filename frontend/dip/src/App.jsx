import React, { Component } from 'react';
import EvidenceTable from './components/EvidenceTable'
import DipAppBar from './components/DipAppBar'
import Login from './components/Login';
import EvidenceChart from './components/EvidenceChart';
import {BrowserRouter, Route, Switch} from 'react-router-dom'

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
        {/* <EvidenceTable evidences={posts}></EvidenceTable> */}
        {/* <EvidenceChart></EvidenceChart> */}
      </div>
    );
  }
}
export default App;
