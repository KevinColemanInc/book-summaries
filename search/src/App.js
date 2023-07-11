import React, { Component } from "react";
import axios from "axios";

import { search } from "./utils";
import Summaries from "./Summaries";

class App extends Component {
  state = {
    summaries: null,
    loading: false,
    value: ""
  };

  search = async (query, chapter) => {
    if (!query || !chapter) {
      return;
    }
    this.setState({ loading: true });
    const results = await search(
    `http://127.0.0.1:8000/query?q=${query}&chapter=${chapter}`
    );
    const summaries = results;
    console.log('summaries', summaries )

    this.setState({ summaries, loading: false });
  };

  onChangeQueryHandler = async e => {
    this.search(e.target.value, this.state.chapter);
    this.setState({ value: e.target.value });
  };

  onChangeChapterHandler = async e => {
    this.search(this.state.value, e.target.value);
    this.setState({ chapter: e.target.value });
  };



  renderSumaries() {
    let summaries = <p>There are no summaries</p>;
    console.log("renderSumaries.query", this.state.value);
    if (this.state.summaries) {
      summaries = <Summaries list={this.state.summaries} query={this.state.value} />;
    }

    return summaries;
  }

  render() {
    return (
      <div style={{textAlign: ""}}>
        <div className="container">
            <h1>SSS: Summary Semantic Search</h1>
            <p>Search</p>
            <input
                value={this.state.value}
                onChange={e => this.onChangeQueryHandler(e)}
                placeholder="Type something to search"
            />
            <p>Up to Chapter</p>
                <input
                value={this.state.chapter}
                type="number"
                min={1}
                max={1}
                onChange={e => this.onChangeChapterHandler(e)}
                placeholder="chapter"
                />
        {this.renderSumaries()}
        </div>
      </div>
    );
  }
}

export default App;
