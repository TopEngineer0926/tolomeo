import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Grid, Typography } from '@material-ui/core';
const useStyles = makeStyles(theme => ({
  root: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    display: 'flex',
    justifyContent: 'center',
    marginTop: 100
  },
  content: {
    textAlign: 'center',
  },
  image: {
    display: 'inline-block',
    maxWidth: '100%',
  },
  main: {
      width: '70%'
  }
}));

const Dashboard = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
        <Grid container justify="center" alignItems="center" className={classes.main}>
          <Grid item className={classes.content}>
            <Typography variant="h4">
              Progetto delle cattedre di Informatica-Intelligenza Artificiale (Prof. Michele Laurelli); Criminologia (Prof. Saverio Fortunato),
              per la realizzazione di un software dotato di Intelligenza Artificiale in grado di mappare il dark web risalendo ai traffici illeciti dei singoli siti "oscuri" e ai criminali.
              Software che sarà donato gratuitamente alla Procura della Repubblica di Vibo Valentia
            </Typography>
          </Grid>
          <Grid item>
            <img
              alt="Under development"
              className={classes.image}
              src="/images/landing.jpeg"
            />
          </Grid>
        </Grid>
    </div>
  );
};

export default Dashboard;
