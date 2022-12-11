import React, { useEffect } from "react";
import axios from "axios";
import { Routes, Route } from "react-router-dom"
import Home from './Home';
import Analytic from './Analytic';

function App() {
    useEffect(() => {
        axios
            .get("http://18.189.43.26:8080/")
            .then((response) => {
                console.log("SUCCESS", response);
            })
            .catch((error) => {
                console.log(error);
            });
    }, []);
    return (
        <div className="App">
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="analytic" element={<Analytic />} />
            </Routes>
        </div>
    );
}

export default App;
