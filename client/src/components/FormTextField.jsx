import React from "react";
import TextField from "@mui/material/TextField";
import { toCamelCase } from "../utils/StringUtils";
import { useState, useEffect } from "react";
import { PLAYLIST_DETAILS } from "../consts";
import PropTypes from "prop-types";

function FormTextField(props) {
  const [value, setValue] = useState(props.defaultValue);
  const [isError, setIsError] = useState(false);
  const [helperText, setHelperText] = useState("");

  useEffect(() => {
    if (props.isRequired) {
      const validInput = value === "" ? false : true;
      props.setIsValidInput(validInput);
      setIsError(!validInput);
      const text = isError ? "* Required" : "";
      setHelperText(text);
    }
  }, [props, value, isError]);

  const handleChange = (event) => {
    setValue(event.target.value);
    const newBody = props.body[0];
    const bodyKey = toCamelCase(props.label);
    newBody[PLAYLIST_DETAILS][bodyKey] = event.target.value;
    props.setBody([newBody]);
  };

  return (
    <TextField
      sx={{
        "& .Mui-error": {
          color: "white",
        },
        '& label.Mui-focused': {
          color: '#6db4fc',
          fontSize: 20
        },
        '& .MuiOutlinedInput-root': {
          fontSize: 20
        },
        '& .MuiFormHelperText-root': {
          color: '#ff3838'
        }
      }}
      label={props.label}
      color="primary"
      onChange={handleChange}
      helperText={helperText}
      multiline={true}
      error={isError}
      focused
      defaultValue={props.defaultValue}
      inputProps={{ style: { color: "white", fontSize: "18px" } }}
      value={value}
      id={props.id}
    />
  );
}

FormTextField.propTypes = {
  defaultValue: PropTypes.string,
  isRequired: PropTypes.bool,
  setIsValidInput: PropTypes.func,
  body: PropTypes.array,
  setBody: PropTypes.func,
  label: PropTypes.string,
  id: PropTypes.string,
};

export default FormTextField;
