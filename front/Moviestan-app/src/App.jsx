import { useEffect, useState } from 'react';
import Navbar from './components/navbar.jsx';
import Content from'./components/content.jsx';
import axios from 'axios'
import './App.css'

function App() {

  const [query,setQuery]=useState('')
  const handleChange =(e)=>{
      setQuery(e.target.value)
      console.log(query)
  }

  

  useEffect (()=>{
     axios.get(`http://127.0.0.1:5000/api/search/?q=${query}`)
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    });
  },[query])

 

  return (
    <div className="App">
      <Navbar change={handleChange} qry={query}/>
      <Content/>
    </div>
  )
}

export default App
