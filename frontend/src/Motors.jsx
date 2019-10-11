import React from 'react';
import cx from 'classnames';

import styles from './styles/Motors.module.css';

const Motors = ({
  motorData,
  onChangeSpeedValue,
  onChangeSpeed,
  onKeyDown,
  onKeyUp
}) => (
  <div className={styles.container}>
    <div className={styles.steeringButtonsContainer}>
      <div className={styles.upDownButtonContainer}>
        <input
          id="w"
          type="button"
          value="&uarr;"
          onMouseDown={onKeyDown}
          onMouseUp={onKeyUp}
        />
      </div>
      <div className={styles.middleButtonsContainer}>
        <input
          id="a"
          type="button"
          value="&larr;"
          onMouseDown={onKeyDown}
          onMouseUp={onKeyUp}
        />
        <input
          id="s"
          type="button"
          value="&rarr;"
          onMouseDown={onKeyDown}
          onMouseUp={onKeyUp}
        />
      </div>
      <div className={styles.upDownButtonContainer}>
        <input
          id="d"
          type="button"
          value="&darr;"
          onMouseDown={onKeyDown}
          onMouseUp={onKeyUp}
        />
      </div>
    </div>
  </div>
);

const Motor = ({
  speed,
  onValueChange,
  onSpeedChange,
  title,
}) => (
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
