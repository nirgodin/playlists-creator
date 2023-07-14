import LoginButton from ".././components/LoginButton";
import React from "react";
import PropTypes from "prop-types";
import { LOGIN_PAGE_TEXT } from "../consts";
import { Box, Typography } from "@mui/material";

function LoginPage(props) {
  function toTypographies(descriptionMapping) {
    return descriptionMapping.map((typographyDetails) => (
      <Typography
        key={""}
        variant={typographyDetails["variant"]}
        sx={{
          p: 2,
          paddingBottom: "0px",
          paddingTop: "5px",
          textAlign: typographyDetails["textAlign"],
          color: typographyDetails["color"],
          fontWeight: typographyDetails["fontWeight"],
          fontFamily: "Gill Sans",
        }}
      >
        {typographyDetails["text"]}
      </Typography>
    ));
  }

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
      <LoginButton
        text={"Login to get started"}
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
