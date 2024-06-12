import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import Header from "./Header";

axios.defaults.withCredentials = true;

export default function PatientDetail() {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPatientDetail = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/patient/${id}`);
        setPatient(response.data.patient);
      } catch (error) {
        console.error('Error fetching patient details:', error);
      }
    };
    fetchPatientDetail();
  }, [id]);

  const handleDelete = async () => {
    try {

      axios.post("http://localhost:5000/patient_delete", { id }).then((res) => {
        console.log("res", res.data.res)
        if(res.data.res){
          alert('삭제 성공')
        }
        else
          alert('삭제 실패 : 나중에 다시 시도해주세요.')
        navigate('/patients');
      });
    } catch (error) {
      console.error('Error deleting patient:', error);
      alert("환자 정보 삭제에 실패했습니다.");
    }
  };

  if (!patient) return <div>Loading...</div>;

  const cardClassName = `details detail-border-${patient.risk}`;

  return (
    <>
      <Header />
      <main className={cardClassName}>
        <link rel="preconnect" href="https://fonts.googleapis.com"></link>
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin></link>
        <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet"></link>
        
        <h3>{patient.name}</h3>
        <img src={`/assets/PatientsImg/${patient.img}`} alt="patient" width={200} height={200} />
        <br></br>
        <h6>환자 위치: {patient.loc}</h6>
        <h6>담당 간호사: {patient.nurse}</h6>
        <h6>특이사항: {patient.significant}</h6>
        <button onClick={handleDelete}>환자 삭제</button>
      </main>
    </>
  );
}
