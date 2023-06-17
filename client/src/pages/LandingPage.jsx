import React from "react";
import MethodToggleButtonGroup from ".././components/MethodToggleButtonGroup";
import { Box } from "@mui/material";
import FormTextField from ".././components/FormTextField";
import SendButton from ".././components/SendButton";
import { useState, useEffect } from "react";
import RequestBody from ".././components/RequestBody";
import { PROMPT, CONFIGURATION, PHOTO } from "../consts";
import PhotoDropzone from "../components/PhotoDropzone";
import _ from "underscore";
import PropTypes from "prop-types";
import Popup from "../components/Popup";
import PlaylistDetails from "../components/PlaylistDetails";

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
    } else {
      const isValid = isValidExistingPlaylist && isValidPlaylistName;
      setIsValidInput(isValid);
    }
  }, [alignment, isValidPrompt, isValidPlaylistName, isValidExistingPlaylist, files]);

  const playlistDetails = (
    <PlaylistDetails
      body={props.body}
      setBody={props.setBody}
      isValidPlaylistName={isValidPlaylistName}
      setIsValidPlaylistName={setIsValidPlaylistName}
    ></PlaylistDetails>
  );

  const popup = <Popup alignment={alignment}></Popup>;

  const toggleButton = (
    <div className="toggle-button">
      <MethodToggleButtonGroup
        alignment={alignment}
        setAlignment={setAlignment}
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
        ></SendButton>
      </Box>
      <p className="error-message" key={props.errorMessage}>
        {props.errorMessage}
      </p>
    </div>
  );

  if (alignment === PROMPT) {
    return (
      <div>
        {playlistDetails}
        <Box>
          {toggleButton}
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
          {buttons}
        </Box>
      </div>
    );
  } else if (alignment === CONFIGURATION) {
    return (
      <div>
        {playlistDetails}
        {toggleButton}
        <RequestBody body={props.body} setBody={props.setBody}></RequestBody>
        {buttons}
      </div>
    );
  } else if (alignment === PHOTO) {
    return (
      <div>
        {playlistDetails}
        {toggleButton}
        <PhotoDropzone files={files} setFiles={setFiles}></PhotoDropzone>
        {buttons}
      </div>
    );
  } else {
    return (
      <div>
        {playlistDetails}
        {toggleButton}
        <div className="text-field">
          <FormTextField
            isRequired={true}
            id={"Existing Playlist"}
            label={'Playlist URL'}
            defaultValue={""}
            body={props.body}
            setBody={props.setBody}
            isValidInput={isValidExistingPlaylist}
            setIsValidInput={setIsValidExistingPlaylist}
          ></FormTextField>
        </div>
        {buttons}
      </div>
    );
  }
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
};

export default LandingPage;
