import { useState } from "react";
import axios from "axios";
import Header from "./Header";
import { useNavigate } from "react-router-dom";

axios.defaults.withCredentials = true;

export default function Paddition() {
    const [name, setName] = useState('');
    const [loc, setLoc] = useState('');
    const [nurse, setNurse] = useState('');
    const [significant, setSignificant] = useState('');
    const [currentStatus, setCurrentStatus] = useState('');
    const [file, setFile] = useState(null);
    const navigate = useNavigate();

    const getRiskValue = (status) => {
        switch (status) {
            case '안전':
                return 0;
            case '주의':
                return 1;
            case '위험':
                return 2;
            default:
                return '';
        }
    };

    const handleAdd = () => {
        const risk = getRiskValue(currentStatus);

        const formData = new FormData();
        formData.append('name', name);
        formData.append('loc', loc);
        formData.append('nurse', nurse);
        formData.append('significant', significant);
        formData.append('risk', risk);
        formData.append('current_status', currentStatus);
        if (file) {
            formData.append('file', file);
        }

        axios.post('http://localhost:5000/add_patients', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then((res) => {
            console.log("res", res.data.res);
            if (res.data.res) {
                alert('환자 정보가 성공적으로 추가되었습니다.');
                navigate('/patients');
            } else {
                alert('환자 추가 실패: 정보를 확인하세요.');
            }
        }).catch((error) => {
            console.error("There was an error adding the patient!", error);
        });
    };

    return (
        <>
            <Header />
            <main className="padd-card">
                <link rel="preconnect" href="https://fonts.googleapis.com"></link>
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin></link>
                <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet"></link>
                <h1 className="info">환자 추가</h1>
                <br></br>
                <div><input value={name} onChange={(e) => setName(e.target.value)} placeholder=" 환자 이름"></input></div>
                <div><input value={loc} onChange={(e) => setLoc(e.target.value)} placeholder=" 병실 호실"></input></div>
                <div><input value={nurse} onChange={(e) => setNurse(e.target.value)} placeholder=" 담당 간호사 이름"></input></div>
                <div><input value={significant} onChange={(e) => setSignificant(e.target.value)} placeholder=" 주의 사항"></input></div>
                <div className='padd-div'>
                    <p>낙상 위험 정도</p>
                    <label>
                        <input className='input-radio' type="radio" value="안전" checked={currentStatus === '안전'} onChange={() => setCurrentStatus('안전')} />
                        <span>안전</span>
                    </label>
                    <label>
                        <input className='input-radio' type="radio" value="주의" checked={currentStatus === '주의'} onChange={() => setCurrentStatus('주의')} />
                        <span>주의</span>
                    </label>
                    <label>
                        <input className='input-radio' type="radio" value="위험" checked={currentStatus === '위험'} onChange={() => setCurrentStatus('위험')} />
                        <span>위험</span>
                    </label>
                </div>
                <div>
                    <p>환자 사진</p>
                    <input type="file" onChange={(e) => setFile(e.target.files[0])} />
                </div>
                <button className='padd-btn' onClick={handleAdd}>환자 추가</button>
            </main>
        </>
    );
}
