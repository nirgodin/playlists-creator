import Multiselect from 'multiselect-react-dropdown';
import './MultiSelectChip.css';

const MultipleSelectChip = (props) => {
    function getOptions() {
        let options = [];

        for (const [index, rawOption] of props.options.entries()) {
            const option = { name: rawOption, id: index }
            options.push(option)
        }

        return options
    }

    function onSelect(selectedList, selectedItem) {
        const selectedItems = selectedList.map((item) => item['name']);
        props.setSelectedOptions(selectedItems);
    }

    function onRemove(selectedList, removedItem) {
        const selectedItems = selectedList.map((item) => item['name']);
        props.setSelectedOptions(selectedItems);
    }

    return <div className='multi-select-dropdown'>
        <p>{props.title}</p>
        <Multiselect
            options={getOptions()} // Options to display in the dropdown
            onSelect={onSelect} // Function will trigger on select event
            onRemove={onRemove} // Function will trigger on remove event
            displayValue="name"
        />
    </div>
}

export default MultipleSelectChip