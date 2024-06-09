import { Route, Routes } from 'react-router-dom'
import './App.css'
import Login from './components/Login'
import Footer from './components/Footer'
import Patients from './components/Patients'
import Paddition from './components/Paddition'
import PatientDetail from "./components/PatientDetail";
import axios from 'axios'
import { useEffect } from 'react'



function App() {

  const fetchAPI = async() => {
    const response = await axios.get("http://localhost:5000/");
    console.log(response.data.users);
  }

  useEffect( () => {
    fetchAPI();
  }, []);

  return (
    <>
      <Routes>
        <Route path='/' element={<Login />} />
        <Route path='/patients' element={<Patients />} />
        <Route path='/paddition' element={<Paddition />} />
        <Route path="/patient/:id" element={<PatientDetail />} />
      </Routes>
      <Footer/>
    </>
  )
}

export default App
