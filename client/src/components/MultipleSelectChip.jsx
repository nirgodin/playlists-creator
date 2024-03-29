import * as React from "react";
import { Box } from "@mui/material";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Chip from "@mui/material/Chip";
import { toCamelCase } from "../utils/StringUtils";
import _ from "underscore";
import { BACKGROUND_COLOR, FEATURES_VALUES, FILTER_PARAMS, MenuProps, POSSIBLE_VALUES, VALUE } from "../consts";
import PropTypes from "prop-types";

function MultipleSelectChip(props) {
  const [possibleValues, setPossibleValues] = React.useState(props.possibleValues);
  const [selectedOptions, setSelectedOptions] = React.useState([]);

  React.useEffect(() => {
    props.effectCallback(selectedOptions, props.title)
  }, [possibleValues, selectedOptions]);
  
  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedOptions(typeof value === "string" ? value.split(",") : value);
  };

  return (
    <div className="multiple-select-chip">
      <Box sx={{ width: 200 }}>
        <FormControl sx={{ width: 200 }}>
          <InputLabel
            className="input-label"
            id="demo-multiple-chip-label"
            style={{ color: "white" }}
          >
            {props.title}
          </InputLabel>
          <Select
            labelId="demo-multiple-chip-label"
            id="demo-multiple-chip"
            multiple={props.multiple}
            value={selectedOptions}
            onChange={handleChange}
            input={
              <OutlinedInput id="select-multiple-chip" label={props.title} />
            }
            renderValue={(selected) => (
              <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                {selected.map((value) => (
                  <Chip key={value} label={value} sx={{ color: BACKGROUND_COLOR, bgcolor: "#6db4fc", fontWeight: "600" }} />
                ))}
              </Box>
            )}
            MenuProps={MenuProps}
          >
            {possibleValues.map((option) => (
              <MenuItem key={option} value={option}>
                {option}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
    </div>
  );
}

MultipleSelectChip.propTypes = {
  title: PropTypes.string,
  body: PropTypes.array,
  setBody: PropTypes.func,
  effectCallback: PropTypes.func,
  multiple: PropTypes.bool,
  possibleValues: PropTypes.array
};

export default MultipleSelectChip;
