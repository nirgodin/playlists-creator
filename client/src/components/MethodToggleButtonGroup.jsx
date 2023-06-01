import * as React from 'react';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import { CONFIGURATION, PROMPT, PHOTO } from '../consts';
import TuneIcon from '@mui/icons-material/Tune';
import EditNoteIcon from '@mui/icons-material/EditNote';
import InsertPhotoRoundedIcon from '@mui/icons-material/InsertPhotoRounded';
import PropTypes from 'prop-types';

function MethodToggleButtonGroup(props) {
  function handleChange(event, newAlignment) {
    props.setAlignment(newAlignment);
    props.setEndpoint(newAlignment);
  }

  return (
    <ToggleButtonGroup
      color="primary"
      value={props.alignment}
      exclusive
      onChange={handleChange}
      aria-label="Platform"
    >
      <ToggleButton sx={{ color: 'white', width: '200px' }} value={PROMPT}>
        <EditNoteIcon className='toggle-button-icon' />
        {PROMPT}
      </ToggleButton>
      <ToggleButton sx={{ color: 'white', width: '200px' }} value={CONFIGURATION}>
        <TuneIcon className='toggle-button-icon' />
        {CONFIGURATION}
      </ToggleButton>
      <ToggleButton sx={{ color: 'white', width: '200px' }} value={PHOTO}>
        <InsertPhotoRoundedIcon className='toggle-button-icon' />
        {PHOTO}
      </ToggleButton>
    </ToggleButtonGroup >
  );
}

MethodToggleButtonGroup.propTypes = {
  setAlignment: PropTypes.func,
  setEndpoint: PropTypes.func,
  alignment: PropTypes.string
}

export default MethodToggleButtonGroup;