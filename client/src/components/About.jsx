import React from "react";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import GitHubIcon from "@mui/icons-material/GitHub";
import { Box, IconButton, Tooltip } from "@mui/material";
import Link from "@mui/material/Link";

function About() {
  function toIconButton(href, icon, title) {
    return (
      <Box sx={{ width: "50px" }}>
        <Tooltip title={title} placement="left">
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

  return (
    <div className="about-page">
      <p>About Us!</p>
      {toIconButton(
        "https://www.linkedin.com/in/nirgodin/",
        <LinkedInIcon fontSize="large" />,
        "Linkedin Page"
      )}
      {toIconButton(
        "https://github.com/nirgodin/playlists-creator",
        <GitHubIcon fontSize="large" />,
        "Github Repository"
      )}
    </div>
  );
}

export default About;
