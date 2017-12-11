import React from 'react';
import './Weatherbox.css'


class Weatherbox extends React.Component {
    constructor(props) {
        super(props);
        const {
            temperature,
            sunny,
            cloudy,
            rainy,
        } = props.weatherInfo;
        let weather = ''
        if (sunny) {
            weather = 'Sunny';
        }
        if (cloudy) {
            weather = 'Cloudy';
        }
        if (rainy) {
            weather = 'Rainy';
        }
        this.state = {
            temp : temperature, 
            weather: weather, 
            icon: '',
            shouldWarn: false,
            alertMsg: "",
        };
        this._showAlert= this._showAlert.bind(this);
    }
    
    componentDidMount() {
        switch (this.state.weather){
            case 'Sunny':
                this.setState({icon: require('./weather/sunny.svg')});
                if (this.state.temp > 75) {
                    this.setState({shouldWarn: true});
                    this.setState({alertMsg: "It might be too hot for your dog!"});
                }
                break;
            case 'Cloudy':
                this.setState({icon: require('./weather/cloudy.svg')});
                break;
            case 'Snowy':
                this.setState({icon: require('./weather/snowy.svg')});
                break;
            case 'Rainy':
                this.setState({icon: require('./weather/rainy.svg')});
                this.setState({shouldWarn: true});
                this.setState({alertMsg: "It's raining on this route now, you may want to reconsider!"});
                break;
            case 'Windy':
                this.setState({icon: require('./weather/windy.svg')});
                break;
            default:
                console.log('cannot identifiy '+this.state.weather);
        }
    }

    _showAlert(event){
        event.preventDefault();
        alert(this.state.alertMsg);
    }

    render() {
        return (
            <div className="row weather">
                {this.state.shouldWarn &&
                    <img className="img-responsive weather-icon" src={require("./weather/warning.svg")} onClick={this._showAlert} alt="weather icon"/>
                }
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
