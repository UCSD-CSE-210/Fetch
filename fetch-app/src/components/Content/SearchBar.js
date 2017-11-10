import React from 'react';
import "./SearchBar.css";
import CheckBox from './CheckBox.js';

const items = [
    'is shaded',
    'has garbage bag',
    'show wildlife',
]

class SearchBar extends React.Component {

    constructor(props) {
        super(props);
        this.state = {text : ''};
        this.updateText = this.updateText.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.selectedCheckBoxes = new Set();
        this.toggleCheckBox = this.toggleCheckBox.bind(this);
    }

    updateText(event) {
        this.setState({text: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        let params = {
            'address': this.state.text,
        }
        if (this.selectedCheckBoxes.has('is shaded')) {
            params['is_shade'] = true; 
        }
        if (this.selectedCheckBoxes.has('has garbage bag')) {
            params['is_garbage_can'] = true;
        }
        let esc = encodeURIComponent
        let query = Object.keys(params)
             .map(k => esc(k) + '=' + esc(params[k]))
             .join('&')
        var shouldShow = {
            wildlife : this.selectedCheckBoxes.has('show wildlife'),
        }
        fetch('http://localhost:5000/api/route?' + query)
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

    render() {
        var checkboxes = items.map(
            label => <CheckBox
                        label = {label}
                        callback = {this.toggleCheckBox}
                        key = {label}
                     />
        );

        return (
            <div>
                <div className='fulldiv'>
                    <form onSubmit={this.handleSubmit}>
                        <input
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
      </div>
    );
  }
}

export default SearchBar;
