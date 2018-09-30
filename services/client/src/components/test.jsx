import React from 'react';

const Tubes = (props) => {
    return (
        <div className="">
            {
                props.tube_states.map((row, index) => {
                    return (
                        <div key={index} className="board-row">
                        {
                            row.map((element, idx) => {
                                return (
                                    <div key={idx} className={`square state${ element }`}>
                                        { element }
                                    </div>
                            )})

                        }

                        </div>
                    )
                })
            }
        </div>
    )
};

export default Tubes;
