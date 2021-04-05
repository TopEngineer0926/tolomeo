import React, { useEffect, useState } from 'react';
import Tree from 'react-d3-tree';
import { Container } from '@material-ui/core';
import { useCenteredTree } from "./helpers";
import '../assets/nodes.css'
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
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
        overflow: 'hidden',
        textOverflow: 'ellipsis'
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
    handleClickPickUp,
    handleClickExpand,
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
                            {<p className={classes.textOneLine}>Ciclo: {nodeDatum.attributes.step}</p>}
                            {nodeDatum.attributes.keywords_found && <p className={classes.textOneLine}>Parole chiave trovate: {nodeDatum.attributes.keywords_found}</p>}
                            {nodeDatum.attributes.urls_queryable && <p className={classes.textOneLine}>Url trovate utilizzabili: {nodeDatum.attributes.urls_queryable}</p>}
                        </CardContent>
                    </CardActionArea>
                    <CardActions>
                        <Grid item container justify="space-between">
                            <Grid item>
                                <Button size="small" color="primary" onClick={(e) => handleClickExpand(e, nodeDatum)}>Espandi</Button>
                            </Grid>
                            <Grid item>
                                <Button size="small" color="primary" onClick={(e) => handleClickPickUp(e, nodeDatum)}
                                    style={{visibility: nodeDatum.attributes.urls_queryable && nodeDatum.attributes.urls_queryable.length > 0 ? 'visible' : 'hidden'}}
                                >
                                    Riprendi da qui
                                </Button>
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

    let items = props.data;
    const [data, setData] = useState(items);
    const limit = props.limit;
    const page = props.page;
    const [open, setOpen] = useState(false);
    const [openSnackbar, setOpenSnackbar] = useState(false);

    const [startUrls, setStartUrls] = useState('');
    const [keywords, setKeywords] = useState('');
    const [cycles, setCycles] = useState(0);
    const [parent, setParent] = useState('');
    const [step, setStep] = useState(0);
    const classes = useStyles();

    useEffect(() => {
        setData(items)
    }, [items]);

    const handleClickPickUp = (event, nodeData) => {
        setStartUrls(nodeData.attributes.urls_queryable + "");
        setKeywords(nodeData.attributes.keywords + "");
        setCycles(0);
        setStep(nodeData.attributes.step);
        setParent(nodeData.attributes.parent);
        setOpen(true);
    };

    const handleClickExpand = (event, nodeData) => {
        if (nodeData.attributes.uuid == null)
            return;
        AdminService.getExpandedCharts(limit, page, nodeData.attributes.uuid)
        .then(
            response => {
                if (response.data.status_code !== 200) {
                    console.error(response.data.message);
                } else {
                    let response_data = {
                        name: "Partenza",
                        attributes: {
                            step: 0,
                            keywords_found: [],
                            urls_queryable: [],
                            keywords: '',
                            parent: null,
                            uuid: null
                        },
                        children: data.children && data.children.map(
                            (d, i) =>(d.attributes.uuid === nodeData.attributes.uuid) ? {
                                name: nodeData.name,
                                attributes: nodeData.attributes,
                                children: response.data.data.items.map(
                                    item => {
                                        return {
                                            name: item.url,
                                            attributes: {
                                                keywords_found: item.keywords_found,
                                                keywords: item.keywords,
                                                step: item.step,
                                                urls_queryable: item.urls_queryable,
                                                parent: item.parent,
                                                uuid: item.uuid
                                            },
                                            children: item.children.map(child => {
                                                return {
                                                    name: child.url,
                                                    attributes: {
                                                        step: child.step,
                                                        keywords_found: child.keywords_found,
                                                        keywords: child.keywords,
                                                        urls_queryable: child.urls_queryable,
                                                        parent: child.parent,
                                                        uuid: child.uuid
                                                    }
                                                }
                                            })
                                        }
                                    }
                                )
                            } : d
                        )
                    }
                    setData(response_data);
                }
            }
        )
        .catch(
            error => {
                if (error.response) {
                    console.log(error.response.data.message);
                    if (error.response.data.status_code === 401)
                        window.location.replace('/login');
                } else {
                    window.location.replace('/login');
                }
            }
        );
    }

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
                            renderForeignObjectNode({ ...rd3tProps, foreignObjectProps, handleClickPickUp, handleClickExpand, classes })
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