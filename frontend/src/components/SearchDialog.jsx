import React, { useState } from 'react';
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
import AdminService from '../services/api.js';

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

export default function SearchDialog(props) {

    const [open, setOpen] = React.useState(false);
    const [openSnackbar, setOpenSnackbar] = React.useState(false);

    const [startUrls, setStartUrls] = useState('');
    const [keywords, setKeywords] = useState('');
    const [cycles, setCycles] = useState(0);
    const [uuid, setUUID] = useState('');

    const classes = useStyles();

    const handleClickOpen = () => {
        setStartUrls('');
        setKeywords('');
        setCycles(0);
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleStart = () => {
        setOpen(false);
        setCrawl();
    };

    const setCrawl = () => {
        var data = {};
        data['urls'] = startUrls.split(',');
        data['step'] = 0;
        data['totalsteps'] = cycles;
        data['keywords'] = keywords.split(',');
        data['parent'] = null;

        AdminService.getCrawl(data)
        .then(
            response => {
                if (response.data.status_code !== 200) {
                    console.error(response.data.message);
                } else {
                    setUUID(response.data.data.worker_id);
                    setOpenSnackbar(true);
                }
            }
        )
        .catch(
            error => {
                console.error(error.response.data.message);
                if (error.response.data.status_code === 401)
                    window.location.replace('/login');
            }
        );
    }

    const handleChangeStartUrls = (event) => {
        setStartUrls(event.target.value);
    }

    const handleChangeKeywords = (event) => {
        setKeywords(event.target.value);
    }

    const handleChangeCycles = (event) => {
        setCycles(event.target.value);
    }

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
                            value={startUrls}
                            onChange={handleChangeStartUrls}
                        />
                        <TextField
                            autoFocus
                            margin="dense"
                            id="keywords"
                            label="Parole chiave"
                            type="text"
                            value={keywords}
                            onChange={handleChangeKeywords}
                        />
                    </div>
                    <div>
                        <TextField
                            autoFocus
                            margin="dense"
                            id="cycles"
                            label="Numero di cicli"
                            type="number"
                            value={cycles}
                            onChange={handleChangeCycles}
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