import React, { useState } from 'react';
import Tree from 'react-d3-tree';
import { Container } from '@material-ui/core';
import { useCenteredTree } from "./helpers";
import '../assets/nodes.css'
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
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
    },
    textOneLine: {
        whiteSpace: 'nowrap',
        overflow: 'hidden'
    }
}));

const containerStyles = {
    width: "100vw",
    height: "100vh"
};

const renderForeignObjectNode = ({
    nodeDatum,
    toggleNode,
    foreignObjectProps,
    handleClickOpen,
    classes
}) => {
 return   (
        <g>
            <circle r={15}></circle>
            <foreignObject {...foreignObjectProps}>
                <Card style={{ maxWidth: 345 }}>
                    <CardActionArea>
                        <CardContent>
                            <h2 className={classes.textOneLine}>{nodeDatum.name}</h2>
                            {nodeDatum.attributes.step && <p className={classes.textOneLine}>Ciclo: {nodeDatum.attributes.step}</p>}
                            {nodeDatum.attributes.keywords_found && <p className={classes.textOneLine}>Parole chiave trovate: {nodeDatum.attributes.keywords_found}</p>}
                        </CardContent>
                    </CardActionArea>
                    <CardActions>
                        <Grid item container justify="space-between">
                            <Grid item>
                                <Button size="small" color="primary">Espandi</Button>
                            </Grid>
                            <Grid item>
                                <Button size="small" color="primary" onClick={(e) => handleClickOpen(e, nodeDatum)}>Riprendi da qui</Button>
                            </Grid>
                        </Grid>
                    </CardActions>
                </Card>
            </foreignObject>
        </g>
    )
};

export default function TreeChart(props) {
    const [translate, containerRef] = useCenteredTree();
    const nodeSize = { x: 400, y: 200 };
    const foreignObjectProps = { width: nodeSize.x, height: nodeSize.y, x: -100, className: "node-custom" };
    const data = props.data;
    const [open, setOpen] = React.useState(false);
    const [openSnackbar, setOpenSnackbar] = React.useState(false);

    const [startUrls, setStartUrls] = useState('');
    const [keywords, setKeywords] = useState('');
    const [cycles, setCycles] = useState(0);
    const [parent, setParent] = useState('');
    const [step, setStep] = useState(0);
    const classes = useStyles();

    const handleClickOpen = (event, nodeData) => {
        setStartUrls(nodeData.attributes.urls_queryable + "");
        setKeywords(nodeData.attributes.keywords + "");
        setCycles(0);
        setStep(nodeData.attributes.step);
        setParent(nodeData.attributes.parent);
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleStart = () => {
        setOpen(false);
        var node = {};
        node['urls'] = startUrls.split(',');
        node['step'] = step;
        node['totalsteps'] = cycles;
        node['keywords'] = keywords.split(',');
        node['parent'] = parent;
        setCrawl(node);
    };

    const setCrawl = (node) => {
        AdminService.getCrawl(node)
        .then(
            response => {
                if (response.data.status_code !== 200) {
                    console.error(response.data.message);
                } else {
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

    const handleChangeCycles = (event) => {
        setCycles(event.target.value);
    }

    const handleCloseSnackbar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setOpenSnackbar(false);
    };
    if (null !== data) {
        return (
            <div>
                <Container maxWidth="xl" style={containerStyles} ref={containerRef}>
                    <Tree
                        data={data}
                        translate={translate}
                        nodeSize={nodeSize}
                        renderCustomNodeElement={(rd3tProps) =>
                            renderForeignObjectNode({ ...rd3tProps, foreignObjectProps, handleClickOpen, classes })
                        }
                        orientation="vertical"
                    />
                </Container>
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
                                disabled={true}
                            />
                            <TextField
                                autoFocus
                                margin="dense"
                                id="keywords"
                                label="Parole chiave"
                                type="text"
                                value={keywords}
                                disabled={true}
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

    return (
        <div>Non ci sono risultati</div>
    )
}