import * as React from 'react';
import ClickButton from './ClickButton';
import {generateAccessCodeURL} from '../utils/UrlUtils';

export default function LoginButton(props) {
    const [isClicked, setIsClicked] = React.useState(false)

    const handleClick = (e) => {
        setIsClicked(true);
        const accessCodeURL = generateAccessCodeURL(process.env.REACT_APP_SPOTIFY_CLIENT_ID, process.env.REACT_APP_SPOTIFY_REDIRECT_URI)
        window.location = accessCodeURL;
    }

    return <div>
        <ClickButton
            text={props.text}
            isClicked={isClicked}
            handleClick={handleClick}
        ></ClickButton>
    </div>
}