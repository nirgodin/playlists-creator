import React from "react";
import { Spotify } from "react-spotify-embed";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";

const playlistLinks = [
  "https://open.spotify.com/playlist/7tl7o5eRmr0Or5nMTYbhxd",
  "https://open.spotify.com/playlist/3OsNzkOT8c1q8Us2akJG8v",
  "https://open.spotify.com/playlist/4vVsm1wPutTPpKvYmbGvVv",
  "https://open.spotify.com/playlist/2kGSqBC8plc2BMDX69aLfA",
  "https://open.spotify.com/playlist/69sVKdyoUDgAjsozl7XNMY",
  "https://open.spotify.com/playlist/2V3lUk2Fx6fhCrOTSDCaiG",
];

function FeaturedPlaylists() {
  function toPlaylistIFrames() {
    return playlistLinks.map((playlistLink) => (
      <Grid key="" item xs={4}>
        <Spotify link={playlistLink} width={"400px"} />
      </Grid>
    ));
  }

  return (
    <div className="featured-playlists">
      <Box sx={{ flexGrow: 1, paddingTop: "20px", width: "1400px" }}>
        <Grid
          container
          spacing={5}
          direction="row"
          justifyContent="center"
          alignItems="center"
        >
          {toPlaylistIFrames()}
        </Grid>
      </Box>
    </div>
  );
}

export default FeaturedPlaylists;
