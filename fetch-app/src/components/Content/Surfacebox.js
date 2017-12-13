import React from 'react';
import "./Surfacebox.css"


class Surfacebox extends React.Component {

    constructor(props) {
        super(props);
        this.checked = this.props.defaultChecked;
        if (this.checked === null)
            this.checked = false;
        this.toggleCheckBoxChange = this.toggleCheckBoxChange.bind(this);
    }

    toggleCheckBoxChange(event) {
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
                    defaultChecked={this.checked}
                />{label}
            </label>
        );
    }

}

export default Surfacebox;
