import { Route, Routes } from 'react-router-dom'
import './App.css'
import Login from './components/Login'
import Footer from './components/Footer'
import Patients from './components/Patients'
import WarningList from './components/WarningList'

function App() {
  return (
    <>
      <Routes>
        <Route path='/' element={<Login />} />
        <Route path='/patients' element={<Patients />} />
        <Route path='/warninglist' element={<WarningList />} />
      </Routes>
      <Footer/>
    </>
  )
}

export default App
