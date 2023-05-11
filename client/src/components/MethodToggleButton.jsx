import * as React from 'react';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import { CONFIGURATION, PROMPT } from '../consts';

export default function MethodToggleButton(props) {
  const handleChange = (event, newAlignment) => {
    props.setAlignment(newAlignment);
  };

  return (
    <ToggleButtonGroup
      color="primary"
      value={props.alignment}
      exclusive
      onChange={handleChange}
      aria-label="Platform"
    >
      <ToggleButton sx={{color: 'white'}} value={PROMPT}>prompt</ToggleButton>
      <ToggleButton sx={{color: 'white'}} value={CONFIGURATION}>configuration</ToggleButton>
    </ToggleButtonGroup>
  );
}