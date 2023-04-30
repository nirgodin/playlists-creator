import LoginButton from "./LoginButton";
import React from 'react';

export default function LoginPage(props) {
    return <div className="login-page">
        <h2>Please log in your spotify account</h2>
        <LoginButton
            text={'Login'}
            body={props.body}
            setBody={props.setBody}
        ></LoginButton>
    </div>
}