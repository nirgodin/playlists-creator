import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Button from "@mui/material/Button";
import { ReactComponent as Logo } from "../static/logo.svg";
import PropTypes from "prop-types";
import { ABOUT, CREATE_PLAYLIST, FEATURED_PLAYLISTS } from "../consts";

const pages = [CREATE_PLAYLIST, FEATURED_PLAYLISTS, ABOUT];

function ResponsiveAppBar(props) {
  function handleClick(e) {
    props.setCurrentPage(e.currentTarget.textContent);
  }

  return (
    <AppBar position="static">
      <Container
        maxWidth="justify"
        sx={{ backgroundColor: "#7cff8f" }}
        disableGutters
      >
        <Toolbar disableGutters>
          <div className="row-items" style={{ paddingLeft: "5px" }}>
            <div className="svg-logo">
              <Logo />
            </div>
            <Box sx={{ paddingTop: "7px" }}>
              <Typography
                variant="h6"
                component="a"
                href="/"
                sx={{
                  mr: 2,
                  display: { xs: "none", md: "flex" },
                  fontFamily: "monospace",
                  fontWeight: 700,
                  letterSpacing: ".1rem",
                  color: "black",
                  textDecoration: "none",
                }}
              >
                Playlists
              </Typography>
              <Typography
                variant="h6"
                component="a"
                href="/"
                sx={{
                  mr: 2,
                  display: { xs: "none", md: "flex" },
                  fontFamily: "monospace",
                  fontWeight: 700,
                  letterSpacing: ".1rem",
                  color: "black",
                  textDecoration: "none",
                }}
              >
                Creator
              </Typography>
            </Box>
          </div>
          <Box sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={handleClick}
                sx={{
                  ":hover": { bgcolor: "#b4fabe" },
                  my: 2,
                  color: "black",
                  fontSize: 17,
                  fontWeight: 500,
                  margin: "15px"
                }}
              >
                {page}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

ResponsiveAppBar.propTypes = {
  currentPage: PropTypes.string,
  setCurrentPage: PropTypes.func,
};

export default ResponsiveAppBar;
