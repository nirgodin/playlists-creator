import React from "react";
import MethodToggleButtonGroup from ".././components/MethodToggleButtonGroup";
import { Box } from "@mui/material";
import FormTextField from ".././components/FormTextField";
import SendButton from ".././components/SendButton";
import { useState, useEffect } from "react";
import RequestBody from "../content_clients/RequestBody";
import {
  PROMPT,
  CONFIGURATION,
  PHOTO,
  EXISTING_PLAYLIST,
  WRAPPED,
  FOR_YOU,
} from "../consts";
import PhotoDropzone from "../content_clients/PhotoDropzone";
import _ from "underscore";
import PropTypes from "prop-types";
import Popup from "../components/Popup";
import PlaylistDetails from "../components/PlaylistDetails";
import TuneIcon from "@mui/icons-material/Tune";
import EditNoteIcon from "@mui/icons-material/EditNote";
import InsertPhotoRoundedIcon from "@mui/icons-material/InsertPhotoRounded";
import QueueMusicRoundedIcon from "@mui/icons-material/QueueMusicRounded";
import FavoriteRoundedIcon from "@mui/icons-material/FavoriteRounded";
import ReplayCircleFilledRoundedIcon from "@mui/icons-material/ReplayCircleFilledRounded";
import WrappedClient from "../content_clients/WrappedClient";

function LandingPage(props) {
  const [alignment, setAlignment] = useState(PROMPT);
  const [isValidInput, setIsValidInput] = useState(false);
  const [isValidPrompt, setIsValidPrompt] = useState(false);
  const [isValidExistingPlaylist, setIsValidExistingPlaylist] = useState(false);
  const [isValidPlaylistName, setIsValidPlaylistName] = useState(false);
  const [files, setFiles] = useState([]);

  useEffect(() => {
    if (alignment === PROMPT) {
      const isValid = isValidPrompt && isValidPlaylistName;
      setIsValidInput(isValid);
    } else if (alignment === PHOTO) {
      const isValid = isValidPlaylistName && !_.isEqual(files, []);
      setIsValidInput(isValid);
    } else if (alignment === CONFIGURATION) {
      setIsValidInput(isValidPlaylistName);
    } else if (alignment === EXISTING_PLAYLIST) {
      const isValid = isValidExistingPlaylist && isValidPlaylistName;
      setIsValidInput(isValid);
    } else {
      setIsValidInput(isValidPlaylistName)
    }
  }, [
    alignment,
    isValidPrompt,
    isValidPlaylistName,
    isValidExistingPlaylist,
    files,
  ]);

  const playlistDetails = (
    <PlaylistDetails
      body={props.body}
      setBody={props.setBody}
      isValidPlaylistName={isValidPlaylistName}
      setIsValidPlaylistName={setIsValidPlaylistName}
    ></PlaylistDetails>
  );

  const popup = <Popup alignment={alignment}></Popup>;

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
    {
      value: WRAPPED,
      icon: <ReplayCircleFilledRoundedIcon sx={{ paddingRight: "10px" }} />,
    },
    {
      value: FOR_YOU,
      icon: <FavoriteRoundedIcon sx={{ paddingRight: "10px" }} />,
    },
  ];

  const toggleButton = (
    <div className="toggle-button">
      <MethodToggleButtonGroup
        alignment={alignment}
        setAlignment={setAlignment}
        config={toggleButtonsConfig}
        sx={{
          borderColor: "white",
          borderWidth: "1px",
          justifyContent: "center",
        }}
      ></MethodToggleButtonGroup>
      {popup}
    </div>
  );

  const buttons = (
    <div className="send-button">
      <Box>
        <SendButton
          text={"Create Playlist"}
          alignment={alignment}
          body={props.body}
          setBody={props.setBody}
          defaultRequestBody={props.defaultRequestBody}
          setWasRequestSent={props.setWasRequestSent}
          setIsSuccessful={props.setIsSuccessful}
          setErrorMessage={props.setErrorMessage}
          setPlaylistLink={props.setPlaylistLink}
          isValidInput={isValidInput}
          files={files}
          setFiles={setFiles}
          setCaseId={props.setCaseId}
        ></SendButton>
      </Box>
      <p className="error-message" key={props.errorMessage}>
        {props.errorMessage}
      </p>
    </div>
  );

  const alignmentsMapping = {
    [PROMPT]: (
      <div className="text-field">
        <FormTextField
          isRequired={true}
          id={PROMPT}
          label={"Prompt"}
          defaultValue={""}
          body={props.body}
          setBody={props.setBody}
          isValidInput={isValidPrompt}
          setIsValidInput={setIsValidPrompt}
        ></FormTextField>
      </div>
    ),
    [CONFIGURATION]: (
      <RequestBody body={props.body} setBody={props.setBody}></RequestBody>
    ),
    [PHOTO]: <PhotoDropzone files={files} setFiles={setFiles}></PhotoDropzone>,
    [EXISTING_PLAYLIST]: (
      <div className="text-field">
        <FormTextField
          isRequired={true}
          id={"Existing Playlist"}
          label={"Playlist URL"}
          defaultValue={""}
          body={props.body}
          setBody={props.setBody}
          isValidInput={isValidExistingPlaylist}
          setIsValidInput={setIsValidExistingPlaylist}
        ></FormTextField>
      </div>
    ),
    [WRAPPED]: (
      <WrappedClient
        body={props.body}
        setBody={props.setBody}
      ></WrappedClient>
    ),
    [FOR_YOU]: "",
  };

  return (
    <div>
      {playlistDetails}
      {toggleButton}
      {[alignmentsMapping[alignment]]}
      {buttons}
    </div>
  );
}

LandingPage.propTypes = {
  isValidInput: PropTypes.bool,
  alignment: PropTypes.string,
  files: PropTypes.array,
  body: PropTypes.array,
  setBody: PropTypes.func,
  setPlaylistLink: PropTypes.func,
  setIsSuccessful: PropTypes.func,
  setErrorMessage: PropTypes.func,
  setWasRequestSent: PropTypes.func,
  text: PropTypes.string,
  defaultRequestBody: PropTypes.array,
  errorMessage: PropTypes.string,
  setCaseId: PropTypes.func
};

export default LandingPage;
