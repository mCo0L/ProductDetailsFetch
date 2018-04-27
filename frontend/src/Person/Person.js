import React from 'react';

const person = (para) => {
    //run js in this using {}
    return (
    		<div>
    		<p> react in sublime { para.name } { para.age } </p>
    		<p>{para.children}</p>
    		</div>
    	)
};

export default person;