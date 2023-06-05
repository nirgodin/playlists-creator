import * as React from "react";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";

function ClickButton(props) {
  return (
    <Button
      sx={{width: props.width, height: props.height, fontSize: props.fontSize, backgroundColor: "#6db4fc", color: "white", fontWeight: 700, WebkitTextStrokeWidth: "0.3px", WebkitTextStrokeColor: "black"}}
      variant="contained"
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
  width: PropTypes.string,
  height: PropTypes.string,
  fontSize: PropTypes.number
};

export default ClickButton;
