import React, { Component } from 'react';
import TreeChart from './TreeChart';

class EvidenceChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
          evidences: null
        }
      }
    
      componentDidMount() {
        const url = "http://0.0.0.0:5000/map";
        fetch(url)
        .then(response => response.json())
        .then(json => this.handleResponse(json))
      }

      handleResponse(json) {
        const data = {
            name: "Partenza",
            attributes: {
                step: 0,
                keywords_found: null,
            },
            children: json.map(
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
        this.setState({ evidences: data })
      }
    
      render()  {
        return (<TreeChart data={this.state.evidences}></TreeChart>)
      }
}
export default EvidenceChart