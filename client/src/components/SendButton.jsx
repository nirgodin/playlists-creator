import * as React from 'react';
import Button from '@mui/material/Button';
import axios from 'axios'

export default function SendButton(props) {
    const [isClicked, setIsClicked] = React.useState(false)
    const url = `${process.env.REACT_APP_BASE_URL}/${props.endpoint}`

    const sendPlaylistCreationRequest = async () => {
        await axios.post(url, props.body)
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => handleResponse(jsonfiedData))
            .catch((error) => handleError(error))
        setIsClicked(false);
    };

    const handleResponse = (jsonfiedData) => {
        const isSuccess = jsonfiedData['isSuccess'];
        const playlistLink = jsonfiedData['playlistLink'];
        props.setIsSuccessfull(isSuccess);
        props.setPlaylistLink(playlistLink);
    }

    const handleError = (error) => {
        console.log(error);
        props.setIsError(true)
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