import { useEffect, useState } from "react";
import axios from "axios";
import img from '../assets/patient_img.png';
import Header from "./Header";
import { io } from "socket.io-client";

axios.defaults.withCredentials = true;

export default function Patients() {
  const [isWarning, setIsWarning] = useState(false);
  const [warningInfo, setWarningInfo] = useState({warningText: "경고", detail: "환자가 위험합니다."});
  const [patients, setPatients] = useState([]);
  const [warningPatient, setwarningPatient] = useState(0);
  const [socket, setSocket] = useState(io("http://localhost:5000"));

  const fetchAPI = async () => {
    try {
      const response = await axios.get("http://localhost:5000/patients");
      console.log(response.data);
      setPatients(response.data.patients);
      const socket = io("http://localhost:5000");
      setSocket(socket)
    } catch (error) {
      console.error('Error fetching patients:', error);
    }
  };

  useEffect(() => {
    fetchAPI();
  }, []);

  useEffect(() => {

    socket.on('warning', (data) => {
      console.log('Warning received:', data);
      setWarningInfo({ warningText: "경고", detail: `환자 ID ${data.patient_id}: ${data.message}` });
      setwarningPatient(data.patient_id)
      setIsWarning(true);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleClose = () => {
    setIsWarning(false);
    console.log(socket)
    if (socket) {
      console.log('warning_close')
      socket.emit('warning_close', { message: warningPatient });
    }
  };

  const renderPatients = patients.length > 0 && patients.map((p) => {
    return (
      <section className='patient' key={p[0]}>
        <figure><img src={img} alt="patient" /></figure>
        <h3>이름 : {p[1]}</h3>
        <p>환자 위치 : {p[2]}</p>
        <p>특이사항 : {p[3]}</p>
        <p>담당 간호사 : {p[4]}</p>
      </section>
    );
  });

  return (
  <>
  <Header />
      <main>
        <h1>환자 정보</h1>
        <div className="patients">
          {renderPatients}
        </div>
      </main>
  
    { isWarning ? (
      <section className="warning">
        <button className="warning-btn" onClick={handleClose}>✖️</button>
        <h1 style={{ color: 'red', fontSize: '100px' }}>⚠️{warningInfo.warningText}</h1>
        <h1>{warningInfo.detail}</h1>
      </section>
    ) : null }
  </>
  );
}
