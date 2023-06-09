import React from "react";
import { useState, useEffect } from "react";
import MultipleSelectChipWrapper from "./MultipleSelectChipWrapper";
import _ from "underscore";
import { FEATURES_NAMES, POSSIBLE_VALUES } from "../consts";
import PropTypes from "prop-types";

function SelectChips(props) {
  const [featuresNames, setFeaturesNames] = useState([]);

  useEffect(() => {
    if (_.isEqual(featuresNames, [])) {
      setFeaturesNames(props.body[0][FEATURES_NAMES][POSSIBLE_VALUES]);
    }
  }, [featuresNames, setFeaturesNames]);

  function toSelectChips() {
    return featuresNames.map((featureName) => (
      <MultipleSelectChipWrapper
        key={featureName}
        title={featureName}
        body={props.body}
        setBody={props.setBody}
        includesCheckbox={true}
        checkboxLabel={"Include unknowns"}
        featuresDescriptions={props.featuresDescriptions}
      ></MultipleSelectChipWrapper>
    ));
  }

  return <div className="select-chips">{toSelectChips()}</div>;
}

SelectChips.propTypes = {
  body: PropTypes.array,
  setBody: PropTypes.func,
  featuresDescriptions: PropTypes.array,
};

export default SelectChips;
