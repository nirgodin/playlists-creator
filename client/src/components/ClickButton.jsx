import * as React from "react";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";
import { Stack } from "@mui/material";

function ClickButton(props) {
  return (
    <Stack direction={"row"} spacing={2} justifyContent={"center"}>
      <Button
        startIcon={props.startIcon}
        style={{ alignItems: "center", display: "flex" }}
        sx={{
          cursor: props.cursor,
          width: props.width,
          height: props.height,
          fontSize: props.fontSize,
          backgroundColor: "#6db4fc",
          color: "rgb(0, 30, 60)",
          fontWeight: 700,
        }}
        variant="contained"
        disabled={props.isClicked}
        onClick={props.handleClick}
      >
        {" "}
        {props.text}
      </Button>
    </Stack>
  );
}

ClickButton.propTypes = {
  isClicked: PropTypes.bool,
  text: PropTypes.string,
  handleClick: PropTypes.func,
  width: PropTypes.string,
  height: PropTypes.string,
  fontSize: PropTypes.number,
  cursor: PropTypes.string,
  startIcon: PropTypes.elementType,
};

export default ClickButton;
