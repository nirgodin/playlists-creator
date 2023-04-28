import * as React from 'react';
import Button from '@mui/material/Button';

export default function ClickButton(props) {
    if (props.isClicked) {
        return <Button
            variant="outlined"
            disabled
        > {props.text}
        </Button >
    }
    else {
        return <Button
            variant="outlined"
            onClick={props.handleClick}
        > {props.text}
        </Button >
    }
}