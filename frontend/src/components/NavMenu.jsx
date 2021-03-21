import React from 'react';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import { useHistory } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';

const stylesMenu = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

export default function NavMenu() {
  const classes = stylesMenu();
  const history = useHistory();
  const [anchorEl, setAnchorEl] = React.useState(null);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleEvidences = (event) => {
    handleClose()
    history.push("/evidences")
  };
  const handleMap = (event) => {
    handleClose()
    history.push("/map")
  };
  return (
    <div>
        <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu" 
            aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}>
            <MenuIcon />
        </IconButton>
        <Menu
            id="simple-menu"
            anchorEl={anchorEl}
            keepMounted
            open={Boolean(anchorEl)}
            onClose={handleClose}
        >
        <MenuItem onClick={handleEvidences}>Tabella</MenuItem>
        <MenuItem onClick={handleMap}>Mappa</MenuItem>
      </Menu>
    </div>
  );
}