import React from "react";
import Button from "@mui/material/Button";
import Popover from "@mui/material/Popover";
import PopupState, { bindTrigger, bindPopover } from "material-ui-popup-state";
import PropTypes from "prop-types";
import DescriptionTypography from "./DescriptionTypography";

function Popup(props) {
  return (
    <div className="popup">
      <PopupState variant="popover" popupId="demo-popup-popover">
        {(popupState) => (
          <div>
            <Button variant="outlined" {...bindTrigger(popupState)}>
              {`${props.endpoint} Usage guidelines`}
            </Button>
            <Popover
              {...bindPopover(popupState)}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "center",
              }}
              transformOrigin={{
                vertical: "top",
                horizontal: "center",
              }}
            >
              <DescriptionTypography
                endpoint={props.endpoint}
              ></DescriptionTypography>
            </Popover>
          </div>
        )}
      </PopupState>
    </div>
  );
}

Popup.propTypes = {
  endpoint: PropTypes.string,
};

export default Popup;
