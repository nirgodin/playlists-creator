import { ToggleButton } from "@mui/material";
import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { convertCamelToTitle } from "../utils/StringUtils";

function MethodToggleButton(props) {
  const [selected, setSelected] = useState(false);
  
  useEffect(() => {
    setSelected(props.alignment === props.value)
  });

  function handleClick() {
    props.setAlignment(props.value);
    setSelected(true);
  }

  return (
    <ToggleButton
    sx={{ color: 'white', bgcolor: "#02305e", width: "260px", fontSize: "20px"}}
      selected={selected}
      value={convertCamelToTitle(props.value)}
      onClick={handleClick}
    >
      {props.icon}
      {convertCamelToTitle(props.value)}
    </ToggleButton>
  );
}

MethodToggleButton.propTypes = {
  value: PropTypes.string,
  alignment: PropTypes.string,
  setAlignment: PropTypes.func,
  icon: PropTypes.func,
};

export default MethodToggleButton;
