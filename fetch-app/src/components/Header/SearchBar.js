import React, { Component } from 'react';
import "./SearchBar.css"

class SearchBar extends React.Component {

  constructor(props) {
    super(props);
    this.state = {text : ''};
    this.updateText = this.updateText.bind(this);
  }

  updateText(event) {
    this.setState({text: event.target.text});
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <input
          type = "text"
          placeholder = "city or zip code ..."
          value = {this.state.text}
          onChange = {this.updateText}
        />
        <button type = "search">
          <i class="fa fa-search"></i>
        </button>
      </form>
    );
  }
}

export default SearchBar;
