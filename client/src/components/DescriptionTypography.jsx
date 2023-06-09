import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { Box, Typography } from "@mui/material";
import { ENDPOINTS_DESCRIPTIONS, PROMPT } from "../consts";

function DescriptionTypography(props) {
  const [descriptionMapping, setDescriptionMapping] = useState(
    ENDPOINTS_DESCRIPTIONS[PROMPT]
  );

  useEffect(() => {
    const mapping = ENDPOINTS_DESCRIPTIONS[props.alignment];
    setDescriptionMapping(mapping);
  }, [props.alignment]);

  function toTypographies() {
    return descriptionMapping.map((typographyDetails) => (
      <Typography
        key={""}
        variant={typographyDetails["variant"]}
        sx={{ p: 2, width: "500px", paddingBottom: "0px", paddingTop: "5px", textAlign:typographyDetails['textAlign']}}
      >
        {typographyDetails["text"]}
      </Typography>
    ));
  }

  return (
    <div className="description-typographies">
      <Box sx={{ width: 550, display: "flex", flexDirection:"column", textAlign:"justify"}}>{toTypographies()}</Box>
    </div>
  );
}

DescriptionTypography.propTypes = {
  alignment: PropTypes.string,
};

export default DescriptionTypography;
