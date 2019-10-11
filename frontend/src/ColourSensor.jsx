import React from 'react';

import Dropdown from 'react-dropdown';

import styles from './styles/ColourSensor.module.css';
import '!style-loader!css-loader!react-dropdown/style.css';

const dropdownModeOptions = [
  'COL-REFLECT',
  'COL-AMBIENT',
  'COL-COLOR',
  'REF-RAW',
  'RGB-RAW',
];

const ColourSensor = ({
  colours, onModeChange, onCalibrate,
}) => (
  <div className={styles.container}>
    <div className={styles.dropdownContainer}>
      <span className={styles.dropdownTitle}>Mode</span>
      <Dropdown
        className={styles.dropdown}
        options={dropdownModeOptions}
        onChange={onModeChange}
        value={colours.mode}
        placeholder="Select mode"
      />
    </div>
    <div className={styles.colourContainer}>
      <span className={styles.dropdownTitle}>Colour</span>
      <Colour colours={colours} mode={colours.mode} />
    </div>
    <div className={styles.buttonContainer}>
      <span className={styles.dropdownTitle}/>
      <input type="button" 
             value="Calibrate" 
             onClick={onCalibrate} />
    </div>
  </div>
);

const Colour = ({ colours, mode }) => {
  const cssColour = () => {
    if (mode === 'COL-COLOR') {
      return colours.value.toLowerCase();
    }
    if (mode === 'COL-AMBIENT') {
      const colorVal = (colours.value / 100) * 255;
      return `rgb(${colorVal},${colorVal},${colorVal})`;
    }
    if (mode === 'COL-REFLECT') {
      const colorVal = (colours.value / 100) * 255;
      return `rgb(${colorVal},${colorVal},${colorVal})`;
    }
    return `rgb(${colours.rgb})`;
  };

  return (
    <div style={{ backgroundColor: cssColour() }} className={styles.colour}>
      <span style={{ color: cssColour() }} className={styles.colourText}>
        {(() => ((mode === 'COL-REFLECT' || mode === 'COL-AMBIENT') ? `${colours.value} %` : colours.value.toString()))()}
      </span>
    </div>
  );
};

export default ColourSensor;
