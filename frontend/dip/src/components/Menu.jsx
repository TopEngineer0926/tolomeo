import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import {BrowserRouter as Router, Link as RouterLink, Route, Switch} from 'react-router-dom'
import EvidenceTable from './EvidenceTable'
import Login from './Login';
import EvidenceChart from './EvidenceChart';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

export default function Menu() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Router>
        <AppBar position="fixed">
          <Toolbar>
              <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" className={classes.title}>
                TOLOMEO
              </Typography>
              <Button color="inherit" component={RouterLink} to="/login">Login</Button>
          </Toolbar>
          <div className={classes.offset} />
        </AppBar>
        <Toolbar>{/* content */}</Toolbar>
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
          <Route path="/">
            Questo è l'ingresso dell'applicazione, effettua il login in alto a destra! {/*Define a home page */}
          </Route>
        </Switch>
      </Router>
    </div>
  );
}