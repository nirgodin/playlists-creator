import * as React from "react";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";

function ClickButton(props) {
  return (
    <Button
      variant="outlined"
      disabled={props.isClicked}
      onClick={props.handleClick}
    >
      {" "}
      {props.text}
    </Button>
  );
}

ClickButton.propTypes = {
  isClicked: PropTypes.bool,
  text: PropTypes.string,
  handleClick: PropTypes.func,
};

export default ClickButton;
