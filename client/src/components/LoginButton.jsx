import * as React from 'react';
import ClickButton from './ClickButton';
import generateAccessCodeURL from '../utils/UrlUtils';

export default function LoginButton(props) {
    const [isClicked, setIsClicked] = React.useState(false)

    const extractCode = (href) => {
        return href.split('code=')[1];
    }

    const handleClick = (e) => {
        setIsClicked(true);
        const accessCodeURL = generateAccessCodeURL(process.env.REACT_APP_SPOTIFY_CLIENT_ID, process.env.REACT_APP_SPOTIFY_REDIRECT_URI)
        window.location = accessCodeURL;
    }
    
    React.useEffect(
        () => {
            if (window.location.href.includes('?code')) {
                const code = extractCode(window.location.href);
                let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
                newBody['accessCode'] = code;
                props.setBody([newBody]);
            }
        }, []
    )
    
    return <div>
        <ClickButton
            text={props.text}
            isClicked={isClicked}
            handleClick={handleClick}
        ></ClickButton>
    </div>
}