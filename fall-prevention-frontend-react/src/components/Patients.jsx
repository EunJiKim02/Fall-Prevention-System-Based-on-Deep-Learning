
import { useEffect, useMemo, useState } from "react"
import { patients } from "../assets/dummyPatients"
import img from '../assets/patient_img.png';
import Header from "./Header";
import Warning from "./Warning";
import axios from "axios";

axios.defaults.withCredentials = true

export default function Patients() {
  const [isWarning, setIsWarning] = useState(false);
  const [warningInfo, setWarningInfo] = useState({warningText: "경고", detail: "환자가 위험합니다."});

  // useEffect(() => {
  //   const getWarningData = async () => { //경고 정보 가져오기
  //     try {
  //       const response = await axios.get('/patients/warning');
  //       setWarningInfo(response);
  //       if (warningInfo.iswarning === 1) //가져온 데이터에서 경고가 참이면
  //         setIsWarning(1);
  //     } catch (e) {
  //       console.log(e);
  //     }
  //   }
  //   getWarningData();

  //   const intervalId = setInterval(getWarningData, 5000);

  //   return () => clearInterval(intervalId);
  // }, []);

  const patientsList = useMemo(() => {
    return patients;
  }, []);
  const renderPatients = patientsList.map((p) => {
    return (
      <section className='patient' key={p.name}>
        <figure><img src={img}></img></figure>
        <h3>이름 : {p.name}</h3>
        <p>환자 위치 : {p.location}</p>
        <p>특이사항 : {p.detail}</p>
        <p>담당 간호사 : {p.nurse}</p>
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
  )
}
