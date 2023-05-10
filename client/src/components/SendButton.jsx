import { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import axios from 'axios'

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
        const isSuccess = jsonfiedData['isSuccess'];

        if (isSuccess) {
            const playlistLink = jsonfiedData['playlistLink'];
            props.setPlaylistLink(playlistLink);
        } else {
            const errorMessage = jsonfiedData['message'];
            props.setErrorMessage(errorMessage);
        }

        const newRequestBody = JSON.parse(JSON.stringify(props.defaultRequestBody));
        newRequestBody[0]['accessCode'] = props.accessCode;
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