import React from 'react';
import cx from 'classnames';

import styles from './styles/TouchSensor.module.css';

const TouchSensor = ({ pressed }) => (
  <div
    className={cx(styles.container, {
      [styles.pressed]: pressed,
      [styles.notPressed]: !pressed,
    })}
  >
    {pressed ? 'Pressed' : 'Not pressed'}
  </div>
);

export default TouchSensor;
