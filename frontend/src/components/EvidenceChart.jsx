import React, { useEffect, useState } from 'react';
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
    const [totalpage, setTotalPage] = useState(1);

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
                    if (response.data.status_code !== 200) {
                        console.error(response.data.message);
                    } else {
                        setPage(response.data.data.page);
                        setTotalPage(response.data.data.total_pages);
                        const data = {
                            name: "Partenza",
                            attributes: {
                                step: 0,
                                keywords_found: [],
                                urls_queryable: [],
                                keywords: '',
                                parent: null,
                                uuid: null
                            },
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
                        }
                        setEvidences(data);
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
                            dataList.map(
                                (select, i) => <option value={i} key={select}>{select}</option>
                            )
                        }
                    </NativeSelect>
                </FormControl>
            </Grid>
            <Grid item container>
                <TreeChart
                    data={evidences}
                    limit={dataList[limit]}
                    page={page}
                />
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