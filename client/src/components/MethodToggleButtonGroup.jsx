import * as React from "react";
// import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import { CONFIGURATION, PROMPT, PHOTO } from "../consts";
import TuneIcon from "@mui/icons-material/Tune";
import EditNoteIcon from "@mui/icons-material/EditNote";
import InsertPhotoRoundedIcon from "@mui/icons-material/InsertPhotoRounded";
import PropTypes from "prop-types";
import MethodToggleButton from "./MethodToggleButton";

function MethodToggleButtonGroup(props) {
  function handleChange(event, newAlignment) {
    props.setAlignment(newAlignment);
  }

  const toggleButtonsConfig = [
    {
      value: PROMPT,
      icon: <EditNoteIcon fontSize="large" sx={{ paddingRight: "10px" }} />,
    },
    {
      value: CONFIGURATION,
      icon: <TuneIcon sx={{ paddingRight: "10px", fontSize: 28 }} />,
    },
    {
      value: PHOTO,
      icon: <InsertPhotoRoundedIcon sx={{ paddingRight: "10px" }} />,
    },
  ];

  function toToggleButtons() {
    return toggleButtonsConfig.map((buttonConfig) => (
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
      sx={{ borderColor: "white", borderWidth: "1px", justifyContent: "center" }}
      color="primary"
      value={props.alignment}
      exclusive
      onChange={handleChange}
      aria-label="Platform"
    >
      {toToggleButtons()}
    </ToggleButtonGroup>
  );
}

MethodToggleButtonGroup.propTypes = {
  setAlignment: PropTypes.func,
  alignment: PropTypes.string,
};

export default MethodToggleButtonGroup;
