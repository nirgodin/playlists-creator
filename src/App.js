import logo from './logo.svg';
import './App.css';
import React from 'react';
import MinDistanceRangeSlider from './components/MinDistanceRangeSlider';
import MultipleSelectChip from './components/MultiSelectDropdown';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <MinDistanceRangeSlider
          minDistance={10}
          value={[0, 100]}
          label={'Popularity'}
        >
        </MinDistanceRangeSlider>
        <MultipleSelectChip label={'Genre'}></MultipleSelectChip>
      </header>
    </div>
  );
}

export default App;
