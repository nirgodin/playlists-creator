import { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import axios from 'axios'
import { ACCESS_CODE, IS_SUCCESS, MESSAGE, PLAYLIST_LINK } from "../consts";

export default function SendButton(props) {
    const [isClicked, setIsClicked] = useState(true);
    const url = `${process.env.REACT_APP_BASE_URL}/${props.endpoint}`;

    useEffect(
        () => {
            setIsClicked(!props.isValidInput)
        }, [props.isValidInput]
    )

    const sendPlaylistCreationRequest = async () => {
        await axios.post(url, props.body[0])
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => handleResponse(jsonfiedData))
            .catch((error) => handleError(error))
        setIsClicked(false);
    };

    const handleResponse = (jsonfiedData) => {
        const isSuccess = jsonfiedData[IS_SUCCESS];

        if (isSuccess) {
            const playlistLink = jsonfiedData[PLAYLIST_LINK];
            props.setPlaylistLink(playlistLink);
        } else {
            const errorMessage = jsonfiedData[MESSAGE];
            props.setErrorMessage(errorMessage);
        }

        const newRequestBody = JSON.parse(JSON.stringify(props.defaultRequestBody));
        newRequestBody[0][ACCESS_CODE] = props.accessCode;
        props.setBody(newRequestBody);
        props.setIsSuccessfull(isSuccess);
        setIsClicked(false);
    }

    const handleError = (error) => {
        props.setErrorMessage('An unexpected error has occured. Please reolad the page and try again');
        props.setBody(props.defaultRequestBody);
    }

    const handleClick = (e) => {
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