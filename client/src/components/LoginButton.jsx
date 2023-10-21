import * as React from "react";
import ClickButton from "./ClickButton";
import { generateAccessCodeURL } from "../utils/UrlUtils";
import PropTypes from "prop-types";
import LoginRoundedIcon from "@mui/icons-material/LoginRounded";
import LogoutRoundedIcon from "@mui/icons-material/LogoutRounded";
import { SPOTIFY_LOGOUT_URL } from "../consts";

function LoginButton(props) {
  let logoutWindow = null;
  
  const loginIcon = (
    <LoginRoundedIcon style={{ fontSize: props.iconFontSize }} />
  );
  const logoutIcon = (
    <LogoutRoundedIcon style={{ fontSize: props.iconFontSize }} />
  );

  const [isClicked, setIsClicked] = React.useState(false);
  const [text, setText] = React.useState(props.text);
  const [icon, setIcon] = React.useState(loginIcon);

  function login() {
    const accessCodeURL = generateAccessCodeURL(
      process.env.REACT_APP_SPOTIFY_CLIENT_ID,
      process.env.REACT_APP_SPOTIFY_REDIRECT_URI
    );
    window.location = accessCodeURL;
  }

  function exitLogoutWindow() {
    logoutWindow.close();
    window.location = process.env.REACT_APP_SPOTIFY_REDIRECT_URI;
  }

  function logout() {
    logoutWindow = window.open(SPOTIFY_LOGOUT_URL);
    setTimeout(exitLogoutWindow, 1000);
  }

  function handleClick() {
    setIsClicked(true);
    props.isUserLoggedIn ? logout() : login();
    setIsClicked(false);
  }

  React.useEffect(() => {
    if (props.isUserLoggedIn) {
      setText("Logout");
      setIcon(logoutIcon);
    } else {
      setText(props.text);
      setIcon(loginIcon);
    }
  }, [props.isUserLoggedIn]);

  return (
    <ClickButton
      startIcon={icon}
      width={"justify"}
      height={props.height}
      fontSize={props.fontSize}
      text={text}
      isClicked={isClicked}
      handleClick={handleClick}
      backgroundColor={props.backgroundColor}
      color={props.color}
      onHoverColor={props.onHoverColor}
    ></ClickButton>
  );
}

LoginButton.defaultProps = {
  height: "50px",
  iconFontSize: 30,
  fontSize: 24,
};

LoginButton.propTypes = {
  text: PropTypes.string,
  backgroundColor: PropTypes.string,
  fontSize: PropTypes.number,
  iconFontSize: PropTypes.number,
  height: PropTypes.string,
  color: PropTypes.string,
  isUserLoggedIn: PropTypes.bool,
  onHoverColor: PropTypes.string,
};

export default LoginButton;
