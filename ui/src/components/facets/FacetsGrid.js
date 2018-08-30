import "./FacetsGrid.css";
import FacetCard from "./FacetCard";

import React, { Component } from "react";
import { GridList, GridTile } from "material-ui/GridList";
import Plot from "react-plotly.js";
import FacetsDropDown from "./FacetsDropDown";

function FacetsGrid(props) {
  const Data = props.allData;
  const plot = props.plot;
  const plot2 = props.plot2;

  console.log("KB HERE");
  //  console.log(Data)
  console.log(props.plot);
  console.log(props.plot2);
  console.log(Data["highest_correlation"]);

  //console.log(Data[props.plot])
  var layout = {
    width: 1900,
    height: 900,
    annotations: [
      {
        xref: "paper",
        yref: "paper",
        x: 0.9,
        xanchor: "right",
        y: 1,
        yanchor: "bottom",
        text: Data["highest_correlation"],
        showarrow: false
      }
    ],
    xaxis: { title: props.plot, domain: [0, 0.45] },
    yaxis: { title: "# of participants" },

    yaxis2: { title: props.plot2, anchor: "x2" },
    xaxis2: { title: props.plot, domain: [0.65, 1] }
  };
  var trace = {
    x: Data[props.plot],
    type: "histogram"
  };
  var trace2 = {
    x: Data[props.plot],
    y: Data[props.plot2],
    xaxis: "x2",
    yaxis: "y2",
    mode: "markers",
    type: "scatter"
  };

  var data = [trace, trace2];

  return <Plot data={data} layout={layout} />;
}
export default FacetsGrid;
