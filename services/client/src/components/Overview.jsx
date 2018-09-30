import React from 'react';

const Overview = (props) => {
    return (
        <div>
            <h1 className="title is-1">Reactor Overview</h1>
            <hr/><br/>
            <div className="reactor">
            {
                props.tube_states.map((row, index) => {
                    return (
                        <div key={index} className="reactor-row">
                        {
                            row.map((element, idx) => {
                                return (
                                    <div key={idx} className={`tube state${ element }`}>
                                        { element }
                                    </div>
                            )})
                        }
                        </div>
                    )
                })
            }
            </div>
        </div>
    )
};

export default Overview;