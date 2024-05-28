import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import mainLogo from '../assets/main_logo.png';

axios.defaults.withCredentials = true

export default function Login() {
  const [email, setId] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const handleLogin = () => {
    //ex. 서버로 아이디 비밀번호 보내기

    let isLoginAuthorzied = false;
    axios.post('http://localhost:5000/signin_request', { email, password }).then((res) => {
      console.log("res", res.data.res)
      if(res.data.res){
        navigate('/patients');
      }
    });
  }

  return (
  <>
    {/* <h1 className="appname">낙상방지 환자 모니터링 서비스</h1> */}
    <main className="card">
      <img className='mainlogo'src={mainLogo} ></img>
      <h3>낙상 예방 환자 모니터링</h3>
      <div><input value={email} onChange={(e)=>setId(e.target.value)} placeholder="아이디를 입력하세요."></input></div>
      <div><input value={password} type='password' onChange={(e) => setPassword(e.target.value)} placeholder="비밀번호를 입력하세요."></input></div>
      <button className='login-btn' onClick={handleLogin}>로그인</button>
    </main>
  </>
  )
}
