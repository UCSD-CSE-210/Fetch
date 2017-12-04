import React from 'react';
import './Weatherbox.css'


class Weatherbox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {temp : '', weather: ''};
    }
    
    componentDidMount() {
        this.setState({temp : '85', weather: 'Sunny'});

        // fetch("https://dog.ceo/api/breed/retriever/golden/images/random")
        //     .then(data => data.json())
        //     .then(data => {
        //         images.append(data.message);
        //         this.setState({imgs: data.message})
        //     });
        // this._renderMap();
    }

    render() {
        var icon = '';
        console.log(this.state.weather);
        switch (this.state.weather){
            case 'Sunny':
                icon = require('./weather/sunny.svg');
                break;
            case 'Cloudy':
                icon = require('./weather/cloudy.svg');
                break;
            case 'Snowy':
                icon = require('./weather/snowy.svg');
                break;
            case 'Rainy':
                icon = require('./weather/rainy.svg');
                break;
            case 'Windy':
                icon = require('./weather/windy.svg');
                break;
        }

        return (
            <div className="row weather">
                <img className="img-responsive weather-icon" src={icon} alt="weather icon"/>
                <div>                
                    <div>{this.state.weather}</div>
                    <div>{this.state.temp}</div>
                </div>
            </div>
        );
    }

}

export default Weatherbox;
