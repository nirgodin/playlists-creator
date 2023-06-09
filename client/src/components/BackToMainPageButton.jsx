import React from "react";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";

function BackToMainPageButton(props) {
  function resetState() {
    props.setWasRequestSent(false);
    props.setIsSuccessful(false);
  }

  return (
    <Button sx={{fontWeight: 500, fontSize: 15, borderColor: "#6db4fc", color: "#6db4fc"}} variant="outlined" onClick={resetState}>
      {" "}
      {"Create another playlist"}
    </Button>
  );
}

BackToMainPageButton.propTypes = {
  setWasRequestSent: PropTypes.func,
  setIsSuccessful: PropTypes.func,
};

export default BackToMainPageButton;
