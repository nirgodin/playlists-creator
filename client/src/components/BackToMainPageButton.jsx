import React from 'react';
import Button from '@mui/material/Button';
import PropTypes from 'prop-types'

function BackToMainPageButton(props) {
    function resetState() {
        props.setWasRequestSent(false);
        props.setIsSuccessfull(false);
    }
    
    return (
        <Button
            variant="outlined"
            onClick={resetState}
        > {'Create another playlist'}
        </Button >
    )
}

BackToMainPageButton.propTypes = {
    setWasRequestSent: PropTypes.func,
    setIsSuccessfull: PropTypes.func
}

export default BackToMainPageButton