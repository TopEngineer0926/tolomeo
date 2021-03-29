import React from 'react';
import { Switch, Route, Redirect} from 'react-router-dom';
import EvidenceTable from './components/EvidenceTable'
import EvidenceChart from './components/EvidenceChart';
import Login from './components/Login';
import NotFound from './components/NotFound';

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
                Questo è l'ingresso dell'applicazione, effettua il login in alto a destra! {/*Define a home page */}
            </Route>
            <Route path="/not-found">
                <NotFound />
            </Route>
            <Redirect to="/not-found" />
        </Switch>
    );
};

export default Routes;
