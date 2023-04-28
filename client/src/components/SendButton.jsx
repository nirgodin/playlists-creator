import * as React from 'react';
import Button from '@mui/material/Button';
import axios from 'axios'

export default function SendButton(props) {
    const [isClicked, setIsClicked] = React.useState(false)
    const sendPlaylistCreationRequest = async () => {
        await axios.post(props.url, props.body)
            .then((resp) => JSON.stringify(resp.data))
            .then((data) => JSON.parse(data))
            .then((jsonfiedData) => jsonfiedData['isSuccess'])
            .then((isSuccess) => props.setIsSuccessfull(isSuccess))
        setIsClicked(false);
    };
    const handleClick = (e) => {
        props.setWasRequestSent(true);
        setIsClicked(true);
        sendPlaylistCreationRequest();
    }

    if (isClicked) {
        return <Button
            variant="outlined"
            disabled
        > {props.text}
        </Button >
    }
    else {
        return <Button
            variant="outlined"
            onClick={handleClick}
        > {props.text}
        </Button >
    }
}