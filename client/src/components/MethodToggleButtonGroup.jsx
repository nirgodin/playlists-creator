import * as React from "react";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import PropTypes from "prop-types";
import MethodToggleButton from "./MethodToggleButton";

function MethodToggleButtonGroup(props) {
  function handleChange(event, newAlignment) {
    props.setAlignment(newAlignment);
  }

  function toToggleButtons() {
    return props.config.map((buttonConfig) => (
      <MethodToggleButton
        key={"toggle-button-icon"}
        value={buttonConfig["value"]}
        icon={buttonConfig["icon"]}
        alignment={props.alignment}
        setAlignment={props.setAlignment}
      ></MethodToggleButton>
    ));
  }

  return (
    <ToggleButtonGroup
      sx={props.sx}
      color="primary"
      value={props.alignment}
      exclusive
      onChange={handleChange}
      aria-label="Platform"
    >
      <div className="toggle-button-bla">{toToggleButtons()}</div>
    </ToggleButtonGroup>
  );
}

MethodToggleButtonGroup.propTypes = {
  setAlignment: PropTypes.func,
  alignment: PropTypes.string,
  config: PropTypes.array,
  sx: PropTypes.object,
};

export default MethodToggleButtonGroup;
