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
      const text = isError ? "This field is required" : "";
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
      inputProps={{ style: { color: "white" } }}
      multiline={true}
      error={isError}
      required={props.isRequired}
      value={value}
      id={props.id}
      label={props.label}
      defaultValue={props.defaultValue}
      onChange={handleChange}
      helperText={helperText}
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
