import React from "react";
import PlaylistTextFields from "./PlaylistTextFields";
import PropTypes from "prop-types";

function PlaylistDetails(props) {
  return (
    <div className="playlist-details">
      <h3> Customize your own playlists </h3>
      <PlaylistTextFields
        body={props.body}
        setBody={props.setBody}
        isValidPlaylistName={props.isValidPlaylistName}
        setIsValidPlaylistName={props.setIsValidPlaylistName}
      ></PlaylistTextFields>
    </div>
  );
}

PlaylistDetails.propTypes = {
  body: PropTypes.array,
  setBody: PropTypes.func,
  isValidPlaylistName: PropTypes.bool,
  setIsValidPlaylistName: PropTypes.func,
};

export default PlaylistDetails;
