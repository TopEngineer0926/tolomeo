import React, { Component } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { Container } from '@material-ui/core';
import SearchDialog from './SearchDialog'

class EvidenceTable extends Component {

  constructor(props) {
    super(props);
    this.state = {
      evidences: []
    }
  }

  componentDidMount() {
    const url = "http://0.0.0.0:5000/evidences";
    fetch(url)
    .then(response => response.json())
    .then(json => this.setState({ evidences: json }))
  }

  render() {
    return (
      <Container maxWidth="xl">
        <h1>Risultati dello scraping</h1>
        <SearchDialog></SearchDialog>
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
            {this.state.evidences.map((row) => (
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
                <TableCell align="justify" style={{maxWidth:250, overflow:'hidden', maxHeight:50, textOverflow:"ellipsis", maxLines: 3, whiteSpace:"nowrap"}}>{row.keywords_found}</TableCell>
                <TableCell align="justify" style={{maxWidth:250, overflow:'hidden', maxHeight:50, textOverflow:"ellipsis", maxLines: 3, whiteSpace:"nowrap"}} >
                  {row.urls_queryable}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Container>
    );
  }
  
}

export default EvidenceTable;