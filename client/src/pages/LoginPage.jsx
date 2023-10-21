import LoginButton from ".././components/LoginButton";
import React from "react";
import PropTypes from "prop-types";
import { LOGIN_PAGE_TEXT } from "../consts";
import { Box } from "@mui/material";
import { toTypographies } from "../utils/TypographiesUtils";

function LoginPage(props) {
  return (
    <div className="login-page">
      <Box
        sx={{
          width: 750,
          display: "flex",
          flexDirection: "column",
          textAlign: "justify",
        }}
      >
        {toTypographies(LOGIN_PAGE_TEXT)}
      </Box>
      <div className="login-button">
        <LoginButton
          text={"Login to get started"}
          body={props.body}
          setBody={props.setBody}
          fontSize={20}
        ></LoginButton>
      </div>
    </div>
  );
}

LoginPage.propTypes = {
  body: PropTypes.array,
  setBody: PropTypes.func,
};

export default LoginPage;
