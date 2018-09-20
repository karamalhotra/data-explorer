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
  var fruits = Data[props.plot2];
  console.log(Data["select_k_best_title"]);
  console.log(Data[props.plot]);

  var layout = {
    width: 1900,
    height: 1500,
    //barmode: 'stack',
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
        x: 0.92,
        xanchor: "right",
        y: 0.4,
        yanchor: "bottom",
        text: "PCA analysis",
        font: { size: 32 },
        showarrow: false
      },
      {
        xref: "paper",
        yref: "paper",
        x: 0.4,
        xanchor: "right",
        y: 0.4,
        yanchor: "bottom",
        text: Data["select_k_best_title"],
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
        y: 0.97,
        yanchor: "bottom",
        text: Data[props.plot + "_" + props.plot2],
        font: { size: 32 },
        showarrow: false
      }
    ],
    xaxis: { title: props.plot, domain: [0, 0.45], titlefont: { size: 28 } },
    yaxis: {
      title: "# of participants",
      titlefont: { size: 28 },
      domain: [0.65, 0.95]
    },

    yaxis2: {
      title: props.plot2,
      titlefont: { size: 28 },
      anchor: "x2",
      domain: [0.65, 0.95]
    },
    xaxis2: { title: props.plot, titlefont: { size: 28 }, domain: [0.65, 1] },

    yaxis3: { title: "score", titlefont: { size: 28 }, domain: [0.1, 0.35] },
    xaxis3: {
      domain: [0, 0.45],
      anchor: "y3",
      tickfont: { size: 18 },
      tickangle: 75
    },

    yaxis4: { domain: [0.1, 0.35] },
    xaxis4: { domain: [0.65, 1], anchor: "y4" }
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

  var trace3 = {
    x: Data["select_k_best_predictors"],
    y: Data["select_k_best_scores"],
    xaxis: "x3",
    yaxis: "y3",
    mode: "markers",
    type: "scatter"
  };

  var trace4 = {
    x: Data["comp_features"],
    y: Data["com0"],
    xaxis: "x4",
    yaxis: "y4",
    name: "Component1",
    type: "bar"
  };

  var trace5 = {
    x: Data["comp_features"],
    y: Data["com1"],
    xaxis: "x4",
    yaxis: "y4",
    name: "Component2",
    type: "bar"
  };
  var trace6 = {
    x: Data["comp_features"],
    y: Data["com2"],
    xaxis: "x4",
    yaxis: "y4",
    name: "Component3",
    type: "bar"
  };

  var data = [trace, trace2, trace3, trace4, trace5, trace6];

  return <Plot data={data} layout={layout} />;
}
export default FacetsPlot;
