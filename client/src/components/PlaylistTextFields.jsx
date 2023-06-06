import * as React from "react";
import Box from "@mui/material/Box";
import FormTextField from "./FormTextField";
// import PlaylistSwitch from "./PlaylistSwitch";
import PropTypes from "prop-types";

function PlaylistTextFields(props) {
  return (
    <Box
      component="form"
      sx={{
        "& .MuiTextField-root": { m: 1, width: "15ch" },
      }}
      noValidate
      autoComplete="off"
    >
      <div className="row-items">
        <div>
          <FormTextField
            isRequired={true}
            id={"playlist-name"}
            label={"Playlist name"}
            defaultValue={""}
            body={props.body}
            setBody={props.setBody}
            isValidInput={props.isValidPlaylistName}
            setIsValidInput={props.setIsValidPlaylistName}
          ></FormTextField>
          <FormTextField
            isRequired={false}
            id={"playlist-description"}
            label={"Playlist description"}
            defaultValue={""}
            body={props.body}
            setBody={props.setBody}
          ></FormTextField>
        </div>
        <div className="is-public-switch">
          {/* <PlaylistSwitch
            body={props.body}
            setBody={props.setBody}
          ></PlaylistSwitch> */}
        </div>
      </div>
    </Box>
  );
}

PlaylistTextFields.propTypes = {
  body: PropTypes.array,
  setBody: PropTypes.func,
  isValidPlaylistName: PropTypes.bool,
  setIsValidPlaylistName: PropTypes.func,
};

export default PlaylistTextFields;
