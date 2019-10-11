import React from 'react';
import cx from 'classnames';

import styles from './styles/Motors.module.css';

const Motors = ({ motorData, onChangeLeftValue, onChangeRightValue, onChangeLeftSpeed, onChangeRightSpeed, onChangeThrottle }) => (
  <div className={styles.container}>
    <Motor
      title="Left"
      speed={motorData.left}
      onValueChange={onChangeLeftValue}
      onSpeedChange={onChangeLeftSpeed}
    />
    <div className={styles.throttleContainer}>
      <input type="button"
             className={cx({
              [styles.pressed]: motorData.throttle,
              [styles.notPressed]: !motorData.throttle,})}
             value={motorData.throttle ? 'Motor On' : 'Motor Off'}  
             onClick={onChangeThrottle} />
    </div>
    <Motor
      title="Right"
      speed={motorData.right}
      onValueChange={onChangeRightValue}
      onSpeedChange={onChangeRightSpeed}
    />
  </div>
);

const Motor = ({ speed, onValueChange, onSpeedChange, title }) => (
  <div className={styles.motorContainer}>
    <div className={styles.sliderContainer}>
      <input
        type="range"
        className={styles.slider}
        orient="vertical"
        min="-100"
        max="100"
        value={speed}
        onMouseUp={onSpeedChange}
        onTouchEnd={onValueChange}
        onChange={onValueChange}
      />
      <span className={styles.speed}>{speed}</span>
    </div>
    <span className={styles.title}>{title}</span>
  </div>
);

export default Motors;
