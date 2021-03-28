import React, { useEffect, useState } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { Checkbox, Container } from '@material-ui/core';
import SearchDialog from './SearchDialog'
import Pagination from '@material-ui/lab/Pagination';
import Grid from '@material-ui/core/Grid';
import AdminService from '../services/api.js';
import FormControl from '@material-ui/core/FormControl';
import NativeSelect from '@material-ui/core/NativeSelect';
import InputBase from '@material-ui/core/InputBase';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const BootstrapInput = withStyles((theme) => ({
    root: {
        'label + &': {
            [theme.breakpoints.up('xl')]: {
                marginTop: 24,
            },
            [theme.breakpoints.between('lg', 'lg')]: {
                marginTop: 17,
            },
            [theme.breakpoints.down('md')]: {
                marginTop: 12,
            },
        },
    },
    input: {
        borderRadius: 4,
        position: 'relative',
        backgroundColor: 'white',
        border: '1px solid #1499ff',
        color: '#1499ff',
        padding: '2px 12px',
        display: 'flex',
        alignItems: 'center',
        transition: theme.transitions.create(['border-color', 'box-shadow']),
        // Use the system font instead of the default Roboto font.
        fontFamily: [
            'Poppins',
        ].join(','),
        '&:focus': {
            borderRadius: 4,
            borderColor: '#1499ff',
            boxShadow: '0 0 0 0.2rem rgba(0,123,255,.25)',
        },
    },
}))(InputBase);

const useStyles = makeStyles({
    margin: {
        width: props => props.width,
        '& .MuiSelect-select.MuiSelect-select': {
            borderColor: '#1499ff'
        },
        '& .MuiNativeSelect-icon': {
            color: '#1499ff'
        },
    },
    selectMargin: {
        marginRight: 20,
        marginTop: 20
    }
});

const EvidenceTable = (props) => {
    const classes = useStyles();
    const dataList = [20, 50, 100, 200];

    const [evidences, setEvidences] = useState([]);
    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(0);
    const totalpage = 10;

    const handleChangePage = (event, page) => {
        setPage(page);
    }
    const handleChange = (event) => {
        setLimit(event.target.value);
    };

    useEffect(() => {
        AdminService.getEvidences(dataList[limit], page)
            .then(
                response => {
                    if (response.data.status_code !== 200) {
                        console.error(response.data.message);
                      } else {
                        setEvidences(response.data.data);
                      }
                }
            )
            .catch(
                error => {
                    console.log(error.response.data.message);
                    if (error.response.data.status_code === 401)
                        window.location.replace('/login');
                }
            );
    }, [page, limit]);

    return (
        <Grid container spacing={2}>
            <Grid item container direction="row-reverse" className={classes.selectMargin}>
                <FormControl className={classes.margin}>
                    <NativeSelect
                        value={limit}
                        onChange={handleChange}
                        input={<BootstrapInput />}
                    >
                        {
                            dataList.map((select, i) =>
                                <option value={i} key={select}>{select}</option>
                            )}
                    </NativeSelect>
                </FormControl>
            </Grid>
            <Grid item container>
                <Container maxWidth="xl">
                    <h1>Risultati dello scraping</h1>
                    <Grid item container spacing={3} direction="row" alignItems="center">
                        <Grid item>
                            <SearchDialog></SearchDialog>
                        </Grid>
                        <Grid item>
                            <TextField
                                autoFocus
                                id="cycles"
                                label="Numero di cicli"
                                type="text"
                            />
                        </Grid>
                        <Grid item>
                            <Checkbox
                            />
                        </Grid>
                    </Grid>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>UUID</TableCell>
                                <TableCell>Titolo</TableCell>
                                <TableCell>Precedente</TableCell>
                                <TableCell>Url</TableCell>
                                <TableCell>Numero Ciclo</TableCell>
                                <TableCell>Totale Cicli</TableCell>
                                <TableCell>Parole chiave cercate</TableCell>
                                <TableCell>Parole chiave trovate</TableCell>
                                <TableCell>Url trovate utilizzabili</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {evidences.map((row) => (
                                <TableRow key={`${row.uuid}`}>
                                    <TableCell component="th" scope="row">
                                        {row.uuid}
                                    </TableCell>
                                    <TableCell align="left">{row.title}</TableCell>
                                    <TableCell align="left">{row.parent}</TableCell>
                                    <TableCell align="left">{row.url}</TableCell>
                                    <TableCell align="left">{row.step}</TableCell>
                                    <TableCell align="left">{row.total_steps}</TableCell>
                                    <TableCell align="left">{row.keywords}</TableCell>
                                    <TableCell align="justify" style={{ maxWidth: 250, overflow: 'hidden', maxHeight: 50, textOverflow: "ellipsis", maxLines: 3, whiteSpace: "nowrap" }}>{row.keywords_found}</TableCell>
                                    <TableCell align="justify" style={{ maxWidth: 250, overflow: 'hidden', maxHeight: 50, textOverflow: "ellipsis", maxLines: 3, whiteSpace: "nowrap" }} >
                                        {row.urls_queryable}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Container>
            </Grid>
            <Grid item container direction="row-reverse" className={classes.selectMargin}>
                <Pagination
                    count={totalpage}
                    color="primary"
                    page={page}
                    onChange={handleChangePage}
                />
            </Grid>
        </Grid>
    );

}

export default EvidenceTable;