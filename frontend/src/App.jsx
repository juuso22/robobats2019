import React from 'react';

import SensorContainer from './SensorContainer.jsx';
import ColourSensor from './ColourSensor.jsx';
import InfraredSensor from './InfraredSensor.jsx';
import TouchSensor from './TouchSensor.jsx';
import Motors from './Motors.jsx';

import styles from './styles/App.module.css';

const ROBOT_IP_ADDR = '10.10.90.209';
const ROBOT_PORT = 9000;

const robotUri = `ws://${ROBOT_IP_ADDR}:${ROBOT_PORT}`;

let websocket = null;

const sensorData = {
  colour_sensor: {
    rgb: [230, 230, 230],
    value: 'White',
    mode: 'RGB-RAW',
  },
  touch_sensor: false,
  infrared_sensor: 42,
  motors: {
    throttle: false,
    left: 0,
    right: 0,
  },
};

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: sensorData,
      colourConfig: {
        mode: 'COL-REFLECT',
        type: 'RGB',
      },
    };
  }

  componentDidMount() {
    this.connect();
  }

  /* UI update handlers */
  onLeftMotorValueChanged = data => {
    const speedLeft = Number(data.target.value);
    this.setState({
      data: {
        ...this.state.data,
        motors: { ...this.state.data.motors, left: speedLeft },
      },
    });
  };

  onRightMotorValueChanged = data => {
    const speedRight = Number(data.target.value);
    this.setState({
      data: {
        ...this.state.data,
        motors: { ...this.state.data.motors, right: speedRight },
      },
    });
  };

  /* ROBOT command handlers */
  onColourModeChange = data => {
    this.setState(
      {
        colourConfig: { ...this.state.colourConfig, mode: data.value },
      },
      () => {
        this.sendCommand('MODE', this.state.colourConfig.mode);
      }
    );
  };

  onColourSensorCalibrate = () => {
    this.sendCommand('CALIBRATE', {});
  };

  onThrottleChanged = () => {
    const throttle = !this.state.data.motors.throttle;
    this.setState(
      {
        data: {
          ...this.state.data,
          motors: { ...this.state.data.motors, throttle },
        },
      },
      () => {
        this.sendCommand('MOVETANK', this.state.data.motors);
      }
    );
  };

  onRightMotorSpeedChanged = () => {
    this.sendCommand('MOVETANK', this.state.data.motors);
  };

  onLeftMotorSpeedChanged = () => {
    this.sendCommand('MOVETANK', this.state.data.motors);
  };

  sendCommand(type, payload) {
    const message = {
      type,
      payload,
    };
    console.log(message);
    websocket.send(JSON.stringify(message));
  }

  isMotorOn() {
    return this.state.data.motors.throttle;
  }

  connect() {
    websocket = new WebSocket(robotUri);
    websocket.onopen = () => {
      console.log('CONNECTED');
    };
    websocket.onclose = () => {
      console.log('DISCONNECTED');
    };
    websocket.onmessage = message => {
      const sensorMessage = JSON.parse(message.data);
      this.setState({
        data: {
          ...this.state.data,
          colour_sensor: sensorMessage.colour_sensor,
          infrared_sensor: sensorMessage.infrared_sensor,
          touch_sensor: sensorMessage.touch_sensor,
        },
      });
    };
    websocket.onerror = message => {
      console.log(`Error; ${message.data}`);
    };
  }

  render() {
    const sensors = [
      [
        'Colour Sensor',
        <ColourSensor
          colours={this.state.data.colour_sensor}
          onModeChange={this.onColourModeChange}
          onCalibrate={this.onColourSensorCalibrate}
        />,
      ],
      [
        'Infrared Sensor',
        <InfraredSensor distance={this.state.data.infrared_sensor} />,
      ],
      ['Touch Sensor', <TouchSensor pressed={this.state.data.touch_sensor} />],
      [
        'Motors',
        <Motors
          motorData={this.state.data.motors}
          onChangeLeftValue={this.onLeftMotorValueChanged}
          onChangeRightValue={this.onRightMotorValueChanged}
          onChangeLeftSpeed={this.onLeftMotorSpeedChanged}
          onChangeRightSpeed={this.onRightMotorSpeedChanged}
          onChangeThrottle={this.onThrottleChanged}
        />,
      ],
    ];
    return (
      <div className={styles.container}>
        <main className={styles.sensors}>
          {sensors.map(([title, sensor]) => (
            <SensorContainer title={title}>{sensor}</SensorContainer>
          ))}
        </main>
        <div className={styles.footer}>
          <img
            className={styles.logo}
            src={require('./images/relex-logo-rgb.png')}
            alt="Relex Solutions"
          />
        </div>
      </div>
    );
  }
}

export default App;
