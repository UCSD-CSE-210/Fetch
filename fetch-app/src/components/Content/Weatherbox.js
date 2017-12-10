import React from 'react';
import './Weatherbox.css'


class Weatherbox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {temp : '85', weather: 'Sunny', icon: ''};
    }
    
    componentDidMount() {
        // fetch("https://dog.ceo/api/breed/retriever/golden/images/random")
        //     .then(data => data.json())
        //     .then(data => {
        //         images.append(data.message);
        //         this.setState({imgs: data.message})
        //     });
        // this._renderMap();
        switch (this.state.weather){
            case 'Sunny':
                this.setState({icon: require('./weather/sunny.svg')});
                break;
            case 'Cloudy':
                this.setState({icon: require('./weather/cloudy.svg')});
                break;
            case 'Snowy':
                this.setState({icon: require('./weather/snowy.svg')});
                break;
            case 'Rainy':
                this.setState({icon: require('./weather/rainy.svg')});
                break;
            case 'Windy':
                this.setState({icon: require('./weather/windy.svg')});
                break;
            default:
                console.log('cannot identifiy '+this.state.weather);
        }
    }

    render() {
        return (
            <div className="row weather">
                <img className="img-responsive weather-icon" src={this.state.icon} alt="weather icon"/>
                <div>                
                    <div>{this.state.weather}</div>
                    <div>{this.state.temp}</div>
                </div>
            </div>
        );
    }

}

export default Weatherbox;
