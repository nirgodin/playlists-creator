import React from "react";
import { useState, useEffect } from "react";
import MultipleSelectChipWrapper from "./MultipleSelectChipWrapper";
import _ from "underscore";
import { FEATURES_NAMES, POSSIBLE_VALUES } from "../consts";
import { sendGetRequest } from "../utils/RequestsUtils";
import PropTypes from "prop-types";

function SelectChips(props) {
  const [featuresNames, setFeaturesNames] = useState([]);

  async function getFeaturesNames() {
    const featuresNames = await sendGetRequest(
      `${FEATURES_NAMES}/${POSSIBLE_VALUES}`,
      FEATURES_NAMES
    );
    setFeaturesNames(featuresNames);
  }

  useEffect(() => {
    if (_.isEqual(featuresNames, [])) {
      getFeaturesNames();
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
        checkboxLabel={"Include unkowns"}
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
