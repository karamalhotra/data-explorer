import "./FacetsGrid.css";
import FacetCard from "./FacetCard";

import React, { Component } from "react";
import { GridList, GridTile } from "material-ui/GridList";
import Plot from "react-plotly.js";

function FacetsGrid(props) {
  const facets = props.facets;
  const updateFacets = props.updateFacets;
  const facetsList = facets.map(facet => (
    <GridTile key={facet.name}>
      <FacetCard facet={facet} updateFacets={updateFacets} />
    </GridTile>
  ));

  var layout = { width: 320, height: 240, title: "HI" };
  return (
    <Plot
      data={[
        {
          x: [1, 2, 3],
          y: [2, 6, 3],
          type: "scatter",
          mode: "lines+points",
          marker: { color: "red" }
        },
        { type: "bar", x: [1, 2, 3], y: [2, 5, 3] }
      ]}
      layout={layout}
    />
  );
}

export default FacetsGrid;
