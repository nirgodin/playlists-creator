import Button from '@mui/material/Button';

export default function BackToMainPageButton(props) {
    return (
        <Button
            variant="outlined"
            onClick={props.setWasRequestSent(false)}
        > {'Create another playlist'}
        </Button >
    )
}