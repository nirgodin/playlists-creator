import * as React from "react";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import { toCamelCase } from "../utils/StringUtils";
import { FILTER_PARAMS, INCLUDE_NAN } from "../consts";
import PropTypes from "prop-types";

function FilterCheckbox(props) {
  const [checked, setChecked] = React.useState(true);
  const camelCasedLabel = toCamelCase(props.title);

  function handleChange(event) {
    setChecked(event.target.checked);
    let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
    newBody[FILTER_PARAMS][camelCasedLabel][INCLUDE_NAN] = event.target.checked;
    props.setBody([newBody]);
  }

  return (
    <FormGroup>
      <FormControlLabel
        sx={{ paddingLeft: 1 }}
        control={
          <Checkbox className="checkbox"
            checked={checked}
            onChange={handleChange}
            style={{ color: "#6db4fc" }}
          />
        }
        label={props.label}
      />
    </FormGroup>
  );
}

FilterCheckbox.propTypes = {
  title: PropTypes.string,
  label: PropTypes.string,
  body: PropTypes.array,
  setBody: PropTypes.func,
};

export default FilterCheckbox;
