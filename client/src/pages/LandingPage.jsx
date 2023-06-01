import React from "react"
import MethodToggleButtonGroup from ".././components/MethodToggleButtonGroup"
import { Box } from "@mui/material"
import FormTextField from ".././components/FormTextField"
import SendButton from ".././components/SendButton"
import { useState, useEffect } from "react"
import RequestBody from ".././components/RequestBody"
import PlaylistTextFields from ".././components/PlaylistTextFields"
import { PROMPT, CONFIGURATION, PHOTO } from "../consts"
import PhotoDropzone from "../components/PhotoDropzone"
import _ from "underscore"
import PropTypes from 'prop-types';

function LandingPage(props) {
    const [alignment, setAlignment] = useState(PROMPT);
    const [endpoint, setEndpoint] = useState(PROMPT);
    const [isValidInput, setIsValidInput] = useState(false);
    const [isValidPrompt, setIsValidPrompt] = useState(false);
    const [isValidPlaylistName, setIsValidPlaylistName] = useState(false);
    const [files, setFiles] = useState([]);

    useEffect(
        () => {
            if (endpoint === PROMPT) {
                const isValid = (isValidPrompt && isValidPlaylistName);
                setIsValidInput(isValid);
            } else if (endpoint === PHOTO){
                const isValid = (isValidPlaylistName && !_.isEqual(files, []));
                setIsValidInput(isValid);
            } else {
                setIsValidInput(isValidPlaylistName);
            }
        }, [endpoint, isValidPrompt, isValidPlaylistName, files]
    )
    const playlistDetails = <div className='playlist-details'>
        <PlaylistTextFields
            body={props.body}
            setBody={props.setBody}
            isValidPlaylistName={isValidPlaylistName}
            setIsValidPlaylistName={setIsValidPlaylistName}
        ></PlaylistTextFields>
    </div>

    const toggleButton = <div className="toggle-button">
        <MethodToggleButtonGroup
            alignment={alignment}
            setAlignment={setAlignment}
            setEndpoint={setEndpoint}
        ></MethodToggleButtonGroup>
    </div>

    const buttons = <div className="send-button">
        <Box>
            <SendButton
                text={'Create Playlist'}
                endpoint={endpoint}
                body={props.body}
                setBody={props.setBody}
                defaultRequestBody={props.defaultRequestBody}
                setWasRequestSent={props.setWasRequestSent}
                setIsSuccessfull={props.setIsSuccessfull}
                setErrorMessage={props.setErrorMessage}
                setPlaylistLink={props.setPlaylistLink}
                isValidInput={isValidInput}
                files={files}
                setFiles={setFiles}
            ></SendButton>
        </Box>
        <p className="error-message" key={props.errorMessage}>{props.errorMessage}</p>
    </div>

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
                            defaultValue={''}
                            body={props.body}
                            setBody={props.setBody}
                            isValidInput={isValidPrompt}
                            setIsValidInput={setIsValidPrompt}
                        ></FormTextField>
                    </div>
                    {buttons}
                </Box>
            </div>
        )
    }
    else if (alignment === CONFIGURATION) {
        return (
            <div>
                {playlistDetails}
                {toggleButton}
                <RequestBody
                    body={props.body}
                    setBody={props.setBody}
                ></RequestBody>
                {buttons}
            </div>
        )
    }
    else {
        return (
            <div>
                {playlistDetails}
                {toggleButton}
                <PhotoDropzone
                    files={files}
                    setFiles={setFiles}
                ></PhotoDropzone>
                {buttons}
            </div>
        )
    }
}

LandingPage.propTypes = {
    isValidInput: PropTypes.bool,
    endpoint: PropTypes.string,
    files: PropTypes.array,
    body: PropTypes.array,
    setBody: PropTypes.func,
    setPlaylistLink: PropTypes.func,
    setIsSuccessfull: PropTypes.func,
    setErrorMessage: PropTypes.func,
    setWasRequestSent: PropTypes.func,
    text: PropTypes.string,
    defaultRequestBody: PropTypes.array,
    errorMessage: PropTypes.string
}

export default LandingPage;