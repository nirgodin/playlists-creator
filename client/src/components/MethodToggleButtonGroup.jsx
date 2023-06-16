import * as React from "react";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import { CONFIGURATION, PROMPT, PHOTO, EXISTING_PLAYLIST } from "../consts";
import TuneIcon from "@mui/icons-material/Tune";
import EditNoteIcon from "@mui/icons-material/EditNote";
import InsertPhotoRoundedIcon from "@mui/icons-material/InsertPhotoRounded";
import PropTypes from "prop-types";
import MethodToggleButton from "./MethodToggleButton";
import QueueMusicRoundedIcon from '@mui/icons-material/QueueMusicRounded';

function MethodToggleButtonGroup(props) {
  function handleChange(event, newAlignment) {
    props.setAlignment(newAlignment);
  }

  const toggleButtonsConfig = [
    {
      value: CONFIGURATION,
      icon: <TuneIcon sx={{ paddingRight: "10px" }} />,
    },
    {
      value: EXISTING_PLAYLIST,
      icon: <QueueMusicRoundedIcon sx={{ paddingRight: "10px" }} />,
    },
    {
      value: PHOTO,
      icon: <InsertPhotoRoundedIcon sx={{ paddingRight: "10px" }} />,
    },
    {
      value: PROMPT,
      icon: <EditNoteIcon sx={{ paddingRight: "10px" }} />,
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
