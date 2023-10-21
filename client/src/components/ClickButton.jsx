import * as React from "react";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";
import { Stack } from "@mui/material";

function ClickButton(props) {
  return (
    <Stack direction={"row"} spacing={2} justifyContent={"center"}>
      <Button
        startIcon={props.startIcon}
        sx={{
          ":hover": { bgcolor: props.onHoverColor },
          cursor: props.cursor,
          width: props.width,
          height: props.height,
          fontSize: props.fontSize,
          backgroundColor: props.backgroundColor,
          color: props.color,
          fontWeight: 700,
        }}
        variant="contained"
        disabled={props.isClicked}
        onClick={props.handleClick}
      >
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
  backgroundColor: PropTypes.string,
  color: PropTypes.string,
  onHoverColor: PropTypes.string,
};

ClickButton.defaultProps = {
  backgroundColor: "#6db4fc",
  onHoverColor: "#1976d2",
  fontSize: 30,
  color: "rgb(0, 30, 60)",
};

export default ClickButton;
