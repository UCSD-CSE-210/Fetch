import React from 'react';
import "./CheckBox.css"


class CheckBox extends React.Component {

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
            <div>
                <label>
                    <input className="checkbox"
                        type="checkbox"
                        value={label}
                        onClick={this.toggleCheckBoxChange}
                    />
                    {label}
                </label>
            </div>
        );
    }

}

export default CheckBox;
