import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { Box } from "@mui/material";
import { ENDPOINTS_DESCRIPTIONS, PROMPT } from "../consts";
import { toTypographies } from "../utils/TypographiesUtils";

function DescriptionTypography(props) {
  const [descriptionMapping, setDescriptionMapping] = useState(
    ENDPOINTS_DESCRIPTIONS[PROMPT]
  );

  useEffect(() => {
    const mapping = ENDPOINTS_DESCRIPTIONS[props.alignment];
    setDescriptionMapping(mapping);
  }, [props.alignment]);

  return (
    <div className="description-typographies">
      <Box sx={{ width: 550, display: "flex", flexDirection:"column", textAlign:"justify"}}>{toTypographies(descriptionMapping)}</Box>
    </div>
  );
}

DescriptionTypography.propTypes = {
  alignment: PropTypes.string,
};

export default DescriptionTypography;
