import * as React from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

export default function FilterCheckbox(props) {
  return (
    <FormGroup>
      <FormControlLabel sx={{ paddingLeft: 1 }} control={<Checkbox defaultChecked />} label={props.label} />
    </FormGroup>
  );
}