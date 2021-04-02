import { useState } from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Paper from '@material-ui/core/Paper';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import { useHistory } from 'react-router-dom'
import AdminService from '../services/api.js';
function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        TOLOMEO
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const useStyles = makeStyles((theme) => ({
  root: {
    height: '100vh',
  },
  image: {
    backgroundImage: 'url(https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.criminologia.it%2Fimages%2Flogo-criminologia-new-2.jpg&f=1&nofb=1)',
    backgroundRepeat: 'no-repeat',
    backgroundColor: 'white',
    backgroundSize: '50%',
    backgroundPosition: 'center',
  },
  paper: {
    margin: theme.spacing(8, 4),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  error: {
    color: 'red'
  }
}));
const validEmailRegex = RegExp(/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i);
const validateForm = (errors) => {
  let valid = true;
  Object.values(errors).forEach(
    (val) => val.length > 0 && (valid = false)
  );
  return valid;
}
export default function Login() {
  const classes = useStyles();
  const history = useHistory();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorsEmail, setErrorsEmail] = useState('');
  const [errorsPassword, setErrorsPassword] = useState('');

  document.onkeydown = function (e) {
    if (e.keyCode === 13) {
      if (document.getElementById('login')) {
        handleLogin();
      }
    }
  }

  const handleChangeEmail = (event) => {
    event.preventDefault();
    let errorsMail =
      validEmailRegex.test(event.target.value)
        ? ''
        : "L'email non è valida!";
    setEmail(event.target.value);
    setErrorsEmail(errorsMail);
  }
  const handleChangePassword = (event) => {
    event.preventDefault();
    let errorsPass =
      event.target.value.length === 0
        ? ''
        : '';
    setPassword(event.target.value);
    setErrorsPassword(errorsPass);
  }

  const handleLogin = () => {
    let cnt = 0;
    if (email.length === 0) { setErrorsEmail('Per favore inserisci la tua email!'); cnt++; }
    if (password.length === 0) { setErrorsPassword('Per favore inserisci LA TUA password!'); cnt++; }
    if (cnt === 0) {
      if (validateForm(errorsEmail)) {
        /* Perform login and then navigate to evidences or home */
        var data = {};
        data['email'] = email;
        data['password'] = password;
        AdminService.login(data)
          .then(
            response => {
              if (response.data.status_code !== 200) {
                console.error(response.data.message);
              } else {
                localStorage.setItem("token", JSON.stringify(response.data.data.token));
                history.push("/evidences");
              }
            },
            error => {
              console.error("Can't connect to the Server!");
            }
          );
      }
      else setErrorsEmail('Email is not valid!');
    }
  };

  return (
    <Grid container component="main" className={classes.root}>
      <CssBaseline />
      <Grid item xs={false} sm={4} md={7} className={classes.image} />
      <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
        <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Log in
          </Typography>
          <form className={classes.form} noValidate>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={handleChangeEmail}
            />
            {errorsEmail.length > 0 &&
              <span className={classes.error}>{errorsEmail}</span>}
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={handleChangePassword}
            />
            {errorsPassword.length > 0 &&
              <span className={classes.error}>{errorsPassword}</span>}
            {/* <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Ricordati di me"
            /> */}
            <Button
              fullWidth
              variant="contained"
              color="primary"
              id="login"
              className={classes.submit}
              onClick={handleLogin}
            >
              Log in
            </Button>
            <Box mt={5}>
              <Copyright />
            </Box>
          </form>
        </div>
      </Grid>
    </Grid>
  );
}