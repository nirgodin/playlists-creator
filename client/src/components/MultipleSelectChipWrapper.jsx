import React from "react";
import MultipleSelectChip from "./MultipleSelectChip";
import FilterCheckbox from "./Checkbox";
import InfoToolTip from "./InfoToolTip";
import PropTypes from "prop-types";

function MultipleSelectChipWrapper(props) {
  const selectChip = (
    <MultipleSelectChip
      title={props.title}
      body={props.body}
      setBody={props.setBody}
      effectCallback={props.effectCallback}
      multiple={props.multiple}
      possibleValues={props.possibleValues}
    ></MultipleSelectChip>
  );

  if (props.includesCheckbox) {
    return (
      <div className="select-chip-wrapper">
        <div className="row-items">
          <div className="select-chip-tooltip">
            <InfoToolTip
              featuresDescriptions={props.featuresDescriptions}
              title={props.title}
            ></InfoToolTip>
          </div>
          {selectChip}
          <div className="filter-checkbox">
            <FilterCheckbox
              title={props.title}
              body={props.body}
              setBody={props.setBody}
              label={props.checkboxLabel}
            ></FilterCheckbox>
          </div>
        </div>
      </div>
    );
  } else {
    <div>{selectChip}</div>;
  }
}

MultipleSelectChipWrapper.propTypes = {
  title: PropTypes.string,
  includesCheckbox: PropTypes.bool,
  featuresDescriptions: PropTypes.array,
  checkboxLabel: PropTypes.string,
  body: PropTypes.array,
  setBody: PropTypes.func,
  multiple: PropTypes.bool,
  possibleValues: PropTypes.array,
};

export default MultipleSelectChipWrapper;
