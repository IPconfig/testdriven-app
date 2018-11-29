import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import axios from 'axios';

import UsersList from './components/UsersList';
import About from './components/About';
import Overview from './components/Overview';
import NavBar from './components/NavBar';
import Form from './components/forms/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';
import Message from './components/Message';
import Restore from './components/Restore';


class App extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      tube_states: [],
      title: 'ButterOverflow.io',
      isAuthenticated: false,
      messageName: null,
      messageType: null,
    };
    this.getPLCData = this.getPLCData.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
    this.loginUser = this.loginUser.bind(this);
    this.createMessage = this.createMessage.bind(this);
    this.removeMessage = this.removeMessage.bind(this);
  };
  componentWillMount() {
    if (window.localStorage.getItem('authToken')) {
      this.setState({ isAuthenticated: true });
    };
  };
  componentDidMount() {
    this.getUsers();
    this.getPLCData();
  };
  getPLCData(){
    axios.get(`${process.env.REACT_APP_PLC_SERVICE_URL}/plc`)
    .then((res) => { this.setState({ tube_states: res.data.tube_values_filtered }); })
    .catch((err) => { });
  };
  getUsers() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
    .then((res) => { this.setState({ users: res.data.data.users }); })
    .catch((err) => { });
  };
  logoutUser() {
    window.localStorage.clear();
    this.setState({ isAuthenticated: false });
  };
  loginUser(token) {
    window.localStorage.setItem('authToken', token);
    this.setState({ isAuthenticated: true });
    this.getUsers();
    this.createMessage('Welcome!', 'success');
  };
  createMessage(name='Sanity Check', type='success') {
    this.setState({
      messageName: name,
      messageType: type
    });
    setTimeout(() => {
      this.removeMessage();
    }, 3000);
  };
  removeMessage() {
    this.setState({
      messageName: null,
      messageType: null
    });
  };
  render() {
    return (
      /*
      <div>
        <NavBar
          title={this.state.title}
          isAuthenticated={this.state.isAuthenticated}
        />
        */
        <section className="section">
          <div className="container">
            {this.state.messageName && this.state.messageType &&
              <Message
                messageName={this.state.messageName}
                messageType={this.state.messageType}
                removeMessage={this.removeMessage}
              />
            }
            <div className="columns is-centered">
             {/* <div className="column is-half"> */ }
                <br/>
                <Switch>
                  <Route exact path='/' render={() => (
                    /*<UsersList
                      users={this.state.users}
                    />*/
                    <Overview tube_states={this.state.tube_states}/>
                  )} />
                  <Route exact path='/about' component={About}/>
                  <Route exact path='/overview' render={() => (
                    <Overview tube_states={this.state.tube_states}/>
                  )} />
                  <Route exact path='/restore' render={() => (
                    <Restore data={this.state.tube_states}
                    createMessage={this.createMessage}/>
                  )} />
                  <Route exact path='/register' render={() => (
                    <Form
                      formType={'Register'}
                      isAuthenticated={this.state.isAuthenticated}
                      loginUser={this.loginUser}
                      createMessage={this.createMessage}
                    />
                  )} />
                  <Route exact path='/login' render={() => (
                    <Form
                      formType={'Login'}
                      isAuthenticated={this.state.isAuthenticated}
                      loginUser={this.loginUser}
                      createMessage={this.createMessage}
                    />
                  )} />
                  <Route exact path='/logout' render={() => (
                    <Logout
                      logoutUser={this.logoutUser}
                      isAuthenticated={this.state.isAuthenticated}
                    />
                  )} />
                  <Route exact path='/status' render={() => (
                    <UserStatus
                      isAuthenticated={this.state.isAuthenticated}
                    />
                  )} />
                </Switch>
           {/*   </div>  div of the is-half column */ }
            </div>
          </div>
        </section>
      //</div>
    )
  }
};

export default App;