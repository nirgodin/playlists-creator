import Button from '@mui/material/Button';

export default function BackToMainPageButton(props) {
    function resetState(e) {
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