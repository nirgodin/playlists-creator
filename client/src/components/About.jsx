import React from "react";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import GitHubIcon from "@mui/icons-material/GitHub";
import { Box, IconButton, Tooltip } from "@mui/material";
import Link from "@mui/material/Link";
import { toTypographies } from "../utils/TypographiesUtils";
import { ABOUT_PAGE_TEXT } from "../consts";

function About() {
  function toIconButton(href, icon, title, tooltipPlacement) {
    return (
      <Box sx={{ width: "50px", margin: "10px" }}>
        <Tooltip title={title} placement={tooltipPlacement}>
          <IconButton
            component={Link}
            href={href}
            variant="outlined"
            sx={{ color: "#6db4fc", ":hover": { bgcolor: "#00254a" } }}
          >
            {icon}
          </IconButton>
        </Tooltip>
      </Box>
    );
  }

  function getIconButtons() {
    return (
      <div className="about-page-icon-buttons">
        {toIconButton(
          "https://www.linkedin.com/in/nirgodin/",
          <LinkedInIcon sx={{ fontSize: "60px" }} />,
          "Linkedin Page",
          "left"
        )}
        {toIconButton(
          "https://github.com/nirgodin/playlists-creator",
          <GitHubIcon sx={{ fontSize: "60px" }} />,
          "Github Repository",
          "right"
        )}
      </div>
    );
  }

  function getDescription() {
    return (
      <Box
        sx={{
          width: 750,
          display: "flex",
          flexDirection: "column",
          textAlign: "justify",
        }}
      >
        {toTypographies(ABOUT_PAGE_TEXT)}
      </Box>
    );
  }

  return (
    <div className="about-page">
      <div className="about-page-description">{getDescription()}</div>
      {getIconButtons()}
    </div>
  );
}

export default About;
