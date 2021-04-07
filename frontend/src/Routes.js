import React from 'react';
import { Switch, Route, Redirect} from 'react-router-dom';
import EvidenceTable from './components/EvidenceTable'
import EvidenceChart from './components/EvidenceChart';
import Login from './components/Login';
import NotFound from './components/NotFound';
import Dashboard from './components/Dashboard';

const Routes = () => {
    return (
        <Switch>
            <Route path="/evidences">
                <EvidenceTable></EvidenceTable>
            </Route>
            <Route path="/map">
                <EvidenceChart></EvidenceChart>
            </Route>
            <Route path="/login">
                <Login></Login>
            </Route>
            <Route exact path="/">
                <Dashboard></Dashboard>
            </Route>
            <Route path="/not-found">
                <NotFound />
            </Route>
            <Redirect to="/not-found" />
        </Switch>
    );
};

export default Routes;
