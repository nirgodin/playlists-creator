import * as React from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import { Box } from '@mui/material';

export default function FilterCheckbox(props) {
  return (
    <FormGroup>
      <FormControlLabel control={<Checkbox defaultChecked />} label={props.label} />
    </FormGroup>
  );
}