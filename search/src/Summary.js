import React from "react";

import classes from "./Summary.module.css";
import { truncStr } from "./utils";
import Highlighter from "react-highlight-words";

const Summary = props => {
  const { summary, chapter } = props.item;
  let terms = []
  if (props.query.length > 0) {
    terms = props.query.split(" ")
  }

  return (
    <div
      className={classes.Container}
    >
        <p className={classes.VoteContainer}>Chapter {(chapter)} Summary Snippet</p>
        <p className={classes.Title}>
        <Highlighter
            highlightClassName="YourHighlightClass"
            searchWords={terms}
            autoEscape={true}
            textToHighlight={summary}
        />
        </p>
    </div>
  );
};

export default Summary;
