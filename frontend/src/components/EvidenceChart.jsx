import React, { Component, useEffect, useState } from 'react';
import TreeChart from './TreeChart';
import Pagination from '@material-ui/lab/Pagination';
import Grid from '@material-ui/core/Grid';
import AdminService from '../services/api.js';
import FormControl from '@material-ui/core/FormControl';
import NativeSelect from '@material-ui/core/NativeSelect';
import InputBase from '@material-ui/core/InputBase';
import { makeStyles, withStyles } from '@material-ui/core/styles';

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
        [theme.breakpoints.up('xl')]: {
            fontSize: 17,
            height: 33,
        },
        [theme.breakpoints.down('lg')]: {
            fontSize: 12,
            height: 23,
        },
        [theme.breakpoints.down('md')]: {
            fontSize: 8,
            height: 16,
        },
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

const EvidenceChart = (props) => {
    const classes = useStyles();
    const dataList = [20, 50, 100, 200];

    const [evidences, setEvidences] = useState(null);

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
        AdminService.getCharts(dataList[limit], page)
            .then(
                response => {
                    if (response.data.code !== 200) {
                        console.error(response.data.message);
                    } else {
                        localStorage.setItem("token", JSON.stringify(response.data.data.token));
                        const data = {
                            name: "Partenza",
                            attributes: {
                                step: 0,
                                keywords_found: null,
                            },
                            children: response.data.data.map(
                                item => {
                                    return {
                                        name: item.url,
                                        attributes: {
                                            keywords_found: item.keywords_found,
                                            step: item.step
                                        },
                                        children: item.children.map(child => {
                                            return {
                                                name: child.url,
                                                attributes: {
                                                    step: child.step,
                                                    keywords_found: child.keywords_found
                                                }
                
                                            }
                                        })
                                    }
                                }
                            )
                        }
                        setEvidences(data);
                    }
                },
                error => {
                    console.error("Can't connect to the Server!");
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
                <TreeChart
                    data={evidences}>
                </TreeChart>
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
export default EvidenceChart