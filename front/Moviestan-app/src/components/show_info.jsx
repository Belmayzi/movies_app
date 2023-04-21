



export default function show_info(props){
    return(
        <div className="show_info">
                <div className="show_title">{props.name}</div>
                <div className="show_season"><span>Genre:</span> {props.genre}</div>
                <div className="show_rating">
                    <span>IMDb {props.rating}</span>
                </div>
                <div className="buttons">                   
                    <img className="play_btn" src="./assets/play-solid.svg"/>
                    <img className="plus_btn" src="./assets/plus-solid.svg"/>
                </div>
                <div className="show_description"><p>{props.description}</p></div>
            </div>
    )
}