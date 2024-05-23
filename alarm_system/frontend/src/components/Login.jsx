// import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import mainLogo from '../assets/main_logo.png';

// axios.defaults.withCredentials = true

export default function Login() {
  const [id, setId] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const handleLogin = () => {
    //ex. 서버로 아이디 비밀번호 보내기

    let isLoginAuthorzied = 0;
    axios.post('/login/request', { id, password }).then((res) => {
      console.log(res.data);
      isLoginAuthorzied = 1;
    });
    if (!isLoginAuthorzied)
      return;

    navigate('/patients');
  }

  return (
  <>
    {/* <h1 className="appname">낙상방지 환자 모니터링 서비스</h1> */}
    <main className="card">
      <img className='mainlogo'src={mainLogo} ></img>
      <div><input value={id} onChange={(e)=>setId(e.target.value)} placeholder="아이디를 입력하세요."></input></div>
      <div><input value={password} type='password' onChange={(e) => setPassword(e.target.value)} placeholder="비밀번호를 입력하세요."></input></div>
      <button className='login-btn' onClick={handleLogin}>로그인</button>
    </main>
  </>
  )
}
