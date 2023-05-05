import MinDistanceRangeSlider from "./MinDistanceRangeSlider"

const featureNames = [
    'Popularity',
    'Artist Popularity',
    'Danceability',
    'Energy',
    'Loudness',
    'Mode',
    'Speechiness',
    'Acousticness',
    'Instrumentalness',
    'Liveness',
    'Valence',
    'Tempo',
]

export default function RangeSliders(props) {
    const toRangeSliders = () => {
        return featureNames.map(
            featureName => <MinDistanceRangeSlider
                minDistance={0.1}
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