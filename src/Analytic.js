import React from "react";
import './Analytic.css';

class Analytic extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            image: null
        }
      }
    
    componentDidMount() {
        fetch("https://dog.ceo/api/breeds/image/random")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        image: result.message
                    })
                }
            )
    }

    render() {
        const {image} = this.state;
        return (
            <div className="Analytic">
                <h1>
                    Here's your dog pic:
                </h1>
                <img src={image} alt="icons" />
            </div>
        );
    }
}
  
export default Analytic;