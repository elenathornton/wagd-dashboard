import React from "react";
import './Analytic.css';
import { withRouter } from './withRouter';
import { ResponsiveLineCanvas } from "@nivo/line";
import { ResponsiveScatterPlotCanvas } from "@nivo/scatterplot";
import { LTD } from 'downsample/methods/LTD';

function parseData(data, len) {
    const arr = new Float64Array(len + 5);
    Object.entries(data).forEach((entry) => {
        const [key, value] = entry;
        arr[key] = value;
    })
    console.log(arr);
    return arr;
}

class Analytic extends React.Component {
    constructor(props) {
        super(props);
        console.log(this.props.location.state);
        const chartwidth = 10000;
        let len = this.props.location.state.duration_ms / 10;
        console.log(len);
        const accelArr = LTD(parseData(JSON.parse(this.props.location.state.acceleration), len), chartwidth);
        console.log(accelArr);
        const yawXArr = LTD(parseData(JSON.parse(this.props.location.state.yaw_x), len), chartwidth);
        const yawYArr = LTD(parseData(JSON.parse(this.props.location.state.yaw_y), len), chartwidth);
        const pitchXArr = LTD(parseData(JSON.parse(this.props.location.state.pitch_x), len), chartwidth);
        const pitchYArr = LTD(parseData(JSON.parse(this.props.location.state.pitch_y), len), chartwidth);
        const rollXArr = LTD(parseData(JSON.parse(this.props.location.state.roll_x), len), chartwidth);
        const rollYArr = LTD(parseData(JSON.parse(this.props.location.state.roll_y), len), chartwidth);
        const distanceArr = LTD(parseData(JSON.parse(this.props.location.state.distance), len), chartwidth);
        const velocityArr = LTD(parseData(JSON.parse(this.props.location.state.velocity), len), chartwidth);
        let graph = {"id": "acceleration"};
        let arr = [];
        let graphYaw = {"id": "yaw"};
        let arrYaw = [];
        let graphPitch = {"id": "pitch"};
        let arrPitch = [];
        let graphRoll = {"id": "roll"};
        let arrRoll = [];
        let graphDistance = {"id": "distance"};
        let arrDistance = [];
        let graphVelocity = {"id": "velocity"};
        let arrVelocity = [];
        let time = 0.0;
        console.log(accelArr.length);
        for (let i = 0; i < accelArr.length; i++) {
            arr[i] = {
                x: time,
                y: accelArr[i]
            };
            arrYaw[i] = {
                x: yawXArr[i],
                y: yawYArr[i]
            }
            arrPitch[i] = {
                x: pitchXArr[i],
                y: pitchYArr[i]
            }
            arrRoll[i] = {
                x: rollXArr[i],
                y: rollYArr[i]
            }
            arrDistance[i] = {
                x: time,
                y: distanceArr[i]
            }
            arrVelocity[i] = {
                x: time,
                y: velocityArr[i]
            }
            time += (this.props.location.state.duration_ms / 1000 / accelArr.length);
        }
        graph["data"] = arr;
        graphYaw["data"] = arrYaw;
        graphPitch["data"] = arrPitch;
        graphRoll["data"] = arrRoll;
        graphDistance["data"] = arrDistance;
        graphVelocity["data"] = arrVelocity;
        console.log('after parse');

        this.state = {
            image: null,
            steps: this.props.location.state.steps,
            graph,
            graphYaw,
            graphPitch,
            graphRoll,
            graphDistance,
            graphVelocity
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
        const {image, steps, graph, graphYaw, graphPitch, graphRoll, graphDistance, graphVelocity} = this.state;
        return (
            <div className="Analytic">
                <h1>
                    Performance Analytics
                </h1>
                <h2>
                    Steps taken: <h3>{steps}</h3>
                </h2>
                <div className="Graph">
                <div className="Chart">
                    <h2>Acceleration Over Time</h2>
                    <ResponsiveLineCanvas 
                        data={[graph]}
                        margin={{ top: 50, right: 60, bottom: 50, left: 120 }}
                        xScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: true,
                            reverse: false
                        }}
                        yScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: true,
                            reverse: false
                        }}
                        axisLeft={{
                            format: '.2',
                            legend: 'acceleration',
                            legendOffset: -40,
                            legendPosition: 'middle'
                        }}
                        axisBottom={{
                            format: '.2',
                            legend: 'time (seconds)',
                            legendOffset: 36,
                            legendPosition: 'middle'
                        }}
                        pointSize={0.5}
                        pointColor="white"
                        colors={{ scheme: 'nivo' }}
                        theme={{
                            background: 'white'
                        }}
                    />
                </div>
                <div className="Chart">
                    <h2>Yaw</h2>
                    <ResponsiveScatterPlotCanvas 
                        data={[graphYaw]}
                        margin={{ top: 50, right: 60, bottom: 50, left: 120 }}
                        xScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                        }}
                        xFormat=">-.2f"
                        yScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                        }}
                        axisLeft={{
                            format: '.2',
                            legend: 'yaw_y',
                            legendOffset: -60,
                            legendPosition: 'middle'
                        }}
                        axisBottom={{
                            format: '.2',
                            legend: 'yaw_x',
                            legendOffset: 36,
                            legendPosition: 'middle'
                        }}
                        nodeSize={3}
                        colors={{ scheme: 'spectral' }}
                        theme={{
                            background: 'white'
                        }}
                    />
                </div>
                <div className="Chart">
                    <h2>Pitch</h2>
                    <ResponsiveScatterPlotCanvas 
                        data={[graphPitch]}
                        margin={{ top: 50, right: 60, bottom: 50, left: 120 }}
                        xScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: false,
                            reverse: false
                        }}
                        yScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: false,
                            reverse: false
                        }}
                        axisLeft={{
                            format: '.2',
                            legend: 'pitch_y',
                            legendOffset: -60,
                            legendPosition: 'middle'
                        }}
                        axisBottom={{
                            format: '.2',
                            legend: 'pitch_x',
                            legendOffset: 36,
                            legendPosition: 'middle'
                        }}
                        nodeSize={3}
                        colors={{ scheme: 'accent' }}
                        theme={{
                            background: 'white'
                        }}
                    />
                </div>
                <div className="Chart">
                    <h2>Roll</h2>
                    <ResponsiveScatterPlotCanvas 
                        data={[graphRoll]}
                        margin={{ top: 50, right: 60, bottom: 50, left: 120 }}
                        xScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: false,
                            reverse: false
                        }}
                        yScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: false,
                            reverse: false
                        }}
                        axisLeft={{
                            format: '.2',
                            legend: 'roll_y',
                            legendOffset: -60,
                            legendPosition: 'middle'
                        }}
                        axisBottom={{
                            format: '.2',
                            legend: 'roll_x',
                            legendOffset: 36,
                            legendPosition: 'middle'
                        }}
                        nodeSize={3}
                        colors={{ scheme: 'pastel2' }}
                        theme={{
                            background: 'white'
                        }}
                    />
                </div>
                <div className="Chart">
                    <h2>Distance</h2>
                    <ResponsiveLineCanvas 
                        data={[graphDistance]}
                        margin={{ top: 50, right: 60, bottom: 50, left: 120 }}
                        xScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: false,
                            reverse: false
                        }}
                        yScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: false,
                            reverse: false
                        }}
                        axisLeft={{
                            format: '.2s',
                            legend: 'Distance (meters)',
                            legendOffset: -55,
                            legendPosition: 'middle',
                            "format": '.2f'
                        }}
                        axisBottom={{
                            format: '.2s',
                            legend: 'Time (seconds)',
                            legendOffset: 36,
                            legendPosition: 'middle'
                        }}
                        pointSize={1}
                        colors={{ scheme: 'pastel1' }}
                        theme={{
                            background: 'white'
                        }}
                    />
                </div>
                <div className="Chart">
                    <h2>Velocity</h2>
                    <ResponsiveLineCanvas 
                        data={[graphVelocity]}
                        margin={{ top: 50, right: 60, bottom: 50, left: 120 }}
                        xScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: false,
                            reverse: false
                        }}
                        yScale={{
                            type: 'linear',
                            min: 'auto',
                            max: 'auto',
                            stacked: false,
                            reverse: false
                        }}
                        axisLeft={{
                            format: '.2s',
                            legend: 'Velocity (m/s)',
                            legendOffset: -40,
                            legendPosition: 'middle'
                        }}
                        axisBottom={{
                            format: '.2s',
                            legend: 'Time (seconds)',
                            legendOffset: 36,
                            legendPosition: 'middle'
                        }}
                        pointSize={1}
                        colors={{ scheme: 'pastel1' }}
                        theme={{
                            background: 'white'
                        }}
                    />
                </div>
                </div>
                <img src={image} alt="icons" />
            </div>
        );
    }
}
  
export default withRouter(Analytic);