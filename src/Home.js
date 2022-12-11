import './Home.css';
import React from 'react';
import { Link } from 'react-router-dom';





class Home extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            imageURL: '',
        };

        this.handleUploadImage = this.handleUploadImage.bind(this);
    }

    handleUploadImage(ev) {
        console.log("upload")
        ev.preventDefault();

        const data = new FormData();
        data.append('file', this.uploadInput.files[0]);
        data.append('filename', this.fileName.value);

        fetch('http://18.189.43.26:8080/upload', {
            method: 'POST',
            body: data,
        }).then((response) => {
            response.json().then((body) => {
                this.setState({ imageURL: `http://18.189.43.26:8080/${body.file}` });
            });
        });
    }

    render() {
        return (
            <div>
                <header className="App-header">
                    <h1>Canine Athletics Dashboard</h1>
                    <p>Upload your .csv file to view analytics!</p>
                    <form onSubmit={this.handleUploadImage}>
                        <div>
                            <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
                        </div>
                        <div>
                            <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
                        </div>
                        <br />
                        <div>
                            {/* <Link to="analytic"> */}
                                <button>Upload</button>
                            {/* </Link> */}
                        </div>
                    </form>
                </header>
            </div>
        );
    }

}

export default Home;