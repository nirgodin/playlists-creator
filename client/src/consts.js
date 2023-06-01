const PROMPT = "prompt";
const CONFIGURATION = "configuration";
const PHOTO = "photo";
const FILTER_PARAMS = "filterParams";
const INCLUDE_NAN = "includeNan";
const PLAYLIST_DETAILS = "playlistDetails";
const MIN = "min";
const MAX = "max";
const VALUE = "value";
const IS_PUBLIC = "isPublic";
const IS_SUCCESS = "isSuccess";
const PLAYLIST_LINK = "playlistLink";
const MESSAGE = "message";
const ACCESS_CODE = "accessCode";
const REQUEST_BODY = "requestBody";

// Endpoints
const MIN_MAX_VALUES = "minMaxValues";
const POSSIBLE_VALUES = "possibleValues";
const FEATURES_NAMES = "featuresNames";
const FEATURES_DESCRIPTIONS = "featuresDescriptions";

// Style
const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
      backgroundColor: "rgb(0, 30, 60)",
      color: "white",
    },
  },
};

// Photo dropzone style
const PHOTO_DROPZONE_BASE_STYLE = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "20px",
  borderWidth: 2,
  borderRadius: 2,
  borderColor: "#1976d2",
  borderStyle: "dashed",
  backgroundColor: "rgb(0, 30, 60)",
  color: "white",
  outline: "none",
  transition: "border .24s ease-in-out",
  width: "350px",
  margin: "auto",
  fontSize: 16,
};

const PHOTO_DROPZONE_FOCUSED_STYLE = {
  borderColor: "#2196f3",
};

const PHOTO_DROPZONE_ACCEPT_STYLE = {
  borderColor: "#00e676",
};

const PHOTO_DROPZONE_REJECT_STYLE = {
  borderColor: "#ff1744",
};

const PHOTO_DROPZONE_THUMB_CONTAINER_STYLE = {
  display: "flex",
  flexDirection: "row",
  flexWrap: "wrap",
  marginTop: 16,
};

const PHOTO_DROPZONE_THUMB_STYLE = {
  display: "inline-flex",
  borderRadius: 2,
  border: "1px solid #eaeaea",
  marginBottom: 8,
  marginRight: 8,
  width: 100,
  height: 100,
  padding: 4,
  boxSizing: "border-box",
  margin: "auto",
};

const PHOTO_DROPZONE_THUMB_INNER_STYLE = {
  display: "flex",
  minWidth: 0,
  overflow: "hidden",
};

const PHOTO_DROPZONE_IMAGE_STYLE = {
  display: "block",
  width: "auto",
  height: "100%",
};

export {
  PROMPT,
  CONFIGURATION,
  PHOTO,
  FILTER_PARAMS,
  INCLUDE_NAN,
  PLAYLIST_DETAILS,
  MIN,
  MAX,
  MIN_MAX_VALUES,
  POSSIBLE_VALUES,
  VALUE,
  IS_PUBLIC,
  FEATURES_NAMES,
  FEATURES_DESCRIPTIONS,
  IS_SUCCESS,
  PLAYLIST_LINK,
  MESSAGE,
  ACCESS_CODE,
  REQUEST_BODY,
  MenuProps,
  PHOTO_DROPZONE_IMAGE_STYLE,
  PHOTO_DROPZONE_THUMB_INNER_STYLE,
  PHOTO_DROPZONE_THUMB_STYLE,
  PHOTO_DROPZONE_THUMB_CONTAINER_STYLE,
  PHOTO_DROPZONE_REJECT_STYLE,
  PHOTO_DROPZONE_ACCEPT_STYLE,
  PHOTO_DROPZONE_FOCUSED_STYLE,
  PHOTO_DROPZONE_BASE_STYLE,
};
