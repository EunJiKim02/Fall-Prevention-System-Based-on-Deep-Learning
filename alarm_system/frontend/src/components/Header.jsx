import { Link, useLocation } from "react-router-dom";
import mainLogo from '../assets/main_logo.png'

export default function Header() {
  const location = useLocation();

  return (
    <>
    <header>
      <nav>
        <img className='header-mainlogo' src={mainLogo}></img>
        <ul>
          <li><Link to='/'>{location.pathname === '/' ? '로그인' : '로그아웃'}</Link></li>
          <li><Link to='/patients'>환자 정보</Link></li>
          <li><Link to='/warninglist'>알람 목록</Link></li>
        </ul>
      </nav>
      </header>
    </>
  )
}
