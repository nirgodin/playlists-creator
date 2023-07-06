import React from "react";
import CreatePlaylistNavigator from "./CreatePlaylistNavigator";
import _ from "underscore";
import LoadingSpinner from "../components/LoadingSpinner";
import { CREATE_PLAYLIST } from "../consts";
import FeaturedPlaylists from "../components/FeaturedPlaylists";
import PropTypes from "prop-types";
import { FEATURED_PLAYLISTS } from "../consts";

function AppNavigator(props) {
  if (_.isEqual(props.body, [])) {
    return <LoadingSpinner></LoadingSpinner>;
  } else if (props.currentPage === CREATE_PLAYLIST) {
    return (
      <CreatePlaylistNavigator
        body={props.body}
        setBody={props.setBody}
        defaultRequestBody={props.defaultRequestBody}
      ></CreatePlaylistNavigator>
    );
  } else if (props.currentPage === FEATURED_PLAYLISTS) {
    return <FeaturedPlaylists></FeaturedPlaylists>;
  } else {
    return <p>ABOUT US!</p>;
  }
}

AppNavigator.propTypes = {
  body: PropTypes.array,
  defaultRequestBody: PropTypes.array,
  setBody: PropTypes.func,
  currentPage: PropTypes.string,
};

export default AppNavigator;
