// @flow

import React, { Component } from 'react';
import './App.css';

type AppProps = {
  debug: bool
};

class App extends Component<AppProps> {
  static defaultProps = {
    debug: false,
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Welcome to the <code>Miotono</code> UI.</h1>
        </header>
        <p className="App-intro">
          Content should go here.
        </p>
      </div>
    );
  }
}

export default App;
