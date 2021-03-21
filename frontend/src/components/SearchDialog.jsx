import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

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

    const [rendered, setRendered] = React.useState('rendered');

    const handleChange = (event) => {
        setRendered(event.target.value);
    };

    const [open, setOpen] = React.useState(false);

    const classes = useStyles();

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    return (
        <div>
        <Button variant="outlined" color="primary" onClick={handleClickOpen}>
            Avvia Scraper
        </Button>
        <Dialog className={classes.root} open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
            <DialogTitle id="form-dialog-title">Scraper</DialogTitle>
            <DialogContent>
            <DialogContentText>
                Per lanciare lo scraper bisogna inserire una url di partenza, delle parole chiave divise da ',', numero di cicli.
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
                <FormControl className={classes.formControl}>
                    <InputLabel id="demo-simple-select-label">Modalità</InputLabel>
                    <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={rendered}
                    onChange={handleChange}
                    >
                        <MenuItem value={"rendered"}>Renderizzato</MenuItem>
                        <MenuItem value={"skeleton"}>Solo codice sorgente</MenuItem>
                    </Select>
                </FormControl>
            </div>
            
            
            </DialogContent>
            <DialogActions>
            <Button onClick={handleClose} color="primary">
                Ritorna
            </Button>
            <Button onClick={handleClose} color="primary">
                Avvia
            </Button>
            </DialogActions>
        </Dialog>
        </div>
    );
}