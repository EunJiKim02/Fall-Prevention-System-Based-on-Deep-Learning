import { useEffect, useState } from "react";
import axios from "axios";
import img from '../assets/patient_img.png';
import Header from "./Header";
import Warning from "./Warning";

axios.defaults.withCredentials = true;

export default function Patients() {
  const [isWarning, setIsWarning] = useState(false);
  const [warningInfo, setWarningInfo] = useState({warningText: "경고", detail: "환자가 위험합니다."});
  const [patients, setPatients] = useState([]);

  const fetchAPI = async () => {
    try {
      const response = await axios.get("http://localhost:5000/patients");
      console.log(response.data);
      setPatients(response.data.data);
    } catch (error) {
      console.error('Error fetching patients:', error);
    }
  };

  useEffect(() => {
    fetchAPI();
  }, []);

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
        <button onClick={() => setIsWarning(!isWarning)}>경고 보기</button>
      </main>
      {isWarning && <Warning warningInfo={warningInfo} />}
    </>
  );
}
