import {useState,useEffect} from "react";
import Show from './show.jsx'
import Showinfo from './show_info.jsx'
import showdata from "/data/tvshow_data.json"

function content(){

    const [shows,setShows]=useState([]);
    const [loading,setLoading]=useState(true);
    const [showInfo, setShowInfo]=useState(showdata[0]);

    useEffect (()=>{
            setShows(showdata);
            setLoading(false);
    },[])
    function HandleShowClick(show){
        setShowInfo(show);
    }
    return (
        <div className="content_container" >
            
            <Showinfo 
                rating={showInfo.ratingsSummary} 
                name={showInfo.titleText}
                genre={showInfo.genres} 
                description={showInfo.plot}/>

            <div className="shows_container "> 

                {!loading&&<div className="grid_container">
                    {shows.map(show=>{
                        return<Show
                            key={show.id}
                            img={show.primaryImage} 
                            name={show.titleText} 
                            HandleShowClick={()=>HandleShowClick(show)}  
                        />                        
                    })}
                </div>}
            </div>
        </div>
    )
};
export default content
