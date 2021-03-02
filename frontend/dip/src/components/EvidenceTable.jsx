import React, { Component } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { Container } from '@material-ui/core';

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
        <h1>Evidences Grid</h1>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Id</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Parent</TableCell>
              <TableCell>Url</TableCell>
              <TableCell>Keywords Searched</TableCell>
              <TableCell>Keywords Found</TableCell>
              <TableCell>Urls Queryable</TableCell>

            </TableRow>
          </TableHead>
          <TableBody>
            {this.state.evidences.map((row) => (
              <TableRow key={`${row.uuid}`}>
                <TableCell component="th" scope="row">
                  {row.uuid}
                </TableCell>
                <TableCell align="left">{row.title}</TableCell>
                <TableCell align="right">{row.parent}</TableCell>
                <TableCell align="right">{row.url}</TableCell>
                <TableCell align="right">{row.keywords}</TableCell>
                <TableCell align="right">{row.keywords_found}</TableCell>
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