import React from 'react';

const Overview = (props) => {
    return (
        <div>
            <div className="reactor">
            {
                props.tube_states.map((row, index) => {
                    return (
                        <div key={index} className="reactor-row">
                        {
                            row.map((element, idx) => {
                                return (
                                    <div key={idx} className={`tube state${ element }`}>
                                       {/* { element }  /* shows the state ID in the square */} 
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