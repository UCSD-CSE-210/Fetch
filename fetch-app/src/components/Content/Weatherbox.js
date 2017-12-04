import React from 'react';
import "./Weatherbox.css"


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
        return (
            <div>
                <p>{this.state.weather}</p>
                <p>{this.state.temp}</p>
            </div>
        );
    }

}

export default Weatherbox;
