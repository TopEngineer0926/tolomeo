import React from 'react';
import Tree from 'react-d3-tree';
import { Container } from '@material-ui/core';
import { useCenteredTree } from "./helpers";
import '../assets/nodes.css'
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const containerStyles = {
    width: "100vw",
    height: "100vh"
  };
  
  // Here we're using `renderCustomNodeElement` render a component that uses
  // both SVG and HTML tags side-by-side.
  // This is made possible by `foreignObject`, which wraps the HTML tags to
  // allow for them to be injected into the SVG namespace.
  const renderForeignObjectNode = ({
    nodeDatum,
    toggleNode,
    foreignObjectProps
  }) => (
    <g>
      <circle r={15}></circle>
      {/* `foreignObject` requires width & height to be explicitly set. */}
      <foreignObject {...foreignObjectProps}>
        <Card style={{maxWidth: 345}}>
        <CardActionArea>
            <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
                {nodeDatum.name}
            </Typography>
            {nodeDatum.attributes.step && <Typography variant="body2" color="textSecondary" component="p">
                Ciclo: {nodeDatum.attributes.step}
            </Typography>
            }
            {nodeDatum.attributes.keywords_found && <Typography variant="body2" color="textSecondary" component="p">
            Parole chiave trovate: {nodeDatum.attributes.keywords_found}
            </Typography>
            }
            </CardContent>
        </CardActionArea>
        <CardActions>
            <Button size="small" color="primary">
            Espandi
            </Button>
        </CardActions>
        </Card>
      </foreignObject>
    </g>
  );

// This is a simplified example of an org chart with a depth of 2.
// Note how deeper levels are defined recursively via the `children` property.
const orgChart = {
  name: 'http://zqktlwi4fecvo6ri.onion/',
  attributes: {
    keywords_found: "drugs, revenge"
  },
  children: [
    {
        name: 'http://zqktlwi4fecvo6ri.onion/drugs',
        attributes: {
            step: 1,
            keywords_found: "drugs",
        },
    },
    {
        name: 'http://zqktlwi4fecvo6ri.onion/revengeporn',
        attributes: {
            step: 1,
            keywords_found: "revenge",
        },
    },
    {
        name: 'http://zqktlwi4fecvo6ri.onion/drugs',
        attributes: {
            step: 1,
            keywords_found: "drugs, revenge"
        },
    },
    {
        name: 'http://zqktlwi4fecvo6ri.onion/revengeporn',
        attributes: {
            step: 1,
            keywords_found: "drugs"
        },
    },
    {
        name: 'http://zqktlwi4fecvo6ri.onion/drugs',
        attributes: {
            step: 1,
            keywords_found: "drugs"
        },
    },
    {
        name: 'http://zqktlwi4fecvo6ri.onion/revengeporn',
        attributes: {
            step: 1,
            keywords_found: "drugs, revenge"
        },
    },
  ],
};


export default function OrgChartTree() {
    const [translate, containerRef] = useCenteredTree();
    const nodeSize = { x: 400, y: 200 };
    const foreignObjectProps = { width: nodeSize.x, height: nodeSize.y, x: -100, className: "node-custom" };
    return (
      <Container maxWidth="xl" style={containerStyles} ref={containerRef}>
        <Tree
          data={orgChart}
          translate={translate}
          nodeSize={nodeSize}
          renderCustomNodeElement={(rd3tProps) =>
            renderForeignObjectNode({ ...rd3tProps, foreignObjectProps })
          }
          orientation="vertical"
        />
      </Container>
    );
  }