import LoginButton from ".././components/LoginButton";
import React from "react";
import PropTypes from "prop-types";

function LoginPage(props) {
  return (
    <div className="login-page">
      <h2>Please log in your spotify account</h2>
      <LoginButton
        text={"Login"}
        body={props.body}
        setBody={props.setBody}
      ></LoginButton>
    </div>
  );
}

LoginPage.propTypes = {
  body: PropTypes.array,
  setBody: PropTypes.func,
};

export default LoginPage;
