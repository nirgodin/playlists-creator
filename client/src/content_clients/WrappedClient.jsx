import React from "react";

import {
  PLAYLIST_DETAILS,
  TIME_RANGE,
} from "../consts";
import PropTypes from "prop-types";
import MultipleSelectChipWrapper from "../components/MultipleSelectChipWrapper";
import { toCamelCase, toSnakeCase } from "../utils/StringUtils";
import _ from "underscore";

export default function WrappedClient(props) {
  function effectCallback(selectedOptions, title) {
    let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
    
    if (!_.isEqual(selectedOptions, [])) {
        const selectedTimeRange = toSnakeCase(selectedOptions[0]);
        newBody[PLAYLIST_DETAILS][TIME_RANGE] = selectedTimeRange;
        props.setBody([newBody]);    
    }
  }

  return (
    <div className="request-body">
      <div className="playlist-configuration">
        <div className="select-chips">
          <div className="multiple-select-chip">
            <MultipleSelectChipWrapper
              key={"Time Range"}
              title={"Time Range"}
              body={props.body}
              setBody={props.setBody}
              includesCheckbox={true}
              checkboxLabel={"Include unknowns"}
              featuresDescriptions={"bla"}
              effectCallback={effectCallback}
              multiple={false}
              possibleValues={["Short Term", "Medium Term", "Long Term"]}
            ></MultipleSelectChipWrapper>
          </div>
        </div>
      </div>
    </div>
  );
}

WrappedClient.propTypes = {
  body: PropTypes.array,
  setBody: PropTypes.func,
};
