
function show(props){
    
    return (  
        <div className="show_component " onClick={props.HandleShowClick} >
            <img src={props.img} />
            <span className="title">{props.name}</span>
        </div>
    )
}
export default show