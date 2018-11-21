import React from 'react';

const Overview = (props) => {
    return (
        <div className="column has-text-centered">
        <div className="reactor">
        
        {
            props.tube_states.map((row, index) => {
                return (
                    <div key={index} className="reactor-row">
                    {
                        row.map((element, idx) => {
                            return (
                                <div key={idx} className={`tube state${ element }`}>
                                   {/* { element }  values */ }
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