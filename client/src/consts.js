const PROMPT = "prompt";
const EXISTING_PLAYLIST = "existingPlaylist";
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
const FEATURES_VALUES = "featuresValues";

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

const PROMPT_DESCRIPTION = [
  {
    variant: "h6",
    text: "Using Prompts",
    textAlign: "center",
  },
  {
    variant: "p",
    text: "A prompt is a short statement that is provided as input to a language model in order to generate a response. Your prompt may include anything, but will work best if you follow these rules:",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: '1. Your prompt should include the terminology the model is familiar with. The more you use the terminology used on the "Configuration" page, the more likely the model is to understand you.',
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "2. Your prompt should not be too short or long. Details, explanations, and examples help the model understand you better, but a prompt that is too lengthy will be rejected as it exceeds the maximum number of words allowed.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "3. Your prompt will also be used to generate a custom playlist cover. You may include figurative descriptions in it, but ensure they do not replace the descriptions of the songs themselves; otherwise, we will not be able to create your playlist.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "",
    textAlign: "justify",
  },
];

const PHOTO_DESCRIPTION = [
  {
    variant: "h6",
    text: "Using Photos",
    textAlign: "center",
  },
  {
    variant: "p",
    text: "Simply drag and drop a festival lineup or any other picture into the designated area. Our algorithm will identify the artists' names from the photo and curate a playlist featuring their most popular tracks.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "Here are some guidelines to maximize the utility of this tool:",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "1. Currently, only English is supported as the language. In the event that you provide photos containing languages other than English, it may have a negative impact on the performance, potentially resulting in the inability to generate your playlist successfully.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "2. For optimal results, the model performs best when provided with images featuring dark backgrounds and light text. If you provide photos with light backgrounds, the model may struggle to detect the artists' names accurately, resulting in a failure to create your playlist.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "3. The model's training focused on identifying artists' names, rather than songs or albums. Therefore, it is essential to ensure that your photo includes the names of the artists. Without this information, the model will be unable to generate a playlist for you.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "",
    textAlign: "justify",
  },
];

const CONFIGURATION_DESCRIPTION = [
  {
    variant: "h6",
    text: "Using Configuration",
    textAlign: "center",
  },
  {
    variant: "p",
    text: "Configuration provides the optimal means to finely control every aspect of your playlist, while also being the quickest method. By dragging each slider and selecting options from the dropdown menus, you can precisely define the desired characteristics of your playlist. If you're unsure about the meaning of a particular field, simply hover over the tooltip located to its left for clarification.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "However, please be aware that selecting overly specific criteria may lead to the algorithm's inability to identify any relevant songs, resulting in a failure to generate your playlist.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "",
    textAlign: "justify",
  },
];

const EXISTING_PLAYLIST_DESCRIPTION = [
  {
    variant: "h6",
    text: "Using Existing Playlist",
    textAlign: "center",
  },
  {
    variant: "p",
    text: "Are you finding your current playlist enjoyable but starting to feel like you've heard it all? Then this is just what you need.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "The `Existing Playlist` feature allows you to input the URL of a playlist you already have and receive a fresh new playlist that captures the essence of the one you provided.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "To experience this feature, simply visit your playlist page on Spotify, click on the Share button, select \"Copy link to playlist\" and paste it into the text box provided below.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "Please be aware that if you submit a playlist containing more than 50 songs, only a random selection of 50 songs will be chosen to represent the playlist.",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "Sit back and enjoy!",
    textAlign: "justify",
  },
  {
    variant: "p",
    text: "",
    textAlign: "justify",
  },
];

const ENDPOINTS_DESCRIPTIONS = {
  [CONFIGURATION]: CONFIGURATION_DESCRIPTION,
  [PROMPT]: PROMPT_DESCRIPTION,
  [PHOTO]: PHOTO_DESCRIPTION,
  [EXISTING_PLAYLIST]: EXISTING_PLAYLIST_DESCRIPTION,
};

export {
  PROMPT,
  EXISTING_PLAYLIST,
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
  FEATURES_VALUES,
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
  ENDPOINTS_DESCRIPTIONS,
};
