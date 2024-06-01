# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## react+vite 실행

1. Node.js 설치

https://nodejs.org/ko/download/

2. 프로젝트 설정
   
fronted폴더(리액트)에 package.json이 있어야 함.

```
# package.json으로 패키지 설치
npm install

# vite 설치
npm i vite

# 소켓 사용할 때 필요한 라이브러리 설치
# package.json에 socket.io-client가 없으면 설치
npm i socket.io-client
```

3. 프로젝트 실행
```
npm run dev
```
