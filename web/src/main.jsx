import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"
import "../node_modules/bootstrap-icons/font/bootstrap-icons.min.css";
import "./global.css"


import { Landing } from './pages/landing/Landing.jsx';



const App = () => (
  <React.StrictMode>
    <BrowserRouter>
      <Routes>


        <Route index element={<Landing />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);


ReactDOM.createRoot(document.getElementById('root')).render(<App />);
