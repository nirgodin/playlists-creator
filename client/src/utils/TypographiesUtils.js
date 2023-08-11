import React from "react";
import { Typography } from "@mui/material";

export function toTypographies(descriptionMapping) {
  return descriptionMapping.map((typographyDetails) => (
    <Typography
      key={""}
      variant={typographyDetails["variant"]}
      sx={{
        p: 2,
        paddingBottom: "0px",
        paddingTop: "5px",
        textAlign: typographyDetails["textAlign"],
        color: typographyDetails["color"],
        fontWeight: typographyDetails["fontWeight"],
        fontFamily: typographyDetails["fontFamily"],
        width: typographyDetails["width"]
      }}
    >
      {typographyDetails["text"]}
    </Typography>
  ));
}
