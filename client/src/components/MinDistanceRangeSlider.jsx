import React from "react";
import { useState, useEffect } from "react";
import { Box, Typography } from "@mui/material";
import { Slider } from "@mui/material";
import _ from "underscore";
import { toCamelCase } from "../utils/StringUtils";
import { MIN, MAX, MIN_MAX_VALUES, FILTER_PARAMS, VALUE } from "../consts";
import { sendGetRequest } from "../utils/RequestsUtils";
import PropTypes from "prop-types";

function MinDistanceRangeSlider(props) {
  const [minMaxValues, setMinMaxValues] = useState([]);
  const [actualValues, setActualValues] = useState([]);
  const [minDistance, setMinDistance] = useState(0);
  const minTitleValue = toCamelCase(`${MIN} ${props.title}`);
  const maxTitleValue = toCamelCase(`${MAX} ${props.title}`);

  async function getMinMaxValues() {
    if (_.isEqual(minMaxValues, [])) {
      const values = await sendGetRequest(
        `${MIN_MAX_VALUES}/${props.title}`,
        MIN_MAX_VALUES
      );
      setMinMaxValues(values);
    }
  }

  useEffect(() => {
    if (_.isEqual(minMaxValues, [])) {
      getMinMaxValues();
    }

    if (_.isEqual(actualValues, []) && !_.isEqual(minMaxValues, [])) {
      const updatedMinDistance = (minMaxValues[1] - minMaxValues[0]) / 10;
      setMinDistance(updatedMinDistance);
      setActualValues(minMaxValues);
    }
  }, [minMaxValues, actualValues, getMinMaxValues]);

  function updateRangeValues(newValue, activeThumb) {
    if (!Array.isArray(newValue)) {
      return;
    }

    if (activeThumb === 0) {
      const minActualValue = Math.min(
        newValue[0],
        actualValues[1] - minDistance
      );
      setActualValues([minActualValue, actualValues[1]]);
    } else {
      const maxActualValue = Math.max(
        newValue[1],
        actualValues[0] + minDistance
      );
      setActualValues([actualValues[0], maxActualValue]);
    }
  }

  function updateRequestBody() {
    let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
    newBody[FILTER_PARAMS][minTitleValue][VALUE] = actualValues[0];
    newBody[FILTER_PARAMS][maxTitleValue][VALUE] = actualValues[1];
    props.setBody([newBody]);
  }

  function handleChange(event, newValue, activeThumb) {
    updateRangeValues(newValue, activeThumb);
    updateRequestBody();
  }

  return (
    <div className="range-slider">
      <Box sx={{ width: 180 }}>
        <Typography gutterBottom>{props.title}</Typography>
        <Slider
          style={{ color: "#6db4fc" }}
          min={minMaxValues[0]}
          max={minMaxValues[1]}
          value={actualValues}
          onChange={handleChange}
          valueLabelDisplay="auto"
          disableSwap
        />
      </Box>
    </div>
  );
}

MinDistanceRangeSlider.propTypes = {
  title: PropTypes.string,
  body: PropTypes.array,
  setBody: PropTypes.func,
};

export default MinDistanceRangeSlider;
