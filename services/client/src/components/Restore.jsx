import React, { Component } from 'react';
import axios from 'axios';

// component that will display the data
import Overview from './Overview';

class Restore extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loading: false, // will be true when ajax request is running
    }
  }

  onClick = () => {
    /*
      Begin by setting loading = true, and use the callback function
      of setState() to make the ajax request. Set loading = false after
      the request completes.
    */
    this.setState({ loading: true }, () => {
      axios.get(`${process.env.REACT_APP_PLC_SERVICE_URL}/plc/restore`)
        .then(result => {
        this.props.getPLCData()
        this.setState({
          loading: false,
        })
        this.props.createMessage('Database restored', 'success')
      })
      .catch((err) => { 
        this.setState({ loading: false})
        this.props.createMessage('Database restore failed', 'danger');
      });
    });
  }

  render() {
    var data = this.props.data;
    const { loading } = this.state;

    return (
      <div className="column has-text-centered">
        <h1 className="title is-1">Reactor Overview</h1>
        <hr/><br/>
          {/*
          Check the length of the 'data' variable. If it exists, the table will be shown, else we can show the restore button
        */}
        {data.length ?  '' : <button className={ 'button is-primary is-info' + (loading ? ' is-loading' : '')} onClick={this.onClick}> restore Database</button> }

        


        {/*
          Check the status of the 'loading' variable. If true, then display
          nothing. Otherwise, display the results.
        */}
        {loading ? '' : <Overview tube_states={ data} />}
      </div>
    );
  }
}

export default Restore;