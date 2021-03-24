import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { makeStyles } from '@material-ui/core/styles';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
  root: {
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
    width: '25ch',
  },
  margin: {
    margin: theme.spacing(1),
    width: "25ch"
  }
}));

export default function SearchDialog() {

    const [open, setOpen] = React.useState(false);
    const [openSnackbar, setOpenSnackbar] = React.useState(false);

    const classes = useStyles();

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleStart = () => {
        setOpen(false);
        setOpenSnackbar(true);
    };

    const handleCloseSnackbar = (event, reason) => {
        if (reason === 'clickaway') {
          return;
        }
    
        setOpenSnackbar(false);
      };

    return (
        <div>
        <Button variant="outlined" color="primary" onClick={handleClickOpen}>
            Avvia Programma
        </Button>
        <Dialog className={classes.root} open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
            <DialogTitle id="form-dialog-title">Scraper</DialogTitle>
            <DialogContent>
            <DialogContentText>
                Per lanciare lo scraper bisogna inserire una url di partenza, delle parole chiave divise da ',' e numero di cicli.
            </DialogContentText>
            <div>
                <TextField
                    autoFocus
                    margin="dense"
                    id="url"
                    label="Url di partenza"
                    type="text"
                />
                <TextField
                    autoFocus
                    margin="dense"
                    id="keywords"
                    label="Parole chiave"
                    type="text"
                />
            </div>
            <div>
                <TextField
                    autoFocus
                    margin="dense"
                    id="cycles"
                    label="Numero di cicli"
                    type="number"
                />
            </div>
            
            
            </DialogContent>
            <DialogActions>
            <Button onClick={handleClose} color="primary">
                Annulla
            </Button>
            <Button onClick={handleStart} color="primary">
                Avvia
            </Button>
            </DialogActions>
        </Dialog>
        <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="success">
            Programma avviato correttamente...
            </Alert>
        </Snackbar>
        </div>
    );
}