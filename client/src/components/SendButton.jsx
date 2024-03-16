import React from "react";
import { useState, useEffect } from "react";
import AutoFixHighRoundedIcon from "@mui/icons-material/AutoFixHighRounded";
import axios from "axios";
import {
  CASE_ID,
  // FILTER_PARAMS,
  MESSAGE,
  PHOTO,
} from "../consts";
import PropTypes from "prop-types";
import ClickButton from "./ClickButton";
import { Tooltip } from "@mui/material";

function SendButton(props) {
  const [isClicked, setIsClicked] = useState(false);
  const [cursor, setCursor] = useState(undefined);
  const url = `${process.env.REACT_APP_BASE_URL}/playlist/${props.alignment}`;

  useEffect(() => {
    props.isValidInput ? setCursor(undefined) : setCursor("not-allowed");
  }, [props.isValidInput]);

  async function sendPlaylistCreationRequest() {
    if (props.alignment === PHOTO) {
      await sendPhotoRequest();
    } else {
      await sendPlaylistRequest();
    }
  }

  async function sendPhotoRequest() {
    let bodyFormData = new FormData();
    bodyFormData.append(PHOTO, props.files[0]);
    const body = JSON.stringify(props.body[0]);
    bodyFormData.append("body", body);

    await axios({
      method: "post",
      auth: {
        username: process.env.REACT_APP_USERNAME,
        password: process.env.REACT_APP_PASSWORD,
      },
      url: url,
      data: bodyFormData,
      headers: { "Content-Type": "multipart/form-data" },
    })
      .then((resp) => JSON.stringify(resp.data))
      .then((data) => JSON.parse(data))
      .then((jsonfiedData) => handleResponse(jsonfiedData))
      .catch((error) => handleError(error));
  }

  async function sendPlaylistRequest() {
    await axios
      .post(url, props.body[0], {
        auth: {
          username: process.env.REACT_APP_USERNAME,
          password: process.env.REACT_APP_PASSWORD,
        },
      })
      .then((resp) => JSON.stringify(resp.data))
      .then((data) => JSON.parse(data))
      .then((jsonfiedData) => handleResponse(jsonfiedData))
      .catch((error) => handleError(error));
  }

  function handleResponse(jsonfiedData) {
    const caseId = jsonfiedData[CASE_ID];
    const isSuccess = (caseId !== undefined);

    if (isSuccess) {
      props.setCaseId(caseId);
      // const playlistLink = jsonfiedData[PLAYLIST_LINK];
      // props.setPlaylistLink(playlistLink);
      props.setErrorMessage("");
    } else {
      const errorMessage = jsonfiedData[MESSAGE];
      props.setErrorMessage(errorMessage);
    }

    // resetState(isSuccess);
  }

  // function resetState(isSuccess) {
  //   const newRequestBody = props.body[0];
  //   newRequestBody[FILTER_PARAMS] = props.defaultRequestBody[0][FILTER_PARAMS];
  //   props.setBody([newRequestBody]);
  //   props.setIsSuccessful(isSuccess);
  //   setIsClicked(false);
  // }

  function handleError() {
    props.setErrorMessage(
      "An unexpected error has occurred. Please reload the page and try again"
    );
    props.setBody(props.defaultRequestBody);
  }

  function handleClick() {
    if (!props.isValidInput) {
      props.setErrorMessage(
        "Please fill in all required fields before submitting"
      );
    } else {
      props.setWasRequestSent(true);
      setIsClicked(true);
      sendPlaylistCreationRequest();
    }
  }

  return (
    <div>
      <Tooltip title="Delete">
        <ClickButton
          startIcon={<AutoFixHighRoundedIcon style={{ fontSize: 30 }} />}
          cursor={cursor}
          isClicked={isClicked}
          text={props.text}
          handleClick={handleClick}
          width={"justify"}
          height={"50px"}
          fontSize={22}
        ></ClickButton>
      </Tooltip>
    </div>
  );
}

SendButton.propTypes = {
  isValidInput: PropTypes.bool,
  alignment: PropTypes.string,
  files: PropTypes.array,
  body: PropTypes.array,
  setBody: PropTypes.func,
  setPlaylistLink: PropTypes.func,
  setIsSuccessful: PropTypes.func,
  setErrorMessage: PropTypes.func,
  setWasRequestSent: PropTypes.func,
  text: PropTypes.string,
  defaultRequestBody: PropTypes.array,
  setCaseId: PropTypes.func,
};

export default SendButton;
