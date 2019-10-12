import React from 'react';

import { Stream } from 'stream';
import styles from './styles/App.module.css';

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

  onMotorMove = data => {
    const steering = {
      type: 'MOVE',
      move: data.target.id,
    };
    console.log(steering);
    websocket.send(JSON.stringify(steering));
  };

  onMotorStop = () => {
    const steering = {
      type: 'MOVE',
      move: 'stop',
    };
    console.log(steering);
    websocket.send(JSON.stringify(steering));
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
}

const ROBOT_IP = '123';
const ROBOT_PORT = '9000';

const robotUri = `ws://${ROBOT_IP}:${ROBOT_PORT}`;

const websocket = new WebSocket(robotUri);
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

const sendCommand = command => {
  websocket.send(JSON.stringify(command));
};

let pressedKeys = [];

const onKeyDown = ({ key }) => {
  switch (key) {
    case 'a':
    case 'd':
    case 'a':
    case 't':
    case 'g':
    case 'w': {
      if (pressedKeys.includes(key)) return;
      pressedKeys.push(key);
      const command = {
        type: 'MOVE',
        move: key,
      };
      sendCommand(command);
      break;
    }
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6': {
      if (pressedKeys.includes(key)) return;
      pressedKeys.push(key);
      const command = {
        type: 'MODE',
        mode: key,
      };
      sendCommand(command);
      break;
    }
    default:
  }
};

const onKeyUp = ({ key }) => {
  const command = {
    type: 'MOVE',
    move: 'stop',
  };
  sendCommand(command);
  pressedKeys = pressedKeys.filter(x => x != key);
};

const SimpleController = () => (
  <div
    className={styles.container}
    onKeyDown={onKeyDown}
    onKeyUp={onKeyUp}
    tabIndex="0"
  />
);
export default SimpleController;

// export default App;
