import React, { Component } from 'react';
import { render } from 'react-dom';
import axios from 'axios';

// component that will display the data
import Overview from './Overview';

class Restore extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [], // will hold the results from our ajax call
      loading: false, // will be true when ajax request is running
    }
  }

  getPLCData(){
    axios.get(`${process.env.REACT_APP_PLC_SERVICE_URL}/plc`)
    .then((res) => { console.log("getPLCData method start");
    this.setState({ data: res.data.plc_db.tube_state_client }); })
    .catch((err) => { });
  };

  onClick = () => {
    /*
      Begin by setting loading = true, and use the callback function
      of setState() to make the ajax request. Set loading = false after
      the request completes.
    */
    this.setState({ loading: true }, () => { console.log("button clicked");
      axios.get(`${process.env.REACT_APP_PLC_SERVICE_URL}/plc/restore`)
        .then(result => {
          console.log("getPLCData start")
        this.getPLCData()
        console.log("getPLCData executed")
        this.setState({
          loading: false,
        })
        console.log("loading state to false")
        this.props.createMessage('Database restored', 'success')
      })
      .catch((err) => { 
        this.setState({ loading: false,})
        console.log("error")
        this.props.createMessage('Database restore failed', 'danger');
      });
    });
  }

  render() {
    const { data, loading } = this.state;

    return (
      <div>
        <h1 className="title is-1">Reactor Overview</h1>
        <hr/><br/>

        <button className={ 'button is-primary is-info' + (this.state.loading ? ' is-loading' : '')} onClick={this.onClick}>
          restore Database
        </button>

        {/*
          Check the status of the 'loading' variable. If true, then display
          nothing. Otherwise, display the results.
        */}
        {loading ? '' : <Overview tube_states={ data } />}
      </div>
    );
  }
}

export default Restore;