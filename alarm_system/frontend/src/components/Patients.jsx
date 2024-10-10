import { useEffect, useState } from "react";
import axios from "axios";
import Header from "./Header";
import { io } from "socket.io-client";
import { useNavigate } from "react-router-dom";

axios.defaults.withCredentials = true;

export default function Patients() {
  const [isWarning, setIsWarning] = useState(false);
  const [warningInfo, setWarningInfo] = useState({warningText: "경고", detail: "환자가 위험합니다."});
  const [patients, setPatients] = useState([]);
  const [warningPatient, setwarningPatient] = useState(0);
  const [socket, setSocket] = useState(io("http://localhost:5000"));
  const navigate = useNavigate();

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


  const handlePatientClick = (id) => {
    console.log(id)
    navigate(`/patient/${id}`);
  };

  const renderPatients = patients.length > 0 && patients.map((p) => {
    const imagePath = `/assets/PatientsImg/${p[5]}`;
    const cardClassName = `patient patient-border-${p[6]}`;
    return (
      <section className={cardClassName} key={p[0]} onClick={() => handlePatientClick(p[0])}>
        <figure><img src={imagePath} alt="patient" width={200} height={200} /></figure>
        
        <h3>{p[1]}</h3>
        <h5>환자 위치 : {p[2]}</h5>
        <p className="patient-contents">특이사항 : {p[4]}</p>

      </section>

    );
  });



  return (
  <>
  <Header />
      <link rel="preconnect" href="https://fonts.googleapis.com"></link>
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
      <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet"></link>
      <main>
        <br></br>
        <h1 className="info">환자 정보</h1>
        <br></br><br></br>
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
