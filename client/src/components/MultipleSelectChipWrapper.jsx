import MultipleSelectChip from "./MultipleSelectChip";
import FilterCheckbox from "./Checkbox";

export default function MultipleSelectChipWrapper(props) {
    if (props.includesCheckbox) {
        return (
            <div className='row-items'>
                <MultipleSelectChip
                    title={props.title}
                    body={props.body}
                    setBody={props.setBody}
                ></MultipleSelectChip>
                <div className="filter-checkbox">
                    <FilterCheckbox label={props.checkboxLabel}></FilterCheckbox>
                </div>
            </div>
        )
    }
    else {
        <div>
            <MultipleSelectChip
                title={props.title}
                body={props.body}
                setBody={props.setBody}
            ></MultipleSelectChip>
        </div>
    }
};