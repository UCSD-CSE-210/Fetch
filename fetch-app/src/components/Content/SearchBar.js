import React from 'react';
import "./SearchBar.css";
import CheckBox from './CheckBox.js';
import Surfacebox from './Surfacebox.js';


const items = [
    'Is shaded?',
    'Has garbage can?',
    'Has parking lot?',
    'Show wildlife?',
]

const surfaceItems = [
    'trail',
    'road',
    'all',
]

class SearchBar extends React.Component {

    constructor(props) {
        super(props);
        this.state = {text : '', radius: ''};
        this.updatedRadius = this.updatedRadius.bind(this);
        this.updateText = this.updateText.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.selectedCheckBoxes = new Set();
        this.toggleCheckBox = this.toggleCheckBox.bind(this);
        this.surface = 'all';
        this.toggleSurfacebox = this.toggleSurfacebox.bind(this);
        this._geoError = this._geoError.bind(this);
        this._queryForm = this._queryForm.bind(this);
    }

    updateText(event) {
        this.setState({text: event.target.value});
    }

    updatedRadius(event){
        this.setState({radius: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        if (this.state.radius && navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(this._queryForm, this._geoError);
            return;
        }
        this._queryForm(null);
    }

    _geoError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                console.log("User denied the request for Geolocation.")
                break;
            case error.POSITION_UNAVAILABLE:
                console.log("Location information is unavailable.")
                break;
            case error.TIMEOUT:
                console.log("The request to get user location timed out.")
                break;
            default:
                console.log("An unknown error occurred.")
                break;
        }
        this._queryForm(null);
    }

    _queryForm(position) {

        //cannot test geolocation on my virtual machine;
        //will continue to test it on Chenyu's Side

        let params = {
            'address': this.state.text,
        }
        
        if (this.selectedCheckBoxes.has('Is shaded?')) {
            params['is_shade'] = true; 
        }
        if (this.selectedCheckBoxes.has('Has garbage can?')) {
            params['is_garbage_can'] = true;
        }
        if (this.selectedCheckBoxes.has('Has parking lot?')) {
            params['has_parking_lot'] = true;
        }
        if (this.surface && this.surface !== 'all') {
            params['surface'] = this.surface;
        }

        var shouldShow = {
            wildlife : this.selectedCheckBoxes.has('Show wildlife?'),
        }
        
        let esc = encodeURIComponent
        let query = Object.keys(params)
             .map(k => esc(k) + '=' + esc(params[k]))
             .join('&')
        fetch('http://127.0.0.1:5000/api/route?' + query)
                .then(data => data.json())
                .then(data => {this.props.callback(data.results, shouldShow)});
    }

    toggleCheckBox(label) {
        if (this.selectedCheckBoxes.has(label)) {
            this.selectedCheckBoxes.delete(label);
        } else {
            this.selectedCheckBoxes.add(label);
        }
    }

    toggleSurfacebox(label) {
        this.surface = label;
    }

    render() {
        var checkboxes = items.map(
            label => <CheckBox
                        label = {label}
                        callback = {this.toggleCheckBox}
                        key = {label}
                     />
        );

        var surfaceboxes = surfaceItems.map(
            label => <Surfacebox
                        label = {label}
                        callback = {this.toggleSurfacebox}
                        key = {label}
                     />
        );

        return (
            <div>
                <div className='fulldiv'>
                    <form onSubmit={this.handleSubmit}>
                        <input
                            className="address-input"
                            type = "text"
                            placeholder = " city or zip code ..."
                            value = {this.state.text}
                            onChange = {this.updateText}
                        />
                        <button type = "search">
                            <i className="fa fa-search"></i>
                        </button>
                    </form>
                </div>
                <div className='checkbox'>
                    {checkboxes}
                </div>
                <div className='surfacebox'>
                    <p>Surface type</p>
                    {surfaceboxes}
                </div>
                <div className='radiusbox'>
                    <label>Search radius</label>
                    <input type="text" className="radius-input"
                            placeholder = "Search radius (miles)"
                            value = {this.state.radius}
                            onChange = {this.updatedRadius}
                        />
                </div>
            </div>
    );
  }
}

export default SearchBar;
