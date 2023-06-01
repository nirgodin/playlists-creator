import * as React from 'react';
import Button from '@mui/material/Button';
import PropTypes from 'prop-types'

function ClickButton(props) {
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

ClickButton.propTypes = {
    isClicked: PropTypes.bool,
    text: PropTypes.string,
    handleClick: PropTypes.func
}

export default ClickButton