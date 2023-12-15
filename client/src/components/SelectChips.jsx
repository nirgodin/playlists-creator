import React from "react";
import { useState, useEffect } from "react";
import MultipleSelectChipWrapper from "./MultipleSelectChipWrapper";
import _ from "underscore";
import { FEATURES_NAMES, FEATURES_VALUES, FILTER_PARAMS, POSSIBLE_VALUES, VALUE } from "../consts";
import PropTypes from "prop-types";
import { toCamelCase } from "../utils/StringUtils";

function SelectChips(props) {
  const [featuresNames, setFeaturesNames] = useState([]);

  useEffect(() => {
    if (_.isEqual(featuresNames, [])) {
      setFeaturesNames(props.body[0][FEATURES_NAMES][POSSIBLE_VALUES]);
    }
  }, [featuresNames, setFeaturesNames]);

  function effectCallback(selectedOptions, title) {
    let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
    const camelCasedTitle = toCamelCase(title);
    newBody[FILTER_PARAMS][camelCasedTitle][VALUE] = selectedOptions;
    props.setBody([newBody]);
  }

  function getFeaturePossibleValues(featureName) {
      return props.body[0][FEATURES_VALUES][POSSIBLE_VALUES][featureName]
  }

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
        effectCallback={effectCallback}
        multiple={true}
        possibleValues={getFeaturePossibleValues(featureName)}
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
