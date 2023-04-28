import MinDistanceRangeSlider from "./MinDistanceRangeSlider"

const audioFeatures = [
    'Danceability',
    'Energy',
    'Loudness',
    'Mode',
    'Speechiness',
    'Acousticness',
    'Instrumentalness',
    'Liveness',
    'Valence',
    'Tempo'
]

export default function AudioFeaturesSliders(props) {
    const toRangeSliders = () => {
        return audioFeatures.map(
            featureName => <MinDistanceRangeSlider
                minDistance={10}
                title={featureName}
                body={props.body}
                setBody={props.setBody}
            ></MinDistanceRangeSlider>
        )
    }

    return <div>
        {toRangeSliders()}
    </div>
}