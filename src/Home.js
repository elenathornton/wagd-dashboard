import './Home.css';
import React from 'react';
import {Link} from 'react-router-dom';

function Home() {
    return (
        <div>
            <header className="App-header">
                <h1>Canine Athletics Dashboard</h1>
                <p>Upload your .csv file to view analytics!</p>
                <Link to="analytic"><button>Upload</button></Link>
            </header>
        </div>
    );
}
  
export default Home;