const PROMPT = 'prompt';
const CONFIGURATION = 'configuration';
const PHOTO = 'photo';
const FILTER_PARAMS = 'filterParams';
const INCLUDE_NAN = 'includeNan';
const PLAYLIST_DETAILS = 'playlistDetails';
const MIN = 'min';
const MAX = 'max';
const VALUE = 'value';
const IS_PUBLIC = 'isPublic';
const IS_SUCCESS = 'isSuccess';
const PLAYLIST_LINK = 'playlistLink';
const MESSAGE = 'message';
const ACCESS_CODE = 'accessCode';
const REQUEST_BODY = 'requestBody';

// Endpoints
const MIN_MAX_VALUES = 'minMaxValues';
const POSSIBLE_VALUES = 'possibleValues';
const FEATURES_NAMES = 'featuresNames';
const FEATURES_DESCRIPTIONS = 'featuresDescriptions';

// Style
const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
            backgroundColor: 'rgb(0, 30, 60)',
            color: 'white',
        },
    },
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
    MenuProps
};