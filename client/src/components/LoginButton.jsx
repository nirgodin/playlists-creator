import * as React from "react";
import ClickButton from "./ClickButton";
import { generateAccessCodeURL } from "../utils/UrlUtils";
import PropTypes from "prop-types";

function LoginButton(props) {
  const [isClicked, setIsClicked] = React.useState(false);

  function handleClick() {
    setIsClicked(true);
    const accessCodeURL = generateAccessCodeURL(
      process.env.REACT_APP_SPOTIFY_CLIENT_ID,
      process.env.REACT_APP_SPOTIFY_REDIRECT_URI
    );
    window.location = accessCodeURL;
  }

  return (
    <div className="click-button">
      <ClickButton
        width={'100px'}
        height={'50px'}
        fontSize={20}
        text={props.text}
        isClicked={isClicked}
        handleClick={handleClick}
      ></ClickButton>
    </div>
  );
}

LoginButton.propTypes = {
  text: PropTypes.string,
};

export default LoginButton;
