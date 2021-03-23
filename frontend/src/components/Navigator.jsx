import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import {BrowserRouter as Router, Link as RouterLink, Route, Switch} from 'react-router-dom'
import NavMenu from './NavMenu';
import Routes from '../Routes.js';

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

export default function Navigator() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Router>
        <AppBar position="fixed">
          <Toolbar>
              <NavMenu></NavMenu>
              {/* <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                <MenuIcon />
              </IconButton> */}
              <Typography variant="h6" className={classes.title}>
                TOLOMEO
              </Typography>
              <Button color="inherit" component={RouterLink} to="/login">Login</Button>
          </Toolbar>
          <div className={classes.offset} />
        </AppBar>
        <Toolbar>{/* content */}</Toolbar>
        <Routes />
      </Router>
    </div>
  );
}