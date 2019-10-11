import React from 'react';

import styles from './styles/SensorContainer.module.css';

const SensorContainer = ({ title, children }) => (
  <div className={styles.container}>
    <div className={styles.title}>{title}</div>
    <div className={styles.contents}>{children}</div>
  </div>
);

export default SensorContainer;
