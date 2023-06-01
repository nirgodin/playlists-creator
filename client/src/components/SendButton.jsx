import React from "react";
import { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import axios from 'axios'
import { FILTER_PARAMS, IS_SUCCESS, MESSAGE, PHOTO, PLAYLIST_LINK, REQUEST_BODY } from "../consts";
import PropTypes from 'prop-types';

function SendButton(props) {
    const [isClicked, setIsClicked] = useState(true);
    const url = `${process.env.REACT_APP_BASE_URL}/${props.endpoint}`;

    useEffect(
        () => {
            setIsClicked(!props.isValidInput)
        }, [props.isValidInput]
    )

    async function sendPlaylistCreationRequest() {
        if (props.endpoint === PHOTO) {
            await sendPhotoRequest()
        } else {
            await sendPlaylistConfigurationRequest()
        }
    }

    async function sendPhotoRequest() {
        let bodyFormData = new FormData();
        bodyFormData.append(PHOTO, props.files[0]);
        const json = JSON.stringify(props.body[0]);
        const blob = new Blob([json], {type: 'application/json'});
        bodyFormData.append(REQUEST_BODY, blob);

        await axios({
            method: "post",
            url: url,
            data: bodyFormData,
            headers: { "Content-Type": "multipart/form-data" },
        })
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => handleResponse(jsonfiedData))
            .catch((error) => handleError(error))
    }

    async function sendPlaylistConfigurationRequest() {
        await axios.post(url, props.body[0])
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => handleResponse(jsonfiedData))
            .catch((error) => handleError(error))
    }

    function handleResponse(jsonfiedData) {
        const isSuccess = jsonfiedData[IS_SUCCESS];

        if (isSuccess) {
            const playlistLink = jsonfiedData[PLAYLIST_LINK];
            props.setPlaylistLink(playlistLink);
            props.setErrorMessage('');
        } else {
            const errorMessage = jsonfiedData[MESSAGE];
            props.setErrorMessage(errorMessage);
        }

        resetState(isSuccess);
    }

    function resetState(isSuccess) {
        const newRequestBody = props.body[0];
        newRequestBody[FILTER_PARAMS] = props.defaultRequestBody[0][FILTER_PARAMS]
        props.setBody([newRequestBody]);
        props.setIsSuccessful(isSuccess);
        setIsClicked(false);
    }

    function handleError() {
        props.setErrorMessage('An unexpected error has occured. Please reload the page and try again');
        props.setBody(props.defaultRequestBody);
    }

    function handleClick() {
        props.setWasRequestSent(true);
        setIsClicked(true);
        sendPlaylistCreationRequest();
    }

    return (
        <Button
            variant="outlined"
            disabled={isClicked}
            onClick={handleClick}
        > {props.text}
        </Button >
    )
}

SendButton.propTypes = {
    isValidInput: PropTypes.bool,
    endpoint: PropTypes.string,
    files: PropTypes.array,
    body: PropTypes.array,
    setBody: PropTypes.func,
    setPlaylistLink: PropTypes.func,
    setIsSuccessful: PropTypes.func,
    setErrorMessage: PropTypes.func,
    setWasRequestSent: PropTypes.func,
    text: PropTypes.string,
    defaultRequestBody: PropTypes.array
}

export default SendButton;