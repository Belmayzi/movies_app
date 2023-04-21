import {useState} from "react";


function navbar(props){
    
    return (
        <div className="nav_container">
            <div className="logo">
                <big>M</big><span>OVIESTAN</span>
            </div>
            <input onChange={props.change} value={props.qry} className="search" type="search" placeholder="Enter Keywords..." /> 
            <img src="./assets/magnifying-glass-solid.svg" />
        </div>
    )
}
export default navbar

