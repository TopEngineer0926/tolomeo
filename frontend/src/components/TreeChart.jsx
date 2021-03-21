import React from 'react';
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

const containerStyles = {
    width: "100vw",
    height: "100vh"
  };
  
  const renderForeignObjectNode = ({
    nodeDatum,
    toggleNode,
    foreignObjectProps
  }) => (
    <g>
      <circle r={15}></circle>
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

export default function TreeChart(props) {
    const [translate, containerRef] = useCenteredTree();
    const nodeSize = { x: 400, y: 200 };
    const foreignObjectProps = { width: nodeSize.x, height: nodeSize.y, x: -100, className: "node-custom" };
    const data = props.data;

    if (null !== data) {
      return (
        <Container maxWidth="xl" style={containerStyles} ref={containerRef}>
          <Tree
            data={data}
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

    return (
      <div>Non ci sono risultati</div>
    )
  }