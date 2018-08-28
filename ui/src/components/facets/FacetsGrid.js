//import "./FacetsGrid.css";
//import FacetCard from "./FacetCard";
//
//import React, { Component } from "react";
//import { GridList, GridTile } from "material-ui/GridList";
//
//function FacetsGrid(props) {
//  const facets = props.facets;
//  const updateFacets = props.updateFacets;
//  const facetsList = facets.map(facet => (
//    <GridTile key={facet.name}>
//      <FacetCard facet={facet} updateFacets={updateFacets} />
//    </GridTile>
//  ));
//  return (
//    <GridList className="gridList" cols={3} cellHeight="auto" padding={1}>
//      {facetsList}
//    </GridList>
//  );
//}
//
//export default FacetsGrid;

///////////////////V2/////////////////////////////////////
import "./FacetsGrid.css";
import FacetCard from "./FacetCard";

import React, { Component } from "react";
import { GridList, GridTile } from "material-ui/GridList";
import Plot from "react-plotly.js";
import FacetsDropDown from "./FacetsDropDown";

function FacetsGrid(props) {
  const facets = props.facets;
  const updateFacets = props.updateFacets;
  const Data = props.allData;
  const plot = props.plot;
  var facet = facets[0];
  //var test = facet['values'][0]
  //var updatePlot = props.updatePlot
  //document.write(plot)
  //document.write(typeof Data)
  //  document.write("KB")
  //document.write(updatePlot)
  //var myJSON = JSON.stringify(Data);
  //document.write(Object.keys(Data))

  //  document.write(Object.values(Data))
  //  for (var i in facet) {
  //        document.write(i+":" + facet[i]);
  //  }

  //  const facetsList = facets.map(facet => (
  //    <GridTile key={facet.name}>
  //      <FacetCard facet={facet} updateFacets={updateFacets} />
  //    </GridTile>
  //  ));

  //document.write(plot)
  //console.log('My object : ' + facets[0])

  var layout = { width: 320, height: 240, title: props.plot };
  var trace = {
    x: Data,
    type: "histogram"
  };
  var data = [trace];

  return (
    <Plot
      data={data}
      layout={layout}
      onInitialized={figure => this.setState(figure)}
      onUpdate={figure => this.setState(figure)}
    />
  );
}
export default FacetsGrid;
