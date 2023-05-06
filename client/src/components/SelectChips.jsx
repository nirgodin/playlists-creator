import MultipleSelectChipWrapper from "./MultipleSelectChipWrapper"

const featureNames = [
    'Language',
    'Main Genre'
]

export default function SelectChips(props) {
    function toSelectChips() {
        return featureNames.map(
            featureName => <MultipleSelectChipWrapper
                title={featureName}
                body={props.body}
                setBody={props.setBody}
                includesCheckbox={true}
                checkboxLabel={'Include unkowns'}
            ></MultipleSelectChipWrapper>
        )
    }

    return <div className="select-chips">
        {toSelectChips()}
    </div>
}