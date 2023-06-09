import React from "react";
import MinDistanceRangeSliderWrapper from "./MinDistanceRangeSliderWrapper";
import _ from "underscore";
import { useState, useEffect } from "react";
import { FEATURES_NAMES, MIN_MAX_VALUES } from "../consts";
import PropTypes from "prop-types";

function RangeSliders(props) {
  const [featuresNames, setFeaturesNames] = useState([]);

  useEffect(() => {
    if (_.isEqual(featuresNames, [])) {
      setFeaturesNames(props.body[0][FEATURES_NAMES][MIN_MAX_VALUES]);
    }
  }, [featuresNames, setFeaturesNames]);

  function toRangeSliders() {
    if (!_.isEqual(featuresNames, [])) {
      return featuresNames.map((featureName) => (
        <MinDistanceRangeSliderWrapper
          key={featureName}
          title={featureName}
          body={props.body}
          setBody={props.setBody}
          featuresDescriptions={props.featuresDescriptions}
        ></MinDistanceRangeSliderWrapper>
      ));
    }
  }

  return <div className="range-sliders">{toRangeSliders()}</div>;
}

RangeSliders.propTypes = {
  body: PropTypes.array,
  setBody: PropTypes.func,
  featuresDescriptions: PropTypes.array,
};

export default RangeSliders;
