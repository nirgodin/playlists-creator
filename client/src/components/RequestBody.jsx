import React from "react";
import RangeSliders from "./RangeSliders";
import SelectChips from "./SelectChips";
import { useEffect, useState } from "react";
import _ from "underscore";
import { FEATURES_DESCRIPTIONS } from "../consts";
import PropTypes from "prop-types";

function RequestBody(props) {
  const [featuresDescriptions, setFeaturesDescriptions] = useState([]);

  useEffect(() => {
    if (_.isEqual(featuresDescriptions, [])) {
      setFeaturesDescriptions(props.body[0][FEATURES_DESCRIPTIONS])
    }
  }, [featuresDescriptions]);

  return (
    <div className="request-body">
      <div className="playlist-configuration">
        <SelectChips
          body={props.body}
          setBody={props.setBody}
          featuresDescriptions={featuresDescriptions}
        ></SelectChips>
        <RangeSliders
          body={props.body}
          setBody={props.setBody}
          featuresDescriptions={featuresDescriptions}
        ></RangeSliders>
      </div>
    </div>
  );
}

RequestBody.propTypes = {
  body: PropTypes.array,
  setBody: PropTypes.func,
};

export default RequestBody;
