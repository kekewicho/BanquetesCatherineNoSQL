import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"
import "../node_modules/bootstrap-icons/font/bootstrap-icons.min.css";
import "./global.css"


import { Landing } from './pages/landing/Landing.jsx';
import { Login } from './pages/login/Login.jsx';
import { SessionProvider } from './providers/session.provider.jsx';
import { AppLayout } from './components/organisms/layout/layout.jsx';

import { RoleRouter } from './pages/principalView/principalView.jsx';

import { Index } from './pages/colaborador/Index.jsx';

import { EventoDetalle } from './pages/details/Evento.jsx';


const App = () => (
  <React.StrictMode>
    <SessionProvider>
      <BrowserRouter>
        <Routes>
          <Route index element={<Landing />} />
          <Route path="login" element={<Login />} />

          <Route path="app" element={<AppLayout />}>
            <Route index element={<RoleRouter />} />
            <Route path='colaborador' >
              <Route index element={<Index />} />
              <Route path='evento/:eventId' element={<EventoDetalle scope={"colaborador"} />} />
            </Route>
          </Route>

        </Routes>
      </BrowserRouter>
    </SessionProvider>
  </React.StrictMode>
);


ReactDOM.createRoot(document.getElementById('root')).render(<App />);
