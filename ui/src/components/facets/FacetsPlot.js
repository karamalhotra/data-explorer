import "./FacetsPlot.css";
import FacetCard from "./FacetCard";

import React, { Component } from "react";
import { GridList, GridTile } from "material-ui/GridList";
import Plot from "react-plotly.js";
import FacetsDropDown from "./FacetsDropDown";

function FacetsPlot(props) {
  const Data = props.allData;
  const plot = props.plot;
  const plot2 = props.plot2;

  //  console.log(Data)
  console.log(props.plot);
  console.log(props.plot2);
  console.log(Data[props.plot + "_" + props.plot2]);
  var fruits = Data[props.plot];
  console.log(fruits);

  var layout = {
    width: 1900,
    height: 900,
    annotations: [
      {
        xref: "paper",
        yref: "paper",
        x: 0.3,
        xanchor: "right",
        y: 1,
        yanchor: "bottom",
        text: props.plot + " Distribution",
        font: { size: 32 },
        showarrow: false
      },
      {
        xref: "paper",
        yref: "paper",
        x: 0.97,
        xanchor: "right",
        y: 1,
        yanchor: "bottom",
        text: "Correlation between " + props.plot + " and " + props.plot2,
        font: { size: 32 },
        showarrow: false
      },
      {
        xref: "paper",
        yref: "paper",
        x: 0.93,
        xanchor: "right",
        y: 0.95,
        yanchor: "bottom",
        text: Data[props.plot + "_" + props.plot2],
        font: { size: 32 },
        showarrow: false
      }
    ],
    xaxis: { title: props.plot, domain: [0, 0.45], titlefont: { size: 28 } },
    yaxis: { title: "# of participants", titlefont: { size: 28 } },

    yaxis2: { title: props.plot2, titlefont: { size: 28 }, anchor: "x2" },
    xaxis2: { title: props.plot, titlefont: { size: 28 }, domain: [0.65, 1] }
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
export default FacetsPlot;
