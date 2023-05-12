import { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import axios from 'axios'
import { FILTER_PARAMS, IS_SUCCESS, MESSAGE, PLAYLIST_LINK } from "../consts";

export default function SendButton(props) {
    const [isClicked, setIsClicked] = useState(true);
    const url = `${process.env.REACT_APP_BASE_URL}/${props.endpoint}`;

    useEffect(
        () => {
            setIsClicked(!props.isValidInput)
        }, [props.isValidInput]
    )

    async function sendPlaylistCreationRequest() {
        await axios.post(url, props.body[0])
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => handleResponse(jsonfiedData))
            .catch((error) => handleError(error))
        setIsClicked(false);
    };

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
        props.setIsSuccessfull(isSuccess);
        setIsClicked(false);
    }

    function handleError(error) {
        props.setErrorMessage('An unexpected error has occured. Please reload the page and try again');
        props.setBody(props.defaultRequestBody);
    }

    function handleClick(e) {
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