import React, { Component } from "react";
import { render } from "react-dom";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import DropDownMenu from "material-ui/DropDownMenu";
import MenuItem from "material-ui/MenuItem";

import "./FacetsDropDown.css";

const menuStyles = {
  width: 300,
  fontSize: "30px"
};

class FacetsDropDown extends Component {
  constructor(props) {
    super(props);
    this.state = { value: 0 };
    this.facets = this.props.facets;
    this.updateFacets = this.props.updateFacets;
    this.plot = this.props.thisplot;
    this.facetsList = this.props.facets.map((facet, idx) => (
      <MenuItem value={idx} primaryText={facet.name} />
    ));
    this.onDropDownChange = this.onDropDownChange.bind(this);
  }

  //gets called from the DropDownMenu
  //  handleChange = (event, index, value) => {this.setState({value}); this.props.updateFacets(value,
  //      this.facets[value].name,
  //      'test',
  //      1
  //    )};
  handleChange = (event, index, value) => {
    this.onDropDownChange(value);
  };

  //this.props.updatePlot(value)
  //this.props.updatePlot(value)

  render() {
    return (
      <div>
        <center>
          <MuiThemeProvider>
            <DropDownMenu
              value={this.state.value}
              onChange={this.handleChange}
              style={menuStyles}
            >
              {this.facetsList}
            </DropDownMenu>
          </MuiThemeProvider>
        </center>
      </div>
    );
  }

  onDropDownChange(value) {
    this.setState({ value });
    this.props.updateFacets(value, this.facets[value].name, "test", 1);
  }
}

//render(<FacetsDropDown />, document.getElementById('root'));
export default FacetsDropDown;

//import "./FacetsDropDown.css";
//
//import React, { Component } from "react";
//import DropDownMenu from "material-ui/DropDownMenu";
//import MenuItem from 'material-ui/MenuItem';
//
//
//function FacetsDropDown(props) {
//  const facets = props.facets;
//  const updateFacets = props.updateFacets;
//  const handleChange = props.handleChange;
//  const facetsList = facets.map((facet, idx) => (
//      <MenuItem value={idx} primaryText={facet.name} />
//  ));
//  return (<DropDownMenu onChange={handleChange}>
//    {facetsList}
//  </DropDownMenu>
//
//  );
//}
//
//export default FacetsDropDown;
