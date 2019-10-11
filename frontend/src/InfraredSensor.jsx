import React from 'react';

import styles from './styles/InfraredSensor.module.css';

const InfraredSensor = ({ distance }) => { 
  return (
    <div className={styles.container}>
      {Math.round((distance / 100) * 70)}
      cm
      <Bar distance={distance} />
    </div>
  )
};

const Bar = ({ distance }) => (
  <div className={styles.barContainer}>
    0
    <div className={styles.barBackground}>
      <div
        style={{ width: `${distance}%` }}
        className={styles.bar}
      />
    </div>
    70
  </div>
);

export default InfraredSensor;
