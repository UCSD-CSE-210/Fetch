import React from 'react';
import "./Surfacebox.css"


class Surfacebox extends React.Component {

    constructor(props) {
        super(props);
        this.isChecked = false;
        this.toggleCheckBoxChange = this.toggleCheckBoxChange.bind(this);
    }

    toggleCheckBoxChange(event) {
        this.isChecked = !this.isChecked;
        this.props.callback(this.props.label);
    }

    render() {
        const { label } = this.props;
        return (
            <label className='radio-inline'>
                <input
                    type="radio"
                    name="surface"
                    value={label}
                    onClick={this.toggleCheckBoxChange}
                />{label}
            </label>
        );
    }

}

export default Surfacebox;
