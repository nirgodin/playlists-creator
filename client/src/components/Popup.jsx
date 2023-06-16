import React from "react";
import Button from "@mui/material/Button";
import Popover from "@mui/material/Popover";
import PopupState, { bindTrigger, bindPopover } from "material-ui-popup-state";
import PropTypes from "prop-types";
import DescriptionTypography from "./DescriptionTypography";
import { convertCamelToTitle } from "../utils/StringUtils";

function Popup(props) {
  return (
    <div className="popup">
      <PopupState variant="popover" popupId="demo-popup-popover">
        {(popupState) => (
          <div>
            <Button sx={{fontWeight: 500, fontSize: 15, borderColor: "#6db4fc", color: "#6db4fc"}} variant="outlined" {...bindTrigger(popupState)}>
              {`${convertCamelToTitle(props.alignment)} Usage guidelines`}
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
                alignment={props.alignment}
              ></DescriptionTypography>
            </Popover>
          </div>
        )}
      </PopupState>
    </div>
  );
}

Popup.propTypes = {
  alignment: PropTypes.string,
};

export default Popup;
