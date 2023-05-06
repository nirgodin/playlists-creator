import * as React from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import { toCamelCase } from '../utils/StringUtils';

export default function FilterCheckbox(props) {
  const [checked, setChecked] = React.useState(true)
  const camelCasedLabel = toCamelCase(props.title)

  function handleChange(event) {
    setChecked(event.target.checked);
    let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
    newBody['filterParams'][camelCasedLabel]['includeNan'] = event.target.checked;
    props.setBody([newBody]);
  }

  return (
    <FormGroup>
      <FormControlLabel
        sx={{ paddingLeft: 1 }}
        control={
          <Checkbox
            checked={checked}
            onChange={handleChange}
          />
        }
        label={props.label}
      />
    </FormGroup>
  );
}