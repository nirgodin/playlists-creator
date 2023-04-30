import LoginButton from "./LoginButton";
import React from 'react';
import davidBowieFailureImage from '../static/david_bowie_failure_picture.jpeg';

export default function LoginPage(props) {
    return <div className="login-page">
        <img src={davidBowieFailureImage} alt="Logo" />;
        <h2>Please log in your spotify account</h2>
        <LoginButton
            text={'Login'}
            body={props.body}
            setBody={props.setBody}
        ></LoginButton>
    </div>
}