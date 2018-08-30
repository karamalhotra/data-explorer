import React, { Component } from "react";
import { render } from "react-dom";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import DropDownMenu from "material-ui/DropDownMenu";
import MenuItem from "material-ui/MenuItem";

import "./FacetsDropDown.css";

const menuStyles = {
  width: 300,
  fontSize: "30px",
  paddingLeft: 220
};

class FacetsDropDown extends Component {
  constructor(props) {
    super(props);
    this.state = { value: 0 };
    this.center = this.props.center;
    this.facets = this.props.facets;
    this.updatePlot = this.props.updatePlot;
    this.updatePlot2 = this.props.updatePlot2;
    this.facetsList = this.props.facets.map((facet, idx) => (
      <MenuItem value={idx} primaryText={facet.name} />
    ));
    if (this.center == "2") {
      this.updatePlot2(0);
    } else {
      this.updatePlot(0);
    }

    this.onDropDownChange = this.onDropDownChange.bind(this);
    this.onDropDownChange2 = this.onDropDownChange2.bind(this);
  }

  handleChange = (event, index, value) => {
    this.onDropDownChange(value);
  };
  handleChange2 = (event, index, value) => {
    this.onDropDownChange2(value);
  };

  render() {
    if (this.center == "2") {
      return (
        <div>
          <MuiThemeProvider>
            <DropDownMenu
              value={this.state.value}
              onChange={this.handleChange2}
              style={menuStyles}
            >
              {this.facetsList}
            </DropDownMenu>
          </MuiThemeProvider>
        </div>
      );
    } else {
      return (
        <div>
          <MuiThemeProvider>
            <DropDownMenu
              value={this.state.value}
              onChange={this.handleChange}
              style={menuStyles}
            >
              {this.facetsList}
            </DropDownMenu>
          </MuiThemeProvider>
        </div>
      );
    }
  }

  onDropDownChange(value) {
    this.setState({ value });
    this.props.updatePlot(value);
  }

  onDropDownChange2(value) {
    this.setState({ value });
    this.props.updatePlot2(value);
  }
}

export default FacetsDropDown;
