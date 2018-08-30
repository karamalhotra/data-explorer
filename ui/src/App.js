import "./App.css";
import { ApiClient, DatasetApi, FacetsApi } from "data_explorer_service";
import ExportFab from "./components/ExportFab";
import FacetsGrid from "./components/facets/FacetsGrid";
import Header from "./components/Header";
import FacetsDropDown from "./components/facets/FacetsDropDown";

import React, { Component } from "react";
import { MuiThemeProvider } from "material-ui";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      datasetName: "",
      thisPlot: null,
      thisPlot2: null,
      facets: null,
      totalCount: null,
      allData: null,
      handleChange: 2
    };

    this.apiClient = new ApiClient();
    this.apiClient.basePath = "/api";
    this.facetsApi = new FacetsApi(this.apiClient);
    this.facetsCallback = function(error, data) {
      if (error) {
        console.error(error);
        // TODO(alanhwang): Redirect to an error page
      } else {
        console.log("setting state here");
        console.log(this.state.thisPlot);
        this.setState({
          facets: data.facets,
          thisPlot: data.plot_name,
          thisPlot2: data.plot_name2,
          totalCount: data.count,
          allData: data.datak,
          hanldeChange: data.handleChange
        });
      }
    }.bind(this);
    // Map from facet name to a list of facet values.
    this.filterMap = new Map();
    this.updateFacets = this.updateFacets.bind(this);
    this.updatePlot = this.updatePlot.bind(this);
    this.updatePlot2 = this.updatePlot2.bind(this);
  }

  render() {
    //    debugger;
    if (this.state.facets == null || this.state.datasetName === "") {
      // Server has not yet responded or returned an error
      return <div />;
    } else {
      return (
        <MuiThemeProvider>
          <div className="app">
            <Header
              datasetName={this.state.datasetName}
              totalCount={this.state.totalCount}
            />
            <p id="p">Plot</p>

            <FacetsDropDown
              updatePlot={this.updatePlot}
              updatePlot2={this.updatePlot2}
              facets={this.state.facets}
              allData={this.state.allData}
              center="1"
            />
            <p id="p">Correlate to: </p>

            <FacetsDropDown
              updatePlot={this.updatePlot}
              updatePlot2={this.updatePlot2}
              facets={this.state.facets}
              allData={this.state.allData}
              center="2"
            />
            <FacetsGrid
              allData={this.state.allData}
              plot={this.state.thisplot}
              plot2={this.state.thisplot2}
            />
          </div>
        </MuiThemeProvider>
      );
    }
  }

  componentDidMount() {
    this.facetsApi.facetsGet({ plot: "Age" }, this.facetsCallback);

    // Call /api/dataset
    let datasetApi = new DatasetApi(this.apiClient);
    let datasetCallback = function(error, data) {
      if (error) {
        console.error(error);
        // TODO(alanhwang): Redirect to an error page
      } else {
        this.setState({ datasetName: data.name });
      }
    }.bind(this);
    datasetApi.datasetGet(datasetCallback);
  }

  /**
   * Updates the selection for a single facet value and refreshes the facets data from the server.
   * @param facetName string containing the name of the facet corresponding to this value
   * @param facetValue string containing the name of this facet value
   * @param isSelected bool indicating whether this facetValue should be added to or removed from the query
   * */

  updatePlot(plotValue) {
    this.setState({
      thisplot: this.state.facets[plotValue].name
    });
    this.facetsApi.facetsGet(
      { plot: this.state.facets[plotValue].name, plot2: this.state.thisplot2 },
      this.facetsCallback
    );
  }
  updatePlot2(plotValue) {
    console.log("IN Update pLot 2");
    console.log(plotValue);
    this.setState({
      thisplot2: this.state.facets[plotValue].name
    });
    this.facetsApi.facetsGet(
      { plot: this.state.thisplot, plot2: this.state.facets[plotValue].name },
      this.facetsCallback
    );
  }

  updateFacets(plotValue, facetName, facetValue, isSelected) {
    console.log("in updateFacets");
    console.log(plotValue);

    this.setState({
      thisplot: this.state.facets[plotValue].name
    });
    //    console.log('-------------')
    //    console.log(this.state.plot)

    let currentFacetValues = this.filterMap.get(facetName);
    if (isSelected) {
      // Add facetValue to the list of filters for facetName
      if (currentFacetValues === undefined) {
        this.filterMap.set(facetName, [facetValue]);
      } else {
        currentFacetValues.push(facetValue);
      }
    } else if (this.filterMap.get(facetName) !== undefined) {
      // Remove facetValue from the list of filters for facetName
      this.filterMap.set(
        facetName,
        this.removeFacet(currentFacetValues, facetValue)
      );
    }

    let filterArray = this.filterMapToArray(this.filterMap);
    if (filterArray.length > 0) {
      this.facetsApi.facetsGet(
        { plot: this.state.facets[plotValue].name },
        this.facetsCallback
      );
    } else {
      this.facetsApi.facetsGet(
        { plot: this.state.facets[plotValue].name },
        this.facetsCallback
      );
    }
  }

  removeFacet(valueList, facetValue) {
    let newValueList = [];
    for (let i = 0; i < valueList.length; i++) {
      if (valueList[i] !== facetValue) {
        newValueList.push(valueList[i]);
      }
    }
    return newValueList;
  }

  /**
   * Converts a Map of filters to an Array of filter strings interpretable by
   * the backend
   * @param filterMap Map of facetName:[facetValues] pairs
   * @return [string] Array of "facetName=facetValue" strings
   */
  filterMapToArray(filterMap) {
    let filterArray = [];
    filterMap.forEach((values, key) => {
      // Scenario where there are no values for a key: A single value is
      // checked for a facet. The value is unchecked. The facet name will
      // still be a key in filterMap, but there will be no values.
      if (values.length > 0) {
        for (let value of values) {
          filterArray.push(key + "=" + value);
        }
      }
    });
    return filterArray;
  }
}

export default App;
