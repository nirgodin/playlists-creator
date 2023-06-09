import React from "react";
import Tooltip from "@mui/material/Tooltip";
import HelpRoundedIcon from "@mui/icons-material/HelpRounded";
import IconButton from "@mui/material/IconButton";
import { useState, useEffect } from "react";
import _ from "underscore";
import PropTypes from "prop-types";

function InfoToolTip(props) {
  const [featureDescription, setFeatureDescription] = useState("");

  useEffect(() => {
    if (
      featureDescription === "" &&
      !_.isEqual(props.featuresDescriptions, [])
    ) {
      const description = props.featuresDescriptions[props.title];
      setFeatureDescription(description);
    }
  }, [featureDescription, props.featuresDescriptions, props.title]);

  return (
    <div>
      <Tooltip
        title={
          <p
            className="tooltip-title"
            style={{ fontSize: 14, textAlign: "justify" }}
          >
            {featureDescription}
          </p>
        }
      >
        <IconButton color={"inherit"}>
          <HelpRoundedIcon fontSize={"small"} />
        </IconButton>
      </Tooltip>
    </div>
  );
}

InfoToolTip.propTypes = {
  featuresDescriptions: PropTypes.array,
  title: PropTypes.string,
};

export default InfoToolTip;
