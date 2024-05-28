import { useEffect, useState } from "react";
import axios from "axios";
import Header from "./Header";
import { io } from "socket.io-client";
import { useNavigate } from "react-router-dom";

export default function Paddition() {
    const [name, setName] = useState('');
    const [loc, setLoc] = useState('');
    const [nurse, setNurse] = useState('');
    const [significant, setSignificant] = useState('');
    const [currentStatus, setCurrentStatus] = useState('');
    const navigate = useNavigate();
    const handleAdd = () => {
        //ex. 서버로 환자 정보 보내기
        // let isLoginAuthorzied = false;
        // axios.post('http://localhost:5000/signin_request', { email, password }).then((res) => {
        // console.log("res", res.data.res)
        // if(res.data.res){
        //     navigate('/patients');
        // }
        // });
        const patientData = {
            name,
            loc,
            nurse,
            significant,
            current_status: currentStatus
        };

        axios.post('http://localhost:5000/add_patient', patientData)
            .then((res) => {
                console.log("환자 정보가 성공적으로 추가되었습니다:", res.data);
                navigate('/patients');
            })
            .catch((err) => {
                console.error("환자 정보 추가 중 오류 발생:", err);
            });
    }
    return (
    <>
    <Header />
    <main className="padd-card">
        <h1>환자 추가</h1>
        <div><input value={name} onChange={(e)=>setName(e.target.value)} placeholder="환자 이름"></input></div>
        <div><input value={loc} onChange={(e)=>setLoc(e.target.value)} placeholder="병실 호실"></input></div>
        <div><input value={nurse} onChange={(e)=>setNurse(e.target.value)} placeholder="담당 간호사 이름"></input></div>
        <div><input value={significant} onChange={(e)=>setSignificant(e.target.value)} placeholder="병명"></input></div>
        {/* <div><input value={current_status} onChange={(e) => setCurrentStatus(e.target.value)} placeholder="비밀번호를 입력하세요."></input></div> */}
        <div className='padd-div'>
            <p>낙상 위험 정도</p>
            <label>
                <input className='input-radio' type="radio" value="안전" checked={currentStatus === '안전'} onChange={() => setCurrentStatus('안전')}/>
                <span>안전</span>
            </label>
            <label>
                <input className='input-radio' type="radio" value="위험" checked={currentStatus === '위험'} onChange={() => setCurrentStatus('위험')}/>
                <span>주의</span>
            </label>
        </div>
        <button className='padd-btn' onClick={handleAdd}>환자 추가</button>
    </main>
    </>
    )
}